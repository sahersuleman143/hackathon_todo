# Quickstart: Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2026-01-28

---

## Overview

This is a simple in-memory Python console application for task management. It provides CRUD operations through a menu-driven interface.

---

## Prerequisites

- Python 3.8 or higher
- Terminal/console with stdin/stdout support
- No external dependencies required

---

## Project Structure

```
src/
├── todo_app.py          # Entry point (run this)
├── task_manager.py      # Task CRUD operations
├── validators.py        # Input validation
└── formatters.py        # Display formatting

tests/
├── unit/
│   ├── test_task_manager.py
│   ├── test_validators.py
│   └── test_formatters.py
└── integration/
    └── test_cli_flow.py
```

---

## Running the Application

```bash
# From repository root
python src/todo_app.py

# Or make executable (Unix)
chmod +x src/todo_app.py
./src/todo_app.py
```

---

## Running Tests

```bash
# Install pytest (development only)
pip install pytest

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_task_manager.py
```

---

## Usage

### Main Menu

When you start the application, you'll see:

```
=== Todo Application ===
1. Add task
2. View tasks
3. Update task
4. Delete task
5. Toggle complete
6. Exit

Enter your choice:
```

### Operations

#### 1. Add Task
```
Enter your choice: 1
Enter task title: Buy groceries
Enter description (optional): Milk, bread, eggs

Task 1 created successfully.
```

#### 2. View Tasks
```
Enter your choice: 2

ID  | Title                | Description                        | Status | Created
----|----------------------|------------------------------------|--------|------------------
1   | Buy groceries        | Milk, bread, eggs                  | ☐      | 2026-01-28 10:30
2   | Call mom             | Birthday wishes                    | ✓      | 2026-01-28 10:35
```

#### 3. Update Task
```
Enter your choice: 3
Enter task ID to update: 1
Enter new title (or press Enter to keep current): Shopping
Enter new description (or press Enter to keep current):

Task 1 updated successfully.
```

#### 4. Delete Task
```
Enter your choice: 4
Enter task ID to delete: 2

Task 2 deleted successfully.
```

#### 5. Toggle Complete
```
Enter your choice: 5
Enter task ID to toggle: 1

Task 1 marked as complete.
```

#### 6. Exit
```
Enter your choice: 6
Goodbye!
```

You can also type `q` or `exit` to quit.

---

## Error Handling

| Error | Message |
|-------|---------|
| Empty title | "Title cannot be empty. Please try again." |
| Title too long | "Title exceeds maximum length of 200 characters." |
| Description too long | "Description exceeds maximum length of 1000 characters." |
| Invalid ID input | "Please enter a valid number." |
| Task not found | "Task with ID X not found." |
| Invalid menu choice | "Invalid choice. Please enter a number between 1-6." |

---

## Data Model

Tasks are stored as dictionaries:

```python
{
    "id": 1,                          # Auto-incremented integer
    "title": "Buy groceries",         # Required, 1-200 chars
    "description": "Milk and bread",  # Optional, max 1000 chars
    "completed": False,               # Boolean, default False
    "created_at": datetime(...)       # Auto-set on creation
}
```

---

## Constraints

- **In-memory only**: All data is lost when the application exits
- **Single user**: No concurrency support
- **No persistence**: No database or file storage
- **Python stdlib only**: No external dependencies

---

## Development Guide

### Adding a New Feature

1. Update `task_manager.py` if data operations needed
2. Add validation in `validators.py` if new input types
3. Update `formatters.py` if display changes needed
4. Update `todo_app.py` menu and handlers
5. Add tests for each modified module

### Code Style

- Use type hints where practical
- Follow PEP 8 conventions
- Keep functions small and focused
- Document with docstrings

### Testing Strategy

- **Unit tests**: Test each module in isolation
- **Integration tests**: Test CLI workflows end-to-end
- Run `pytest` before committing

---

## Troubleshooting

### Unicode Icons Not Displaying

If status icons appear as `?` or boxes:

1. Try a different terminal (PowerShell, Windows Terminal, iTerm2)
2. Modify `formatters.py` to use ASCII fallback: `[x]` / `[ ]`

### Import Errors

Ensure you're running from the repository root:

```bash
cd /path/to/hackathon2-phase1
python src/todo_app.py
```

Or add the src directory to PYTHONPATH:

```bash
export PYTHONPATH="${PYTHONPATH}:./src"
python -m todo_app
```

---

## Next Steps

After implementation:

1. Run `/sp.tasks` to generate implementation tasks
2. Follow TDD: Write tests first, then implement
3. Run tests after each module is complete
4. Manual smoke test the full workflow
