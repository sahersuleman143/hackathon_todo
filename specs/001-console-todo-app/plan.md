# Implementation Plan: Console Todo Application

**Branch**: `001-console-todo-app` | **Date**: 2026-01-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo-app/spec.md`

## Summary

Build an in-memory Python console application for single-user task management. The application provides CRUD operations (Create, Read, Update, Delete) and task completion toggling through a menu-driven CLI interface. Uses Python standard library only with no external dependencies or data persistence.

## Technical Context

**Language/Version**: Python 3.8+ (standard library only, per FR-015)
**Primary Dependencies**: None (stdlib only: `datetime` for timestamps)
**Storage**: In-memory list of dictionaries (no persistence, per FR-014)
**Testing**: pytest (stdlib `unittest` as fallback)
**Target Platform**: Any system with Python 3.8+ and terminal access
**Project Type**: Single CLI application
**Performance Goals**: Instant response (<100ms) for all operations
**Constraints**: No external dependencies, no file I/O, single-user only
**Scale/Scope**: Unlimited tasks within available memory, single session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Simplicity | PASS | Single module, no over-engineering, minimal abstractions |
| Test-First | PASS | Unit tests planned for all functions before implementation |
| Library-First | N/A | Single application, not a reusable library |
| CLI Interface | PASS | Menu-driven stdin/stdout interface |
| No External Deps | PASS | Python stdlib only (FR-015) |

**Gate Status**: PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-console-todo-app/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (internal function contracts)
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── todo_app.py          # Main application entry point + menu loop
├── task_manager.py      # Task CRUD operations and data storage
├── validators.py        # Input validation functions
└── formatters.py        # Display formatting functions

tests/
├── unit/
│   ├── test_task_manager.py
│   ├── test_validators.py
│   └── test_formatters.py
└── integration/
    └── test_cli_flow.py
```

**Structure Decision**: Single project with modular separation. Four source modules to maintain separation of concerns while keeping the codebase simple. Tests organized by type (unit vs integration).

## Complexity Tracking

No constitution violations detected. Design follows simplicity principles.

---

## Architecture Overview

### High-Level Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      todo_app.py                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   main()                             │   │
│  │  • Display menu                                      │   │
│  │  • Route user input to handlers                      │   │
│  │  • Loop until exit                                   │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │ calls
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   task_manager.py                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  TaskManager (class or module-level functions)       │   │
│  │  • _tasks: List[Dict]      # In-memory storage       │   │
│  │  • _next_id: int           # ID counter              │   │
│  │  ├── add_task(title, description) → Task             │   │
│  │  ├── get_all_tasks() → List[Task]                    │   │
│  │  ├── get_task_by_id(id) → Task | None                │   │
│  │  ├── update_task(id, title, description) → bool      │   │
│  │  ├── delete_task(id) → bool                          │   │
│  │  └── toggle_complete(id) → bool                      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────┘
                      │ uses
          ┌───────────┴───────────┐
          ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  validators.py   │    │  formatters.py   │
│  ───────────────  │    │  ───────────────  │
│  validate_title() │    │  format_task()    │
│  validate_desc()  │    │  format_task_list│
│  validate_id()    │    │  format_menu()    │
│  parse_int()      │    │  truncate_text()  │
└──────────────────┘    └──────────────────┘
```

### CLI Flow State Machine

```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                           ▼
              ┌────────────────────────┐
              │    DISPLAY MENU        │◄─────────────────┐
              │  1. Add task           │                  │
              │  2. View tasks         │                  │
              │  3. Update task        │                  │
              │  4. Delete task        │                  │
              │  5. Toggle complete    │                  │
              │  6. Exit               │                  │
              └───────────┬────────────┘                  │
                          │                               │
                          ▼                               │
              ┌────────────────────────┐                  │
              │   GET USER INPUT       │                  │
              └───────────┬────────────┘                  │
                          │                               │
        ┌─────────────────┼─────────────────┐             │
        │      │      │       │      │      │             │
        ▼      ▼      ▼       ▼      ▼      ▼             │
     ┌────┐┌────┐┌────┐  ┌────┐┌────┐┌──────────┐        │
     │ 1  ││ 2  ││ 3  │  │ 4  ││ 5  ││6/q/exit  │        │
     │ADD ││VIEW││UPD │  │DEL ││TOG ││  EXIT    │        │
     └─┬──┘└─┬──┘└─┬──┘  └─┬──┘└─┬──┘└────┬─────┘        │
       │     │     │       │     │        │              │
       │     │     │       │     │        ▼              │
       │     │     │       │     │   ┌─────────┐         │
       │     │     │       │     │   │  END    │         │
       │     │     │       │     │   └─────────┘         │
       │     │     │       │     │                       │
       ▼     ▼     ▼       ▼     ▼                       │
     ┌─────────────────────────────────────────┐         │
     │         EXECUTE OPERATION               │         │
     │   • Validate input                      │         │
     │   • Perform action / Show error         │         │
     │   • Display result                      │         │
     └────────────────────┬────────────────────┘         │
                          │                              │
                          └──────────────────────────────┘
