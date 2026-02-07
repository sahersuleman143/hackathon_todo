# Contract: validators.py

**Module**: `src/validators.py`
**Purpose**: Input validation functions with consistent error messaging

---

## Constants

```python
# Maximum lengths (from spec)
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

# Error messages (from spec)
ERROR_EMPTY_TITLE = "Title cannot be empty. Please try again."
ERROR_TITLE_TOO_LONG = "Title exceeds maximum length of 200 characters."
ERROR_DESC_TOO_LONG = "Description exceeds maximum length of 1000 characters."
ERROR_INVALID_NUMBER = "Please enter a valid number."
```

---

## Functions

### validate_title

```python
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
        2. Must be ≤200 characters

    Example:
        >>> validate_title("Buy groceries")
        (True, "")
        >>> validate_title("")
        (False, "Title cannot be empty. Please try again.")
        >>> validate_title("x" * 201)
        (False, "Title exceeds maximum length of 200 characters.")
    """
```

**Preconditions**: None (handles any string input)

**Postconditions**:
- Returns `(True, "")` for valid titles
- Returns `(False, ERROR_EMPTY_TITLE)` for empty/whitespace
- Returns `(False, ERROR_TITLE_TOO_LONG)` for >200 chars
- Strips whitespace before checking emptiness

---

### validate_description

```python
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
        2. Must be ≤1000 characters

    Example:
        >>> validate_description("")
        (True, "")
        >>> validate_description("Some details")
        (True, "")
        >>> validate_description("x" * 1001)
        (False, "Description exceeds maximum length of 1000 characters.")
    """
```

**Preconditions**: None (handles any string input)

**Postconditions**:
- Returns `(True, "")` for valid descriptions (including empty)
- Returns `(False, ERROR_DESC_TOO_LONG)` for >1000 chars

---

### parse_int

```python
def parse_int(value: str) -> Tuple[Optional[int], str]:
    """
    Parse a string as an integer.

    Args:
        value: The string to parse

    Returns:
        Tuple[Optional[int], str]: (parsed_value, error_message)
            - (int, "") if valid integer
            - (None, error_message) if invalid

    Example:
        >>> parse_int("123")
        (123, "")
        >>> parse_int("-5")
        (-5, "")
        >>> parse_int("abc")
        (None, "Please enter a valid number.")
        >>> parse_int("12.5")
        (None, "Please enter a valid number.")
    """
```

**Preconditions**: None (handles any string input)

**Postconditions**:
- Returns `(int_value, "")` for valid integers (positive, negative, zero)
- Returns `(None, ERROR_INVALID_NUMBER)` for non-integers
- Strips whitespace before parsing

---

## Usage Pattern

```python
# In todo_app.py handlers

def handle_add():
    title = input("Enter task title: ")
    is_valid, error = validate_title(title)
    if not is_valid:
        print(error)
        return

    description = input("Enter description (optional): ")
    is_valid, error = validate_description(description)
    if not is_valid:
        print(error)
        return

    task = add_task(title, description)
    print(f"Task {task['id']} created.")


def handle_delete():
    id_input = input("Enter task ID to delete: ")
    task_id, error = parse_int(id_input)
    if task_id is None:
        print(error)
        return

    if not delete_task(task_id):
        print(f"Task with ID {task_id} not found.")
    else:
        print(f"Task {task_id} deleted.")
```

---

## Error Message Reference

| Function | Condition | Message |
|----------|-----------|---------|
| `validate_title` | Empty/whitespace | "Title cannot be empty. Please try again." |
| `validate_title` | >200 chars | "Title exceeds maximum length of 200 characters." |
| `validate_description` | >1000 chars | "Description exceeds maximum length of 1000 characters." |
| `parse_int` | Not an integer | "Please enter a valid number." |

---

## Boundary Cases

| Input | Function | Result |
|-------|----------|--------|
| `""` | `validate_title` | `(False, ERROR_EMPTY_TITLE)` |
| `"   "` | `validate_title` | `(False, ERROR_EMPTY_TITLE)` |
| `"x" * 200` | `validate_title` | `(True, "")` |
| `"x" * 201` | `validate_title` | `(False, ERROR_TITLE_TOO_LONG)` |
| `""` | `validate_description` | `(True, "")` |
| `"x" * 1000` | `validate_description` | `(True, "")` |
| `"x" * 1001` | `validate_description` | `(False, ERROR_DESC_TOO_LONG)` |
| `"0"` | `parse_int` | `(0, "")` |
| `"-1"` | `parse_int` | `(-1, "")` |
| `"  42  "` | `parse_int` | `(42, "")` |
| `"3.14"` | `parse_int` | `(None, ERROR_INVALID_NUMBER)` |
