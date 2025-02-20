from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from app.agents.base import BaseAgent, AgentContext, AgentResult
from app.api.api_v1.endpoints.agents import AgentType, AgentStatus, AgentCapability
from app.core.config import settings

class MarketingAgent(BaseAgent):
    """Agent specialized for marketing content creation and strategy"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.MARKETING)
        self.model = None
        self.verification_model = None
        self.capabilities = [
            AgentCapability(
                name="content_creation",
                description="Generate marketing content",
                parameters={
                    "content_type": "Type of content (blog, social, email, etc.)",
                    "target_audience": "Description of target audience",
                    "tone": "Desired tone of voice",
                    "key_messages": "Main points to convey",
                    "platform": "Platform where content will be published",
                    "length": "Desired content length"
                },
                required_resources=["openai"]
            ),
            AgentCapability(
                name="campaign_strategy",
                description="Develop marketing campaign strategies",
                parameters={
                    "objectives": "Campaign goals and objectives",
                    "target_audience": "Target audience details",
                    "budget": "Available budget",
                    "timeline": "Campaign timeline",
                    "channels": "Preferred marketing channels"
                },
                required_resources=["openai"]
            ),
            AgentCapability(
                name="market_analysis",
                description="Analyze market trends and competition",
                parameters={
                    "industry": "Industry or market sector",
                    "competitors": "List of main competitors",
                    "region": "Geographic region",
                    "focus_areas": "Specific areas to analyze"
                },
                required_resources=["openai"]
            )
        ]

    async def initialize(self) -> bool:
        """Initialize the marketing agent with required models"""
        try:
            self.model = ChatOpenAI(
                model_name=settings.DEFAULT_MODEL,
                temperature=0.7,
                openai_api_key=settings.OPENAI_API_KEY
            )
            
            self.verification_model = ChatOpenAI(
                model_name=settings.VERIFICATION_MODEL,
                temperature=0.2,
                openai_api_key=settings.OPENAI_API_KEY
            )
            
            return True
        except Exception as e:
            await self.handle_error(e)
            return False

    def get_capabilities(self) -> List[AgentCapability]:
        """Return the agent's capabilities"""
        return self.capabilities

    async def execute_task(self, context: AgentContext) -> AgentResult:
        """Execute a marketing task based on the context"""
        try:
            if not await self.prepare_task(context):
                return AgentResult(
                    success=False,
                    output={},
                    error="Agent is busy or unavailable"
                )

            # Get relevant context from RAG
            rag_context = await self._get_rag_context(
                f"{context.input_data.get('task_type', '')} {context.input_data.get('description', '')}"
            )

            # Prepare the prompt based on task type
            task_type = context.input_data.get("task_type")
            prompt = self._get_prompt_for_task(task_type, context, rag_context)

            # Execute the task
            response = await self.model.agenerate([prompt])
            result = self._parse_response(response, task_type)
            
            # Track token usage and cost
            await self._track_usage(
                tokens=response.usage.total_tokens,
                cost=self._calculate_cost(response.usage.total_tokens)
            )

            # Store result in RAG if successful
            if result.success:
                await self._store_result(context, result)

            await self.cleanup_task()
            return result

        except Exception as e:
            await self.handle_error(e)
            return AgentResult(
                success=False,
                output={},
                error=str(e)
            )

    async def validate_result(self, result: AgentResult) -> bool:
        """Validate the marketing content using the verification model"""
        try:
            if not result.success:
                return False

            task_type = result.metadata.get("task_type")
            validation_prompts = {
                "content_creation": ChatPromptTemplate.from_messages([
                    ("system", "You are a marketing content expert. Validate the following content for effectiveness, tone, and alignment with requirements."),
                    ("user", f"Content:\n{result.output.get('content')}\n"
                            f"Requirements:\n{result.output.get('requirements')}\n"
                            f"Target Audience: {result.output.get('target_audience')}")
                ]),
                "campaign_strategy": ChatPromptTemplate.from_messages([
                    ("system", "You are a marketing strategy expert. Validate the following campaign strategy."),
                    ("user", f"Strategy:\n{result.output.get('strategy')}\n"
                            f"Objectives: {result.output.get('objectives')}\n"
                            f"Budget: {result.output.get('budget')}")
                ]),
                "market_analysis": ChatPromptTemplate.from_messages([
                    ("system", "You are a market analysis expert. Validate the following market analysis."),
                    ("user", f"Analysis:\n{result.output.get('analysis')}\n"
                            f"Industry: {result.output.get('industry')}\n"
                            f"Focus Areas: {result.output.get('focus_areas')}")
                ])
            }

            validation_prompt = validation_prompts.get(
                task_type,
                validation_prompts["content_creation"]
            )

            # Get validation response
            validation = await self.verification_model.agenerate([validation_prompt])
            
            # Track validation cost
            await self._track_usage(
                tokens=validation.usage.total_tokens,
                cost=self._calculate_cost(validation.usage.total_tokens, is_verification=True)
            )

            # Parse validation result
            is_valid = "VALID" in validation.generations[0].text.upper()
            return is_valid

        except Exception as e:
            await self.handle_error(e)
            return False

    def _get_prompt_for_task(self, task_type: str, context: AgentContext, rag_context: List[Dict[str, Any]]) -> str:
        """Generate appropriate prompt based on task type"""
        base_context = f"Previous related work:\n{rag_context}\n" if rag_context else ""
        
        prompts = {
            "content_creation": ChatPromptTemplate.from_messages([
                ("system", "You are an expert marketing content creator. Generate engaging content based on the requirements."),
                ("user", f"{base_context}Content Type: {context.input_data.get('content_type')}\n"
                        f"Target Audience: {context.input_data.get('target_audience')}\n"
                        f"Tone: {context.input_data.get('tone')}\n"
                        f"Key Messages: {context.input_data.get('key_messages')}\n"
                        f"Platform: {context.input_data.get('platform')}\n"
                        f"Length: {context.input_data.get('length')}")
            ]),
            "campaign_strategy": ChatPromptTemplate.from_messages([
                ("system", "You are a marketing strategy expert. Develop a comprehensive campaign strategy."),
                ("user", f"{base_context}Objectives: {context.input_data.get('objectives')}\n"
                        f"Target Audience: {context.input_data.get('target_audience')}\n"
                        f"Budget: {context.input_data.get('budget')}\n"
                        f"Timeline: {context.input_data.get('timeline')}\n"
                        f"Channels: {context.input_data.get('channels')}")
            ]),
            "market_analysis": ChatPromptTemplate.from_messages([
                ("system", "You are a market analysis expert. Provide detailed market insights."),
                ("user", f"{base_context}Industry: {context.input_data.get('industry')}\n"
                        f"Competitors: {context.input_data.get('competitors')}\n"
                        f"Region: {context.input_data.get('region')}\n"
                        f"Focus Areas: {context.input_data.get('focus_areas')}")
            ])
        }
        
        return prompts.get(task_type, prompts["content_creation"])

    def _parse_response(self, response: Any, task_type: str) -> AgentResult:
        """Parse the model's response into a standardized format"""
        try:
            text = response.generations[0].text
            output_mapping = {
                "content_creation": {
                    "content": text,
                    "explanation": "Generated marketing content based on requirements"
                },
                "campaign_strategy": {
                    "strategy": text,
                    "explanation": "Developed marketing campaign strategy"
                },
                "market_analysis": {
                    "analysis": text,
                    "explanation": "Completed market analysis"
                }
            }

            return AgentResult(
                success=True,
                output=output_mapping.get(task_type, output_mapping["content_creation"]),
                tokens_used=response.usage.total_tokens,
                metadata={
                    "model_name": response.model_name,
                    "finish_reason": response.generations[0].finish_reason,
                    "task_type": task_type
                }
            )
        except Exception as e:
            return AgentResult(
                success=False,
                output={},
                error=f"Failed to parse response: {str(e)}"
            )

    def _calculate_cost(self, tokens: int, is_verification: bool = False) -> float:
        """Calculate cost based on token usage and model type"""
        # Simplified cost calculation - should be updated with actual pricing
        base_rate = 0.002 if is_verification else 0.001
        return tokens * base_rate
