from fastapi import APIRouter

from app.api.api_v1.endpoints import tasks, agents, costs

api_router = APIRouter()

api_router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["tasks"]
)

api_router.include_router(
    agents.router,
    prefix="/agents",
    tags=["agents"]
)

api_router.include_router(
    costs.router,
    prefix="/costs",
    tags=["costs"]
)
