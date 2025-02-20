from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from app.agents.base import BaseAgent, AgentContext, AgentResult
from app.api.api_v1.endpoints.agents import AgentType, AgentStatus, AgentCapability
from app.core.config import settings

class CodingAgent(BaseAgent):
    """Agent specialized for code generation and analysis tasks"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.CODING)
        self.model = None
        self.verification_model = None
        self.capabilities = [
            AgentCapability(
                name="code_generation",
                description="Generate code based on requirements",
                parameters={
                    "language": "Programming language to use",
                    "framework": "Framework or library preferences",
                    "architecture": "Architectural patterns to follow",
                    "test_coverage": "Whether to include tests"
                },
                required_resources=["openai"]
            ),
            AgentCapability(
                name="code_review",
                description="Review and suggest improvements for existing code",
                parameters={
                    "code": "Code to review",
                    "focus_areas": "Specific areas to focus on (security, performance, etc.)"
                },
                required_resources=["openai"]
            ),
            AgentCapability(
                name="bug_fixing",
                description="Identify and fix bugs in code",
                parameters={
                    "code": "Code with bug",
                    "error_message": "Error message or bug description",
                    "expected_behavior": "Expected code behavior"
                },
                required_resources=["openai"]
            )
        ]

    async def initialize(self) -> bool:
        """Initialize the coding agent with required models"""
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
        """Execute a coding task based on the context"""
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
            
            # Parse and validate the response
            result = self._parse_response(response)
            
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
        """Validate the code using the verification model"""
        try:
            if not result.success:
                return False

            code = result.output.get("code")
            if not code:
                return True  # No code to validate

            # Prepare validation prompt
            validation_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a code review expert. Validate the following code for correctness, security, and best practices."),
                ("user", f"Code to validate:\n{code}")
            ])

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
            "code_generation": ChatPromptTemplate.from_messages([
                ("system", "You are an expert programmer. Generate code based on the requirements."),
                ("user", f"{base_context}Requirements:\n{context.input_data.get('description')}\n"
                        f"Language: {context.input_data.get('language')}\n"
                        f"Framework: {context.input_data.get('framework')}")
            ]),
            "code_review": ChatPromptTemplate.from_messages([
                ("system", "You are a code review expert. Review the code and suggest improvements."),
                ("user", f"{base_context}Code to review:\n{context.input_data.get('code')}\n"
                        f"Focus areas: {context.input_data.get('focus_areas')}")
            ]),
            "bug_fixing": ChatPromptTemplate.from_messages([
                ("system", "You are a debugging expert. Analyze and fix the bug in the code."),
                ("user", f"{base_context}Buggy code:\n{context.input_data.get('code')}\n"
                        f"Error: {context.input_data.get('error_message')}\n"
                        f"Expected behavior: {context.input_data.get('expected_behavior')}")
            ])
        }
        
        return prompts.get(task_type, prompts["code_generation"])

    def _parse_response(self, response: Any) -> AgentResult:
        """Parse the model's response into a standardized format"""
        try:
            text = response.generations[0].text
            return AgentResult(
                success=True,
                output={
                    "code": text,
                    "explanation": "Generated code based on requirements"
                },
                tokens_used=response.usage.total_tokens,
                metadata={
                    "model_name": response.model_name,
                    "finish_reason": response.generations[0].finish_reason
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
