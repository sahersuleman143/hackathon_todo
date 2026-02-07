# Contract: formatters.py

**Module**: `src/formatters.py`
**Purpose**: Display formatting functions for CLI output

---

## Constants

```python
# Display settings
DESCRIPTION_TRUNCATE_LENGTH = 50
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

# Status icons
ICON_COMPLETE = "✓"      # U+2713 CHECK MARK
ICON_INCOMPLETE = "☐"    # U+2610 BALLOT BOX

# Fallback ASCII icons (for terminals without Unicode support)
ICON_COMPLETE_ASCII = "[x]"
ICON_INCOMPLETE_ASCII = "[ ]"

# Messages
MSG_NO_TASKS = "No tasks yet"
```

---

## Functions

### format_menu

```python
def format_menu() -> str:
    """
    Generate the main menu display string.

    Returns:
        str: Multi-line menu string

    Example Output:
        === Todo Application ===
        1. Add task
        2. View tasks
        3. Update task
        4. Delete task
        5. Toggle complete
        6. Exit

        Enter your choice:
    """
```

**Preconditions**: None

**Postconditions**:
- Returns consistent menu string
- Includes all 6 options
- Ends with prompt text

---

### truncate_text

```python
def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to max_length, adding "..." if truncated.

    Args:
        text: The text to potentially truncate
        max_length: Maximum length before truncation (default: 50)

    Returns:
        str: Original text if ≤max_length, otherwise truncated with "..."

    Example:
        >>> truncate_text("Short text")
        "Short text"
        >>> truncate_text("x" * 60, max_length=50)
        "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx..."
    """
```

**Preconditions**:
- `max_length` > 3 (to allow for "...")

**Postconditions**:
- Returns original text if `len(text) <= max_length`
- Returns `text[:max_length] + "..."` if longer
- Output length is `max_length + 3` when truncated

---

### format_datetime

```python
def format_datetime(dt: datetime) -> str:
    """
    Format a datetime object for display.

    Args:
        dt: The datetime to format

    Returns:
        str: Formatted string "YYYY-MM-DD HH:MM"

    Example:
        >>> from datetime import datetime
        >>> format_datetime(datetime(2026, 1, 28, 10, 30))
        "2026-01-28 10:30"
    """
```

**Preconditions**:
- `dt` is a valid datetime object

**Postconditions**:
- Returns string in format "YYYY-MM-DD HH:MM"
- Always 16 characters

---

### get_status_icon

```python
def get_status_icon(completed: bool) -> str:
    """
    Get the status icon for a task's completion state.

    Args:
        completed: Whether the task is complete

    Returns:
        str: "✓" if complete, "☐" if incomplete

    Example:
        >>> get_status_icon(True)
        "✓"
        >>> get_status_icon(False)
        "☐"
    """
```

**Preconditions**: None

**Postconditions**:
- Returns `ICON_COMPLETE` for True
- Returns `ICON_INCOMPLETE` for False

---

### format_task

```python
def format_task(task: Dict) -> str:
    """
    Format a single task as a table row.

    Args:
        task: Task dictionary with id, title, description, completed, created_at

    Returns:
        str: Formatted row string with aligned columns

    Example:
        >>> task = {
        ...     "id": 1,
        ...     "title": "Buy groceries",
        ...     "description": "Get milk and bread",
        ...     "completed": False,
        ...     "created_at": datetime(2026, 1, 28, 10, 30)
        ... }
        >>> format_task(task)
        "1   | Buy groceries        | Get milk and bread                 | ☐      | 2026-01-28 10:30"
    """
```

**Preconditions**:
- `task` contains all required keys

**Postconditions**:
- Returns pipe-delimited row
- Description truncated if needed
- Status shown as icon

**Column Widths**:
| Column | Width | Alignment |
|--------|-------|-----------|
| ID | 4 | Left |
| Title | 20 | Left |
| Description | 36 | Left |
| Status | 6 | Center |
| Created | 16 | Left |

---

### format_task_list

```python
def format_task_list(tasks: List[Dict]) -> str:
    """
    Format all tasks as a table with header.

    Args:
        tasks: List of task dictionaries

    Returns:
        str: Complete formatted table or "No tasks yet" message

    Example Output (empty):
        No tasks yet

    Example Output (with tasks):
        ID  | Title                | Description                        | Status | Created
        ----|----------------------|------------------------------------|--------|------------------
        1   | Buy groceries        | Get milk and bread                 | ☐      | 2026-01-28 10:30
        2   | Call mom             | Wish her happy birthday            | ✓      | 2026-01-28 10:35
    """
```

**Preconditions**: None

**Postconditions**:
- Returns `MSG_NO_TASKS` if list is empty
- Returns header + separator + rows if tasks exist
- Each row formatted via `format_task`

---

## Table Format Specification

```
ID  | Title                | Description                        | Status | Created
----|----------------------|------------------------------------|--------|------------------
1   | Buy groceries        | Get milk, bread, eggs...           | ☐      | 2026-01-28 10:30
```

### Header Row
```python
HEADER = "ID  | Title                | Description                        | Status | Created"
SEPARATOR = "----|----------------------|------------------------------------|--------|------------------"
```

### Column Specifications

| Column | Header Width | Content Width | Notes |
|--------|--------------|---------------|-------|
| ID | 4 | 4 | Left-padded integers |
| Title | 20 | 20 | Left-aligned, no truncation (max 200 fits in spec) |
| Description | 36 | 50 display (truncated) | Truncate at 50, show "..." |
| Status | 6 | 1-3 | Center icon |
| Created | 16 | 16 | Fixed format |

---

## Unicode Support

Primary icons require Unicode support:
- ✓ (U+2713) - Check Mark
- ☐ (U+2610) - Ballot Box

If terminal doesn't support Unicode, use fallback:
- `[x]` for complete
- `[ ]` for incomplete

Detection can be done via environment or try/except on print.
