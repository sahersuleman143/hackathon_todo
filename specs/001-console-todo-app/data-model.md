# Data Model: Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2026-01-28
**Source**: [spec.md](./spec.md) Key Entities section

---

## Entities

### Task

The sole entity in this application, representing a unit of work to be tracked.

#### Attributes

| Attribute | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `id` | integer | Yes | Auto-generated | Unique, positive, never reused | Auto-incremented identifier starting from 1 |
| `title` | string | Yes | N/A | 1-200 characters, non-empty | Brief description of the task |
| `description` | string | No | `""` (empty string) | 0-1000 characters | Optional detailed information |
| `completed` | boolean | Yes | `False` | N/A | Indicates if task is done |
| `created_at` | datetime | Yes | Auto-set | N/A | Timestamp when task was created |

#### Dictionary Schema

```python
from datetime import datetime
from typing import TypedDict, Optional

class Task(TypedDict):
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

#### Example Instance

```python
{
    "id": 1,
    "title": "Buy groceries",
    "description": "Get milk, bread, and eggs",
    "completed": False,
    "created_at": datetime(2026, 1, 28, 10, 30, 0)
}
```

---

## Storage Structure

### Task Collection

| Property | Value |
|----------|-------|
| Type | `List[Dict]` |
| Location | Module-level variable in `task_manager.py` |
| Ordering | Insertion order (append-only) |
| Indexing | Sequential scan by ID |
| Persistence | In-memory only (lost on exit) |

```python
# In task_manager.py
_tasks: List[Dict] = []
_next_id: int = 1
```

---

## Validation Rules

### Title Validation

| Rule | Constraint | Error Message |
|------|------------|---------------|
| Non-empty | `len(title) >= 1` | "Title cannot be empty. Please try again." |
| Max length | `len(title) <= 200` | "Title exceeds maximum length of 200 characters." |
| Whitespace-only | `title.strip() != ""` | "Title cannot be empty. Please try again." |

### Description Validation

| Rule | Constraint | Error Message |
|------|------------|---------------|
| Max length | `len(description) <= 1000` | "Description exceeds maximum length of 1000 characters." |
| Empty allowed | `description == ""` | (No error - valid) |

### ID Validation

| Rule | Constraint | Error Message |
|------|------------|---------------|
| Integer format | Must parse as int | "Please enter a valid number." |
| Exists | Must be in task list | "Task with ID {id} not found." |

---

## State Transitions

### Task Lifecycle

```
                    ┌─────────────┐
                    │  CREATED    │
                    │ completed=F │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌─────────┐  ┌─────────┐  ┌─────────┐
        │ UPDATE  │  │ TOGGLE  │  │ DELETE  │
        │ title/  │  │complete │  │ removed │
        │ desc    │  │ T ↔ F   │  │ from    │
        └────┬────┘  └────┬────┘  │ storage │
             │            │       └─────────┘
             │            │
             └────────────┘
                   │
                   ▼
             ┌───────────┐
             │  ACTIVE   │
             │ (in list) │
             └───────────┘
```

### Completion Toggle

| Current State | After Toggle |
|---------------|--------------|
| `completed: False` | `completed: True` |
| `completed: True` | `completed: False` |

---

## Relationships

This application has a single entity with no relationships.

| Relationship | Description |
|--------------|-------------|
| Task → Task | None (tasks are independent) |
| Task → User | Implicit (single-user, no user entity) |

---

## Display Representation

### Task List View

| Column | Source | Max Width | Truncation |
|--------|--------|-----------|------------|
| ID | `task["id"]` | 4 chars | None |
| Title | `task["title"]` | 20 chars | None (fits constraint) |
| Description | `task["description"]` | 36 chars | Truncate at 50, show "..." |
| Status | `task["completed"]` | 6 chars | Icon: ✓ or ☐ |
| Created | `task["created_at"]` | 16 chars | Format: YYYY-MM-DD HH:MM |

### Status Icons

| State | Icon | Unicode | Fallback (ASCII) |
|-------|------|---------|------------------|
| Complete | ✓ | U+2713 | [x] |
| Incomplete | ☐ | U+2610 | [ ] |

---

## Invariants

1. **ID Uniqueness**: No two tasks share the same ID within a session
2. **ID Monotonicity**: Task IDs always increase; never recycled after deletion
3. **Title Non-null**: Every task has a non-empty title
4. **Created Immutable**: `created_at` is set once at creation, never modified
5. **Order Preservation**: Tasks appear in creation order (list append)
