# [Task T-005, T-006, T-007, T-008] Input validation functions
"""
validators.py - Input validation functions with consistent error messaging

Per contracts/validators.md and spec.md FR-009, FR-011
"""

from typing import Tuple, Optional


# [Task T-005] Constants from spec
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

# [Task T-005] Error messages from spec
ERROR_EMPTY_TITLE = "Title cannot be empty. Please try again."
ERROR_TITLE_TOO_LONG = "Title exceeds maximum length of 200 characters."
ERROR_DESC_TOO_LONG = "Description exceeds maximum length of 1000 characters."
ERROR_INVALID_NUMBER = "Please enter a valid number."


# [Task T-006] Validate title
def validate_title(title: str) -> Tuple[bool, str]:
    """
    Validate a task title.

    Args:
        title: The title string to validate

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
            - (True, "") if valid
            - (False, error_message) if invalid

    Validation Rules:
        1. Must not be empty or whitespace-only
        2. Must be <= 200 characters
    """
    # Strip whitespace and check for empty
    stripped = title.strip()
    if not stripped:
        return (False, ERROR_EMPTY_TITLE)

    # Check length constraint
    if len(title) > MAX_TITLE_LENGTH:
        return (False, ERROR_TITLE_TOO_LONG)

    return (True, "")


# [Task T-007] Validate description
def validate_description(description: str) -> Tuple[bool, str]:
    """
    Validate a task description.

    Args:
        description: The description string to validate

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
            - (True, "") if valid
            - (False, error_message) if invalid

    Validation Rules:
        1. May be empty (optional field)
        2. Must be <= 1000 characters
    """
    # Check length constraint only - empty is allowed
    if len(description) > MAX_DESCRIPTION_LENGTH:
        return (False, ERROR_DESC_TOO_LONG)

    return (True, "")


# [Task T-008] Parse integer
def parse_int(value: str) -> Tuple[Optional[int], str]:
    """
    Parse a string as an integer.

    Args:
        value: The string to parse

    Returns:
        Tuple[Optional[int], str]: (parsed_value, error_message)
            - (int, "") if valid integer
            - (None, error_message) if invalid
    """
    try:
        # Strip whitespace before parsing
        parsed = int(value.strip())
        return (parsed, "")
    except ValueError:
        return (None, ERROR_INVALID_NUMBER)
