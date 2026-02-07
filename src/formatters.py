# [Task T-009 to T-015] Display formatting functions
"""
formatters.py - Display formatting functions for CLI output

Per contracts/formatters.md and spec.md US6
"""

from datetime import datetime
from typing import Dict, List


# [Task T-009] Constants
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


# [Task T-010] Truncate text
def truncate_text(text: str, max_length: int = 50) -> str:
    """
    Truncate text to max_length, adding "..." if truncated.

    Args:
        text: The text to potentially truncate
        max_length: Maximum length before truncation (default: 50)

    Returns:
        str: Original text if <= max_length, otherwise truncated with "..."
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


# [Task T-011] Format datetime
def format_datetime(dt: datetime) -> str:
    """
    Format a datetime object for display.

    Args:
        dt: The datetime to format

    Returns:
        str: Formatted string "YYYY-MM-DD HH:MM"
    """
    return dt.strftime(DATETIME_FORMAT)


# [Task T-012] Get status icon
def get_status_icon(completed: bool, use_ascii: bool = False) -> str:
    """
    Get the status icon for a task's completion state.

    Args:
        completed: Whether the task is complete
        use_ascii: Use ASCII fallback icons (default: False)

    Returns:
        str: checkmark if complete, empty box if incomplete
    """
    if use_ascii:
        return ICON_COMPLETE_ASCII if completed else ICON_INCOMPLETE_ASCII
    return ICON_COMPLETE if completed else ICON_INCOMPLETE


def _can_display_unicode() -> bool:
    """Check if terminal can display Unicode characters."""
    import sys
    try:
        # Test if stdout can encode Unicode
        sys.stdout.encoding
        '\u2713'.encode(sys.stdout.encoding or 'utf-8')
        return True
    except (UnicodeEncodeError, LookupError):
        return False


# Auto-detect Unicode support
USE_ASCII_ICONS = not _can_display_unicode()


# [Task T-013] Format menu
def format_menu() -> str:
    """
    Generate the main menu display string.

    Returns:
        str: Multi-line menu string
    """
    return """
=== Todo Application ===
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Toggle complete
6. Exit

Enter your choice: """


# [Task T-014] Format single task
def format_task(task: Dict) -> str:
    """
    Format a single task as a table row.

    Args:
        task: Task dictionary with id, title, description, completed, created_at

    Returns:
        str: Formatted row string with aligned columns

    Column Widths:
        ID: 4, Title: 20, Description: 36, Status: 6, Created: 16
    """
    task_id = str(task["id"]).ljust(4)
    title = task["title"][:20].ljust(20)
    description = truncate_text(task["description"], 36).ljust(36)
    status = get_status_icon(task["completed"], USE_ASCII_ICONS).center(6)
    created = format_datetime(task["created_at"]).ljust(16)

    return f"{task_id}| {title}| {description}| {status}| {created}"


# [Task T-015] Format task list
def format_task_list(tasks: List[Dict]) -> str:
    """
    Format the complete task list with header.

    Args:
        tasks: List of task dictionaries

    Returns:
        str: Formatted table or "No tasks yet" message
    """
    if not tasks:
        return MSG_NO_TASKS

    # Header
    header = "ID  | Title               | Description                          | Status | Created"
    separator = "-" * len(header)

    # Format each task
    rows = [format_task(task) for task in tasks]

    return "\n".join([header, separator] + rows)
