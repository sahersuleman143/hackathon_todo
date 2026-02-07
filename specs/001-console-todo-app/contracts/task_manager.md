# Contract: task_manager.py

**Module**: `src/task_manager.py`
**Purpose**: CRUD operations for task management with in-memory storage

---

## Module State

```python
_tasks: List[Dict] = []  # In-memory task storage
_next_id: int = 1        # Auto-increment counter
```

---

## Functions

### add_task

```python
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

    Example:
        >>> task = add_task("Buy groceries", "Milk, bread, eggs")
        >>> task["id"]
        1
        >>> task["completed"]
        False
    """
```

**Preconditions**:
- `title` is non-empty and ≤200 characters (caller validates)
- `description` is ≤1000 characters (caller validates)

**Postconditions**:
- Returns task dict with `id`, `title`, `description`, `completed=False`, `created_at`
- Task is appended to `_tasks`
- `_next_id` is incremented by 1

---

### get_all_tasks

```python
def get_all_tasks() -> List[Dict]:
    """
    Retrieve all tasks in creation order.

    Returns:
        List[Dict]: All tasks, empty list if none exist

    Side Effects:
        None (read-only)

    Example:
        >>> tasks = get_all_tasks()
        >>> len(tasks)
        0
    """
```

**Preconditions**: None

**Postconditions**:
- Returns reference to `_tasks` (or copy if immutability desired)
- Order matches creation order

---

### get_task_by_id

```python
def get_task_by_id(task_id: int) -> Optional[Dict]:
    """
    Find a task by its ID.

    Args:
        task_id: The task ID to search for

    Returns:
        Dict: The task if found
        None: If no task with that ID exists

    Side Effects:
        None (read-only)

    Example:
        >>> task = get_task_by_id(1)
        >>> task["title"] if task else "Not found"
        "Buy groceries"
    """
```

**Preconditions**:
- `task_id` is a valid integer

**Postconditions**:
- Returns task dict if found, None otherwise
- Does not modify state

---

### update_task

```python
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

    Example:
        >>> update_task(1, title="Updated title")
        True
        >>> update_task(999, title="No such task")
        False
    """
```

**Preconditions**:
- `task_id` is a valid integer
- `title` (if provided) is validated by caller
- `description` (if provided) is validated by caller

**Postconditions**:
- If task exists: Updates provided fields, returns True
- If task not found: Returns False, no state change
- Only non-None parameters are updated

---

### delete_task

```python
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

    Example:
        >>> delete_task(1)
        True
        >>> delete_task(1)  # Already deleted
        False
    """
```

**Preconditions**:
- `task_id` is a valid integer

**Postconditions**:
- If task exists: Removed from `_tasks`, returns True
- If task not found: Returns False, no state change
- Other task IDs remain unchanged

---

### toggle_complete

```python
def toggle_complete(task_id: int) -> bool:
    """
    Toggle a task's completed status.

    Args:
        task_id: ID of task to toggle

    Returns:
        bool: True if task was found and toggled, False otherwise

    Side Effects:
        - Flips task["completed"] between True and False

    Example:
        >>> toggle_complete(1)  # False -> True
        True
        >>> toggle_complete(1)  # True -> False
        True
        >>> toggle_complete(999)  # Not found
        False
    """
```

**Preconditions**:
- `task_id` is a valid integer

**Postconditions**:
- If task exists: `completed` flipped, returns True
- If task not found: Returns False, no state change

---

### reset

```python
def reset() -> None:
    """
    Clear all tasks and reset ID counter. For testing only.

    Side Effects:
        - Clears _tasks list
        - Resets _next_id to 1

    Example:
        >>> reset()
        >>> len(get_all_tasks())
        0
    """
```

**Preconditions**: None

**Postconditions**:
- `_tasks` is empty
- `_next_id` is 1

---

## Error Handling

All functions follow these conventions:

| Condition | Behavior |
|-----------|----------|
| Task not found | Return `False` or `None` (no exception) |
| Invalid arguments | Caller responsibility to validate |
| State corruption | Not applicable (simple list operations) |

---

## Thread Safety

Not thread-safe. Single-user, single-threaded access assumed.
