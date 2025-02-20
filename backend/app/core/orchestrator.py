from typing import Dict, List, Optional, Type
import asyncio
from uuid import uuid4
from datetime import datetime

from app.agents.base import BaseAgent, AgentContext, AgentResult
from app.agents.coding_agent import CodingAgent
from app.agents.design_agent import DesignAgent
from app.agents.marketing_agent import MarketingAgent
from app.api.api_v1.endpoints.tasks import TaskType, TaskStatus, TaskPriority
from app.core.config import settings

class TaskManager:
    """Manages task execution and status tracking"""
    def __init__(self, task_id: str, task_type: TaskType, priority: TaskPriority):
        self.task_id = task_id
        self.type = task_type
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.progress = 0.0
        self.result: Optional[AgentResult] = None
        self.error: Optional[str] = None
        self.cost = 0.0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update_status(self, status: TaskStatus, progress: float = None):
        self.status = status
        if progress is not None:
            self.progress = progress
        self.updated_at = datetime.utcnow()

class Orchestrator:
    """Manages task distribution and agent coordination"""
    
    def __init__(self):
        self._agents: Dict[TaskType, List[BaseAgent]] = {
            TaskType.CODE: [],
            TaskType.DESIGN: [],
            TaskType.MARKETING: []
        }
        self._tasks: Dict[str, TaskManager] = {}
        self._total_cost = 0.0
        self._cost_limit_reached = False
        self._agent_classes = {
            TaskType.CODE: CodingAgent,
            TaskType.DESIGN: DesignAgent,
            TaskType.MARKETING: MarketingAgent
        }

    async def initialize(self):
        """Initialize the orchestrator and create initial agent pool"""
        try:
            # Create initial agents
            await self._create_agent(TaskType.CODE, "coding-agent-1")
            await self._create_agent(TaskType.DESIGN, "design-agent-1")
            await self._create_agent(TaskType.MARKETING, "marketing-agent-1")
            return True
        except Exception as e:
            print(f"Failed to initialize orchestrator: {str(e)}")
            return False

    async def submit_task(
        self,
        task_type: TaskType,
        title: str,
        description: str,
        priority: TaskPriority = TaskPriority.MEDIUM,
        context: Optional[dict] = None
    ) -> str:
        """Submit a new task for processing"""
        task_id = str(uuid4())
        task = TaskManager(task_id, task_type, priority)
        self._tasks[task_id] = task

        # Start task processing in background
        asyncio.create_task(self._process_task(task_id, {
            "title": title,
            "description": description,
            "context": context or {}
        }))

        return task_id

    async def get_task_status(self, task_id: str) -> Dict:
        """Get current status of a task"""
        if task_id not in self._tasks:
            raise ValueError("Task not found")
        
        task = self._tasks[task_id]
        return {
            "id": task_id,
            "type": task.type,
            "status": task.status,
            "progress": task.progress,
            "cost": task.cost,
            "result": task.result.output if task.result else None,
            "error": task.error,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task"""
        if task_id not in self._tasks:
            return False
        
        task = self._tasks[task_id]
        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED]:
            return False
        
        task.update_status(TaskStatus.FAILED)
        task.error = "Task cancelled by user"
        return True

    async def _create_agent(self, agent_type: TaskType, agent_id: str) -> bool:
        """Create and initialize a new agent"""
        agent_class = self._agent_classes[agent_type]
        agent = agent_class(agent_id)
        if await agent.initialize():
            self._agents[agent_type].append(agent)
            return True
        return False

    async def _get_available_agent(self, task_type: TaskType) -> Optional[BaseAgent]:
        """Get an available agent for the task type"""
        for agent in self._agents[task_type]:
            if agent.status == "idle":
                return agent
        return None

    async def _check_cost_limit(self, estimated_cost: float) -> bool:
        """Check if the task would exceed the cost limit"""
        if self._total_cost + estimated_cost > settings.COST_LIMIT:
            if not self._cost_limit_reached:
                self._cost_limit_reached = True
                # TODO: Implement notification system for cost limit
            return False
        return True

    async def _process_task(self, task_id: str, task_data: Dict) -> None:
        """Process a task using appropriate agent"""
        task = self._tasks[task_id]
        
        try:
            # Get available agent
            agent = await self._get_available_agent(task.type)
            if not agent:
                task.update_status(TaskStatus.FAILED)
                task.error = "No available agent found"
                return

            # Prepare task context
            context = AgentContext(
                task_id=task_id,
                input_data=task_data
            )

            # Update task status
            task.update_status(TaskStatus.IN_PROGRESS, 0.2)

            # Execute task
            result = await agent.execute_task(context)
            
            # Track cost
            if result.success:
                new_cost = self._total_cost + result.cost
                if await self._check_cost_limit(result.cost):
                    self._total_cost = new_cost
                    task.cost = result.cost
                else:
                    task.update_status(TaskStatus.FAILED)
                    task.error = "Cost limit reached"
                    return

            # Verify result if successful
            if result.success:
                task.update_status(TaskStatus.VERIFYING, 0.8)
                is_valid = await agent.validate_result(result)
                if not is_valid:
                    task.update_status(TaskStatus.FAILED)
                    task.error = "Result validation failed"
                    return

            # Update task status
            if result.success:
                task.update_status(TaskStatus.COMPLETED, 1.0)
                task.result = result
            else:
                task.update_status(TaskStatus.FAILED)
                task.error = result.error

        except Exception as e:
            task.update_status(TaskStatus.FAILED)
            task.error = str(e)

    async def get_system_status(self) -> Dict:
        """Get overall system status"""
        return {
            "total_cost": self._total_cost,
            "cost_limit_reached": self._cost_limit_reached,
            "active_tasks": len([t for t in self._tasks.values() if t.status == TaskStatus.IN_PROGRESS]),
            "completed_tasks": len([t for t in self._tasks.values() if t.status == TaskStatus.COMPLETED]),
            "failed_tasks": len([t for t in self._tasks.values() if t.status == TaskStatus.FAILED]),
            "agents": {
                task_type.value: len(agents)
                for task_type, agents in self._agents.items()
            }
        }

# Global orchestrator instance
orchestrator = Orchestrator()