```

---

## In-Memory Data Structure

### Task Dictionary Schema

```python
task = {
    "id": int,              # Auto-incremented, starts at 1, never reused
    "title": str,           # 1-200 characters, required
    "description": str,     # 0-1000 characters, optional (empty string if not provided)
    "completed": bool,      # Default: False
    "created_at": datetime  # Auto-set on creation
}
```

### Storage Design

```python
# Module-level state in task_manager.py
_tasks: List[Dict] = []     # Ordered list of task dictionaries
_next_id: int = 1           # Monotonically increasing counter

# ID Generation Strategy:
# - Increment _next_id BEFORE assignment (ensures uniqueness)
# - Never decrement or recycle IDs after deletion
# - ID 1 is always the first task created in a session
```

### Lookup Strategy

```python
# Find by ID: O(n) linear scan (acceptable for in-memory, single-user)
def get_task_by_id(task_id: int) -> Optional[Dict]:
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None
```

---

## Module Specifications

### 1. validators.py

| Function | Input | Output | Validation Rules |
|----------|-------|--------|------------------|
| `validate_title(title: str)` | string | `(bool, str)` | Non-empty, 1-200 chars |
| `validate_description(desc: str)` | string | `(bool, str)` | Max 1000 chars, empty allowed |
| `parse_int(value: str)` | string | `(int, str) or (None, str)` | Must be valid integer |

**Error Messages** (per spec):
- Empty title: `"Title cannot be empty. Please try again."`
- Title too long: `"Title exceeds maximum length of 200 characters."`
- Description too long: `"Description exceeds maximum length of 1000 characters."`
- Invalid ID: `"Please enter a valid number."`

### 2. task_manager.py

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `add_task(title, description="")` | str, str | Dict | Creates task, returns it |
| `get_all_tasks()` | - | List[Dict] | Returns all tasks |
| `get_task_by_id(task_id)` | int | Dict or None | Find task by ID |
| `update_task(task_id, title=None, description=None)` | int, str?, str? | bool | Update fields, returns success |
| `delete_task(task_id)` | int | bool | Remove task, returns success |
| `toggle_complete(task_id)` | int | bool | Flip completed flag, returns success |
| `reset()` | - | None | Clear all tasks (for testing) |

**Error Handling**: Functions return `False` or `None` on failure; callers handle messaging.

### 3. formatters.py

| Function | Input | Output | Description |
|----------|-------|--------|-------------|
| `format_menu()` | - | str | Returns menu string |
| `format_task(task)` | Dict | str | Single task formatted line |
| `format_task_list(tasks)` | List[Dict] | str | Full task list with headers |
| `truncate_text(text, max_len=50)` | str, int | str | Truncate with "..." |
| `format_datetime(dt)` | datetime | str | "YYYY-MM-DD HH:MM" format |
| `get_status_icon(completed)` | bool | str | Returns "✓" or "☐" |

**Display Format** (per spec):
```
ID  | Title                | Description                        | Status | Created
----|----------------------|------------------------------------|--------|------------------
1   | Buy groceries        | Get milk, bread, eggs...           | ☐      | 2026-01-28 10:30
2   | Call mom             | Wish her happy birthday            | ✓      | 2026-01-28 10:35
```

### 4. todo_app.py

| Function | Description |
|----------|-------------|
| `main()` | Entry point, runs menu loop |
| `display_menu()` | Print menu options |
| `handle_add()` | Prompt for title/desc, validate, add |
| `handle_view()` | Display all tasks or empty message |
| `handle_update()` | Prompt for ID, validate, prompt for new values |
| `handle_delete()` | Prompt for ID, validate, delete |
| `handle_toggle()` | Prompt for ID, validate, toggle |
| `get_user_choice()` | Read and validate menu selection |

**Exit Handling**: Check for '6', 'q', 'exit' (case-insensitive).

---

## Error Handling Strategy

### Error Categories and Responses

| Category | Trigger | Response | Return to |
|----------|---------|----------|-----------|
| Empty title | Title validation fails | Show error, re-prompt | Same operation |
| Title too long | >200 chars | Show error, re-prompt | Same operation |
| Description too long | >1000 chars | Show error, re-prompt | Same operation |
| Invalid ID format | Non-integer input | "Please enter a valid number." | Main menu |
| ID not found | Task doesn't exist | "Task with ID X not found." | Main menu |
| Invalid menu choice | Out of range or non-numeric | Show error, redisplay menu | Main menu |
| Empty task list | View/Update/Delete/Toggle with no tasks | "No tasks yet" or graceful message | Main menu |

### Error Message Constants

```python
ERROR_EMPTY_TITLE = "Title cannot be empty. Please try again."
ERROR_TITLE_TOO_LONG = "Title exceeds maximum length of 200 characters."
ERROR_DESC_TOO_LONG = "Description exceeds maximum length of 1000 characters."
ERROR_INVALID_NUMBER = "Please enter a valid number."
ERROR_TASK_NOT_FOUND = "Task with ID {id} not found."
ERROR_INVALID_CHOICE = "Invalid choice. Please enter a number between 1-6."
MSG_NO_TASKS = "No tasks yet"
```

---

## ID Generation Design

### Requirements
- Auto-increment starting from 1 (FR-002)
- IDs never reused after deletion (SC-007)
- Unique within session

### Implementation

```python
# In task_manager.py
_next_id: int = 1

