from celery import Celery
from celery.signals import worker_ready
from kombu import Queue

from app.core.config import settings
from app.core.orchestrator import orchestrator

# Initialize Celery app
celery_app = Celery(
    "ai_orchestration",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_queues=(
        Queue("code_tasks", routing_key="code.#"),
        Queue("design_tasks", routing_key="design.#"),
        Queue("marketing_tasks", routing_key="marketing.#"),
    ),
    task_routes={
        "app.core.celery_app.execute_code_task": {"queue": "code_tasks"},
        "app.core.celery_app.execute_design_task": {"queue": "design_tasks"},
        "app.core.celery_app.execute_marketing_task": {"queue": "marketing_tasks"},
    },
    task_default_queue="code_tasks",
    task_default_exchange="tasks",
    task_default_routing_key="code.default",
    worker_prefetch_multiplier=1,  # Process one task at a time per worker
    task_acks_late=True,  # Acknowledge tasks after completion
    task_track_started=True,  # Track when tasks are started
    task_time_limit=3600,  # 1 hour timeout
    task_soft_time_limit=3300,  # Soft timeout 55 minutes
    worker_max_tasks_per_child=50,  # Restart worker after 50 tasks
)

@worker_ready.connect
def on_worker_ready(**_):
    """Initialize the orchestrator when Celery worker starts"""
    orchestrator.initialize()

@celery_app.task(bind=True, name="app.core.celery_app.execute_code_task")
def execute_code_task(self, task_id: str, task_data: dict):
    """Execute a coding task"""
    return orchestrator.submit_task(
        task_type="code",
        title=task_data["title"],
        description=task_data["description"],
        priority=task_data.get("priority", "medium"),
        context=task_data.get("context")
    )

@celery_app.task(bind=True, name="app.core.celery_app.execute_design_task")
def execute_design_task(self, task_id: str, task_data: dict):
    """Execute a design task"""
    return orchestrator.submit_task(
        task_type="design",
        title=task_data["title"],
        description=task_data["description"],
        priority=task_data.get("priority", "medium"),
        context=task_data.get("context")
    )

@celery_app.task(bind=True, name="app.core.celery_app.execute_marketing_task")
def execute_marketing_task(self, task_id: str, task_data: dict):
    """Execute a marketing task"""
    return orchestrator.submit_task(
        task_type="marketing",
        title=task_data["title"],
        description=task_data["description"],
        priority=task_data.get("priority", "medium"),
        context=task_data.get("context")
    )

@celery_app.task(bind=True, name="app.core.celery_app.check_cost_limit")
def check_cost_limit(self):
    """Periodic task to check API cost limits"""
    status = orchestrator.get_system_status()
    if status["cost_limit_reached"]:
        # TODO: Implement notification system
        print("Cost limit reached! Pausing new task execution.")
        return False
    return True

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    "check-cost-limit": {
        "task": "app.core.celery_app.check_cost_limit",
        "schedule": 300.0,  # Check every 5 minutes
    },
}

# Error handling
@celery_app.task(bind=True, name="app.core.celery_app.handle_task_error")
def handle_task_error(self, task_id: str, error: str):
    """Handle task execution errors"""
    orchestrator.cancel_task(task_id)
    # TODO: Implement error notification system
    print(f"Task {task_id} failed: {error}")

# Task monitoring
@celery_app.task(bind=True, name="app.core.celery_app.monitor_task_progress")
def monitor_task_progress(self, task_id: str):
    """Monitor and report task progress"""
    try:
        status = orchestrator.get_task_status(task_id)
        if status["status"] in ["completed", "failed"]:
            return status
        
        # Recheck progress in 30 seconds
        self.retry(countdown=30)
    except Exception as e:
        handle_task_error.delay(task_id, str(e))
        return {"status": "failed", "error": str(e)}
