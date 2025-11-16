"""
Workflow engine for defining and executing business processes.
"""

from typing import Dict, Any, List, Callable, Optional
from loguru import logger
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class Task:
    """Represents a workflow task."""
    name: str
    action: Callable
    dependencies: List[str]
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None


class Workflow:
    """Represents a business workflow."""
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize workflow.
        
        Args:
            name: Workflow name
            description: Workflow description
        """
        self.name = name
        self.description = description
        self.tasks: Dict[str, Task] = {}
    
    def add_task(
        self,
        name: str,
        action: Callable,
        dependencies: Optional[List[str]] = None
    ) -> None:
        """
        Add a task to the workflow.
        
        Args:
            name: Task name
            action: Function to execute for this task
            dependencies: List of task names this task depends on
        """
        self.tasks[name] = Task(
            name=name,
            action=action,
            dependencies=dependencies or []
        )
    
    def get_task(self, name: str) -> Optional[Task]:
        """Get a task by name."""
        return self.tasks.get(name)


class WorkflowEngine:
    """Engine for executing workflows."""
    
    def __init__(self):
        """Initialize workflow engine."""
        self.workflows: Dict[str, Workflow] = {}
        logger.info("Workflow engine initialized")
    
    def register_workflow(self, workflow: Workflow) -> None:
        """
        Register a workflow.
        
        Args:
            workflow: Workflow instance to register
        """
        self.workflows[workflow.name] = workflow
        logger.info(f"Registered workflow: {workflow.name}")
    
    def execute_workflow(
        self,
        workflow_name: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow.
        
        Args:
            workflow_name: Name of workflow to execute
            context: Optional context dictionary
        
        Returns:
            Execution results
        """
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow not found: {workflow_name}")
        
        workflow = self.workflows[workflow_name]
        logger.info(f"Executing workflow: {workflow_name}")
        
        context = context or {}
        executed_tasks = set()
        
        # Execute tasks respecting dependencies
        while len(executed_tasks) < len(workflow.tasks):
            progress_made = False
            
            for task_name, task in workflow.tasks.items():
                if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.SKIPPED]:
                    continue
                
                # Check if dependencies are met
                if all(dep in executed_tasks for dep in task.dependencies):
                    try:
                        task.status = TaskStatus.RUNNING
                        logger.info(f"Executing task: {task_name}")
                        
                        task.result = task.action(context)
                        task.status = TaskStatus.COMPLETED
                        executed_tasks.add(task_name)
                        progress_made = True
                        
                    except Exception as e:
                        task.status = TaskStatus.FAILED
                        task.error = str(e)
                        logger.error(f"Task {task_name} failed: {e}")
                        executed_tasks.add(task_name)
                        progress_made = True
            
            if not progress_made:
                # Circular dependency or missing dependency
                remaining = [name for name in workflow.tasks.keys() if name not in executed_tasks]
                raise RuntimeError(f"Cannot execute workflow: circular dependency or missing dependencies. Remaining tasks: {remaining}")
        
        # Collect results
        results = {
            task_name: {
                "status": task.status.value,
                "result": task.result,
                "error": task.error
            }
            for task_name, task in workflow.tasks.items()
        }
        
        success_count = sum(1 for t in workflow.tasks.values() if t.status == TaskStatus.COMPLETED)
        logger.info(f"Workflow {workflow_name} completed: {success_count}/{len(workflow.tasks)} tasks succeeded")
        
        return results