def _generate_id() -> int:
    global _next_id
    task_id = _next_id
    _next_id += 1
    return task_id
```

### ID Lifecycle Example

```
Action              | _next_id (before) | Assigned ID | _next_id (after)
--------------------|-------------------|-------------|------------------
Add "Task A"        | 1                 | 1           | 2
Add "Task B"        | 2                 | 2           | 3
Add "Task C"        | 3                 | 3           | 4
Delete Task 2       | 4                 | -           | 4 (unchanged)
Add "Task D"        | 4                 | 4           | 5
View tasks          | Shows: 1, 3, 4 (gap at 2 is expected)
```

---

## Test Strategy

### Unit Tests (per module)

**test_validators.py**:
- `test_validate_title_valid`: Normal title passes
- `test_validate_title_empty`: Empty string fails with correct message
- `test_validate_title_too_long`: 201+ chars fails
- `test_validate_title_boundary`: Exactly 200 chars passes
- `test_validate_description_valid`: Normal description passes
- `test_validate_description_empty`: Empty string passes
- `test_validate_description_too_long`: 1001+ chars fails
- `test_parse_int_valid`: "123" returns (123, "")
- `test_parse_int_invalid`: "abc" returns (None, error)
- `test_parse_int_negative`: "-1" returns (-1, "") (valid integer)

**test_task_manager.py**:
- `test_add_task_minimal`: Title only
- `test_add_task_with_description`: Title + description
- `test_add_task_auto_id`: IDs increment correctly
- `test_get_all_tasks_empty`: Returns empty list
- `test_get_all_tasks_populated`: Returns all tasks
- `test_get_task_by_id_exists`: Returns correct task
- `test_get_task_by_id_not_found`: Returns None
- `test_update_task_title`: Title updated
- `test_update_task_description`: Description updated
- `test_update_task_not_found`: Returns False
- `test_delete_task_exists`: Task removed, returns True
- `test_delete_task_not_found`: Returns False
- `test_delete_preserves_other_ids`: Other task IDs unchanged
- `test_toggle_complete_false_to_true`: Flips to True
- `test_toggle_complete_true_to_false`: Flips to False
- `test_toggle_complete_not_found`: Returns False

**test_formatters.py**:
- `test_truncate_short_text`: No truncation needed
- `test_truncate_long_text`: Adds "..."
- `test_truncate_exact_length`: No truncation at boundary
- `test_format_datetime`: Correct format
- `test_get_status_icon_complete`: Returns "✓"
- `test_get_status_icon_incomplete`: Returns "☐"
- `test_format_task_list_empty`: Shows "No tasks yet"
- `test_format_task_list_populated`: Correct table format

### Integration Tests

**test_cli_flow.py**:
- `test_add_and_view_flow`: Add task, verify in view
- `test_complete_workflow`: Add → Toggle → View shows ✓
- `test_update_flow`: Add → Update → View shows changes
- `test_delete_flow`: Add → Delete → View shows removed
- `test_invalid_input_recovery`: Bad input → Error → Menu redisplayed
- `test_exit_commands`: 'q', 'exit', '6' all exit cleanly

---

## Implementation Order

### Phase 1: Core Data Layer
1. `validators.py` - Input validation functions
2. `task_manager.py` - CRUD operations

### Phase 2: Display Layer
3. `formatters.py` - Output formatting

### Phase 3: Integration
4. `todo_app.py` - CLI menu and handlers

### Phase 4: Testing
5. Unit tests for each module
6. Integration tests for CLI flow

---

## Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Unicode display issues | Low | Low | Use ASCII fallback for status icons if needed |
| Memory exhaustion | Very Low | Low | Document as expected for very large task counts |
| Input encoding issues | Low | Medium | Use `input()` which handles encoding |
| Ctrl+C crash | Low | Low | Acceptable per spec assumptions |

---

## Definition of Done

- [ ] All source modules implemented
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] No external dependencies used
- [ ] Menu displays correctly
- [ ] All error messages match spec
- [ ] ID generation never reuses IDs
- [ ] Manual smoke test passes
