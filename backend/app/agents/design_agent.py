from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

from app.agents.base import BaseAgent, AgentContext, AgentResult
from app.api.api_v1.endpoints.agents import AgentType, AgentStatus, AgentCapability
from app.core.config import settings

class DesignAgent(BaseAgent):
    """Agent specialized for graphic design and image generation tasks"""

    def __init__(self, agent_id: str):
        super().__init__(agent_id, AgentType.DESIGN)
        self.model = None
        self.verification_model = None
        self.capabilities = [
            AgentCapability(
                name="image_generation",
                description="Generate images based on descriptions",
                parameters={
                    "description": "Detailed description of the desired image",
                    "style": "Artistic style to apply",
                    "dimensions": "Image dimensions (width x height)",
                    "format": "Output format (png, jpg, etc.)"
                },
                required_resources=["openai", "stable-diffusion"]
            ),
            AgentCapability(
                name="design_review",
                description="Review and suggest improvements for designs",
                parameters={
                    "image": "Image to review",
                    "context": "Usage context and requirements",
                    "focus_areas": "Specific areas to focus on (composition, color, etc.)"
                },
                required_resources=["openai"]
            ),
            AgentCapability(
                name="style_guide_generation",
                description="Generate brand style guides",
                parameters={
                    "brand_name": "Name of the brand",
                    "brand_values": "Core values and personality",
                    "target_audience": "Description of target audience",
                    "industry": "Industry or market sector"
                },
                required_resources=["openai"]
            )
        ]

    async def initialize(self) -> bool:
        """Initialize the design agent with required models"""
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
            
            # TODO: Initialize image generation model (e.g., DALL-E or Stable Diffusion)
            
            return True
        except Exception as e:
            await self.handle_error(e)
            return False

    def get_capabilities(self) -> List[AgentCapability]:
        """Return the agent's capabilities"""
        return self.capabilities

    async def execute_task(self, context: AgentContext) -> AgentResult:
        """Execute a design task based on the context"""
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
            if task_type == "image_generation":
                result = await self._generate_image(context)
            else:
                response = await self.model.agenerate([prompt])
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
        """Validate the design using the verification model"""
        try:
            if not result.success:
                return False

            # For image generation tasks, verify the image meets requirements
            if "image_url" in result.output:
                validation_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a design expert. Validate if the generated image meets the requirements."),
                    ("user", f"Image URL: {result.output['image_url']}\n"
                            f"Requirements: {result.output['requirements']}\n"
                            f"Does this image meet the specified requirements?")
                ])
            else:
                # For other design tasks, validate the textual output
                validation_prompt = ChatPromptTemplate.from_messages([
                    ("system", "You are a design expert. Validate the following design suggestions."),
                    ("user", f"Design output:\n{result.output.get('suggestions', '')}")
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

    async def _generate_image(self, context: AgentContext) -> AgentResult:
        """Generate image based on description"""
        try:
            # TODO: Implement actual image generation using DALL-E or Stable Diffusion
            # This is a placeholder that simulates image generation
            return AgentResult(
                success=True,
                output={
                    "image_url": "https://placeholder.com/generated_image.png",
                    "requirements": context.input_data.get("description"),
                    "metadata": {
                        "dimensions": context.input_data.get("dimensions"),
                        "style": context.input_data.get("style")
                    }
                },
                tokens_used=0,  # Image generation might use different metrics
                cost=0.1  # Placeholder cost
            )
        except Exception as e:
            return AgentResult(
                success=False,
                output={},
                error=f"Image generation failed: {str(e)}"
            )

    def _get_prompt_for_task(self, task_type: str, context: AgentContext, rag_context: List[Dict[str, Any]]) -> str:
        """Generate appropriate prompt based on task type"""
        base_context = f"Previous related work:\n{rag_context}\n" if rag_context else ""
        
        prompts = {
            "design_review": ChatPromptTemplate.from_messages([
                ("system", "You are a design expert. Review the design and suggest improvements."),
                ("user", f"{base_context}Design to review:\n{context.input_data.get('image')}\n"
                        f"Context: {context.input_data.get('context')}\n"
                        f"Focus areas: {context.input_data.get('focus_areas')}")
            ]),
            "style_guide_generation": ChatPromptTemplate.from_messages([
                ("system", "You are a brand design expert. Create a comprehensive style guide."),
                ("user", f"{base_context}Brand: {context.input_data.get('brand_name')}\n"
                        f"Values: {context.input_data.get('brand_values')}\n"
                        f"Target Audience: {context.input_data.get('target_audience')}\n"
                        f"Industry: {context.input_data.get('industry')}")
            ])
        }
        
        return prompts.get(task_type, prompts["design_review"])

    def _parse_response(self, response: Any) -> AgentResult:
        """Parse the model's response into a standardized format"""
        try:
            text = response.generations[0].text
            return AgentResult(
                success=True,
                output={
                    "suggestions": text,
                    "explanation": "Generated design suggestions based on requirements"
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
