# [Task T-019 to T-022, T-026, T-037-T-038, T-045, T-052] Task CRUD operations
"""
task_manager.py - CRUD operations for task management with in-memory storage

Per contracts/task_manager.md and data-model.md
"""

from datetime import datetime
from typing import Dict, List, Optional


# [Task T-019] Module-level state
_tasks: List[Dict] = []  # In-memory task storage
_next_id: int = 1        # Auto-increment counter


# [Task T-020] ID generation helper
def _generate_id() -> int:
    """
    Generate the next unique task ID.

    Returns:
        int: Next available ID (auto-incremented)

    Side Effects:
        Increments _next_id
    """
    global _next_id
    task_id = _next_id
    _next_id += 1
    return task_id


# [Task T-021] Add task
def add_task(title: str, description: str = "") -> Dict:
    """
    Create a new task with the given title and optional description.

    Args:
        title: Task title (must be validated before calling)
        description: Optional task description (default: empty string)

    Returns:
        Dict: The newly created task with all fields populated

    Side Effects:
        - Appends task to _tasks list
        - Increments _next_id
    """
    task = {
        "id": _generate_id(),
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now()
    }
    _tasks.append(task)
    return task


# [Task T-022] Reset state (for testing)
def reset() -> None:
    """
    Clear all tasks and reset ID counter.

    Used for testing to ensure clean state between tests.
    """
    global _tasks, _next_id
    _tasks = []
    _next_id = 1


# [Task T-026] Get all tasks
def get_all_tasks() -> List[Dict]:
    """
    Retrieve all tasks in creation order.

    Returns:
        List[Dict]: All tasks, empty list if none exist
    """
    return _tasks


# [Task T-037] Get task by ID
def get_task_by_id(task_id: int) -> Optional[Dict]:
    """
    Find a task by its ID.

    Args:
        task_id: The task ID to search for

    Returns:
        Dict: The task if found
        None: If no task with that ID exists
    """
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None


# [Task T-038] Toggle completion status
def toggle_complete(task_id: int) -> bool:
    """
    Toggle a task's completed status.

    Args:
        task_id: ID of task to toggle

    Returns:
        bool: True if task was found and toggled, False otherwise

    Side Effects:
        - Modifies task's completed field if found
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    task["completed"] = not task["completed"]
    return True


# [Task T-045] Update task
def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> bool:
    """
    Update a task's title and/or description.

    Args:
        task_id: ID of task to update
        title: New title (if provided and not None)
        description: New description (if provided and not None)

    Returns:
        bool: True if task was found and updated, False otherwise

    Side Effects:
        - Modifies task in _tasks if found
    """
    task = get_task_by_id(task_id)
    if task is None:
        return False

    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description

    return True


# [Task T-052] Delete task
def delete_task(task_id: int) -> bool:
    """
    Remove a task by its ID.

    Args:
        task_id: ID of task to delete

    Returns:
        bool: True if task was found and deleted, False otherwise

    Side Effects:
        - Removes task from _tasks if found
        - Does NOT affect _next_id (IDs are never recycled)
    """
    global _tasks
    for i, task in enumerate(_tasks):
        if task["id"] == task_id:
            _tasks.pop(i)
            return True
    return False
