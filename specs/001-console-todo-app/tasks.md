# Tasks: Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Branch**: `001-console-todo-app`
**Date**: 2026-01-28

**Tests**: Tests are included as the plan indicates Test-First approach (TDD).

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US6)
- Include exact file paths in descriptions

## Path Conventions

```text
src/
├── todo_app.py          # Main entry point + menu loop
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

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Create project structure and initialize directories

- [X] T-001 Create project directory structure: `src/` and `tests/unit/`, `tests/integration/` per plan.md "Source Code" section
- [X] T-002 [P] Create empty `src/__init__.py` to make src a Python package
- [X] T-003 [P] Create empty `tests/__init__.py`, `tests/unit/__init__.py`, `tests/integration/__init__.py`
- [X] T-004 [P] Create `requirements-dev.txt` with pytest dependency for testing

**Checkpoint**: Project skeleton ready for implementation

---

## Phase 2: Foundational (Core Modules - Blocking Prerequisites)

**Purpose**: Implement validators.py and formatters.py which ALL user stories depend on

**CRITICAL**: These modules must be complete before any user story can be implemented

### 2.1 Validators Module

**Ref**: plan.md "Module Specifications > validators.py", contracts/validators.md

- [X] T-005 [P] Create `src/validators.py` with constants: MAX_TITLE_LENGTH=200, MAX_DESCRIPTION_LENGTH=1000, and error message constants per spec.md FR-009, FR-011
- [X] T-006 Implement `validate_title(title: str) -> Tuple[bool, str]` in `src/validators.py` per contracts/validators.md
- [X] T-007 Implement `validate_description(desc: str) -> Tuple[bool, str]` in `src/validators.py` per contracts/validators.md
- [X] T-008 Implement `parse_int(value: str) -> Tuple[Optional[int], str]` in `src/validators.py` per contracts/validators.md

### 2.2 Formatters Module

**Ref**: plan.md "Module Specifications > formatters.py", contracts/formatters.md

- [X] T-009 [P] Create `src/formatters.py` with constants: DESCRIPTION_TRUNCATE_LENGTH=50, DATETIME_FORMAT, status icons per contracts/formatters.md
- [X] T-010 Implement `truncate_text(text: str, max_length: int = 50) -> str` in `src/formatters.py`
- [X] T-011 Implement `format_datetime(dt: datetime) -> str` in `src/formatters.py` returning "YYYY-MM-DD HH:MM" format
- [X] T-012 Implement `get_status_icon(completed: bool) -> str` in `src/formatters.py` returning checkmark or empty box
- [X] T-013 Implement `format_menu() -> str` in `src/formatters.py` per spec.md US6 menu options
- [X] T-014 Implement `format_task(task: Dict) -> str` in `src/formatters.py` per contracts/formatters.md column specs
- [X] T-015 Implement `format_task_list(tasks: List[Dict]) -> str` in `src/formatters.py` with header, separator, and "No tasks yet" handling

### 2.3 Foundational Unit Tests

- [X] T-016 [P] Create `tests/unit/test_validators.py` with tests: test_validate_title_valid, test_validate_title_empty, test_validate_title_too_long, test_validate_title_boundary (200 chars), test_validate_description_valid, test_validate_description_empty, test_validate_description_too_long, test_parse_int_valid, test_parse_int_invalid, test_parse_int_negative per plan.md "Test Strategy"
- [X] T-017 [P] Create `tests/unit/test_formatters.py` with tests: test_truncate_short_text, test_truncate_long_text, test_truncate_exact_length, test_format_datetime, test_get_status_icon_complete, test_get_status_icon_incomplete, test_format_task_list_empty, test_format_task_list_populated per plan.md "Test Strategy"
- [X] T-018 Run `pytest tests/unit/test_validators.py tests/unit/test_formatters.py` - verify all tests pass

**Checkpoint**: Foundation ready - validators and formatters complete and tested

---

## Phase 3: User Story 1 - Add a New Task (Priority: P1)

**Goal**: Users can add tasks with title and optional description (spec.md US1)

**Independent Test**: Launch app, select "Add task", enter title/description, verify task created with auto-ID

**Ref**: spec.md US1, FR-001, FR-002, FR-003, plan.md "task_manager.py"

### Task Manager - Add Functionality

- [X] T-019 Create `src/task_manager.py` with module state: `_tasks: List[Dict] = []` and `_next_id: int = 1` per data-model.md "Storage Structure"
- [X] T-020 [US1] Implement `_generate_id() -> int` helper in `src/task_manager.py` that returns current _next_id and increments it per plan.md "ID Generation Design"
- [X] T-021 [US1] Implement `add_task(title: str, description: str = "") -> Dict` in `src/task_manager.py` per contracts/task_manager.md - creates task with id, title, description, completed=False, created_at=datetime.now()
- [X] T-022 [US1] Implement `reset() -> None` in `src/task_manager.py` to clear _tasks and reset _next_id to 1 (for testing)

### Unit Tests for Add Task

- [X] T-023 [P] [US1] Add tests to `tests/unit/test_task_manager.py`: test_add_task_minimal, test_add_task_with_description, test_add_task_auto_id (verify sequential IDs), test_add_task_sets_created_at, test_add_task_sets_completed_false per plan.md "Test Strategy"
- [X] T-024 [US1] Run `pytest tests/unit/test_task_manager.py` - verify add_task tests pass

### CLI Handler for Add

- [X] T-025 [US1] Create `src/todo_app.py` with `handle_add()` function that: prompts for title, validates with validate_title(), prompts for description, validates with validate_description(), calls add_task(), prints success message per contracts/validators.md "Usage Pattern"

**Checkpoint**: US1 complete - users can add tasks via CLI

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

**Goal**: Users can see all tasks with status indicators (spec.md US2)

**Independent Test**: Add tasks, select "View tasks", verify formatted table with ID, Title, Description (truncated), Status icon, Created date

**Ref**: spec.md US2, FR-004, FR-005, plan.md "formatters.py"

### Task Manager - Read Functionality

- [X] T-026 [US2] Implement `get_all_tasks() -> List[Dict]` in `src/task_manager.py` per contracts/task_manager.md

### Unit Tests for View

- [X] T-027 [P] [US2] Add tests to `tests/unit/test_task_manager.py`: test_get_all_tasks_empty, test_get_all_tasks_populated (verify order preserved) per plan.md "Test Strategy"
- [X] T-028 [US2] Run `pytest tests/unit/test_task_manager.py -k "get_all"` - verify get_all_tasks tests pass

### CLI Handler for View

- [X] T-029 [US2] Implement `handle_view()` in `src/todo_app.py` that: calls get_all_tasks(), formats with format_task_list(), prints result (handles empty case) per spec.md US2 acceptance scenarios

**Checkpoint**: US2 complete - users can view all tasks with formatting

---

## Phase 5: User Story 6 - Navigate Menu and Exit (Priority: P2)

**Goal**: Users can navigate menu and exit gracefully (spec.md US6)

**Independent Test**: Launch app, verify menu displays, enter invalid choice (error + redisplay), enter 'q'/'exit'/6 (graceful exit)

**Ref**: spec.md US6, FR-012, FR-013, plan.md "CLI Flow State Machine"

### CLI Main Loop

- [X] T-030 [US6] Implement `display_menu()` in `src/todo_app.py` that prints format_menu() output
- [X] T-031 [US6] Implement `get_user_choice() -> str` in `src/todo_app.py` that reads input and returns stripped lowercase value
- [X] T-032 [US6] Implement `is_exit_command(choice: str) -> bool` in `src/todo_app.py` checking for '6', 'q', 'exit' (case-insensitive)
- [X] T-033 [US6] Implement `main()` in `src/todo_app.py` with while loop: display menu, get choice, route to handlers (1=add, 2=view), handle exit, show error for invalid choice per plan.md "CLI Flow State Machine"
- [X] T-034 [US6] Add `if __name__ == "__main__": main()` entry point to `src/todo_app.py`

### Integration Test for Menu/Exit

- [X] T-035 [P] [US6] Create `tests/integration/test_cli_flow.py` with test_exit_commands testing 'q', 'exit', '6' all exit cleanly (use unittest.mock to simulate input)
- [X] T-036 [US6] Run `pytest tests/integration/test_cli_flow.py -k "exit"` - verify exit tests pass

**Checkpoint**: US6 complete - users can navigate menu and exit; app is runnable with `python src/todo_app.py`

---

## Phase 6: User Story 3 - Toggle Task Completion (Priority: P2)

**Goal**: Users can mark tasks done/undone (spec.md US3)

**Independent Test**: Add task, toggle to complete, verify checkmark in view; toggle again, verify empty box

**Ref**: spec.md US3, FR-008, FR-010, FR-011, contracts/task_manager.md

### Task Manager - Toggle Functionality

- [X] T-037 [US3] Implement `get_task_by_id(task_id: int) -> Optional[Dict]` in `src/task_manager.py` per contracts/task_manager.md
- [X] T-038 [US3] Implement `toggle_complete(task_id: int) -> bool` in `src/task_manager.py` per contracts/task_manager.md - flips completed, returns True if found

### Unit Tests for Toggle

- [X] T-039 [P] [US3] Add tests to `tests/unit/test_task_manager.py`: test_get_task_by_id_exists, test_get_task_by_id_not_found, test_toggle_complete_false_to_true, test_toggle_complete_true_to_false, test_toggle_complete_not_found per plan.md "Test Strategy"
- [X] T-040 [US3] Run `pytest tests/unit/test_task_manager.py -k "toggle or get_task_by_id"` - verify tests pass

### CLI Handler for Toggle

- [X] T-041 [US3] Implement `handle_toggle()` in `src/todo_app.py` that: prompts for ID, parses with parse_int(), calls toggle_complete(), prints success or "Task with ID X not found." per spec.md US3 acceptance scenarios
- [X] T-042 [US3] Update `main()` in `src/todo_app.py` to route choice '5' to handle_toggle()

### Integration Test for Toggle

- [X] T-043 [P] [US3] Add test_complete_workflow to `tests/integration/test_cli_flow.py`: Add task → Toggle → View shows checkmark per plan.md "Integration Tests"
- [X] T-044 [US3] Run `pytest tests/integration/test_cli_flow.py -k "complete_workflow"` - verify test passes

**Checkpoint**: US3 complete - users can toggle task completion status

---

## Phase 7: User Story 4 - Update an Existing Task (Priority: P3)

**Goal**: Users can edit task title/description (spec.md US4)

**Independent Test**: Add task, select update, change title, verify change in view

**Ref**: spec.md US4, FR-006, FR-009, FR-010, contracts/task_manager.md

### Task Manager - Update Functionality

- [X] T-045 [US4] Implement `update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool` in `src/task_manager.py` per contracts/task_manager.md - only updates non-None fields

### Unit Tests for Update

- [X] T-046 [P] [US4] Add tests to `tests/unit/test_task_manager.py`: test_update_task_title, test_update_task_description, test_update_task_both, test_update_task_not_found, test_update_task_keeps_other_fields per plan.md "Test Strategy"
- [X] T-047 [US4] Run `pytest tests/unit/test_task_manager.py -k "update"` - verify tests pass

### CLI Handler for Update

- [X] T-048 [US4] Implement `handle_update()` in `src/todo_app.py` that: prompts for ID, parses with parse_int(), gets task with get_task_by_id(), shows current values, prompts for new title (Enter to keep), prompts for new description (Enter to keep), validates inputs, calls update_task(), prints result per spec.md US4 acceptance scenarios
- [X] T-049 [US4] Update `main()` in `src/todo_app.py` to route choice '3' to handle_update()

### Integration Test for Update

- [X] T-050 [P] [US4] Add test_update_flow to `tests/integration/test_cli_flow.py`: Add → Update title → View shows change per plan.md "Integration Tests"
- [X] T-051 [US4] Run `pytest tests/integration/test_cli_flow.py -k "update"` - verify test passes

**Checkpoint**: US4 complete - users can update task title/description

---

## Phase 8: User Story 5 - Delete a Task (Priority: P3)

**Goal**: Users can remove tasks (spec.md US5)

**Independent Test**: Add tasks 1,2,3, delete task 2, verify tasks 1 and 3 remain with original IDs

**Ref**: spec.md US5, FR-007, FR-010, FR-011, SC-007, contracts/task_manager.md

### Task Manager - Delete Functionality

- [X] T-052 [US5] Implement `delete_task(task_id: int) -> bool` in `src/task_manager.py` per contracts/task_manager.md - removes task, does NOT recycle ID

### Unit Tests for Delete

- [X] T-053 [P] [US5] Add tests to `tests/unit/test_task_manager.py`: test_delete_task_exists, test_delete_task_not_found, test_delete_preserves_other_ids (verify IDs don't change after deletion) per plan.md "Test Strategy"
- [X] T-054 [US5] Run `pytest tests/unit/test_task_manager.py -k "delete"` - verify tests pass

### CLI Handler for Delete

- [X] T-055 [US5] Implement `handle_delete()` in `src/todo_app.py` that: prompts for ID, parses with parse_int(), calls delete_task(), prints success or "Task with ID X not found." per spec.md US5 acceptance scenarios
- [X] T-056 [US5] Update `main()` in `src/todo_app.py` to route choice '4' to handle_delete()

### Integration Test for Delete

- [X] T-057 [P] [US5] Add test_delete_flow to `tests/integration/test_cli_flow.py`: Add → Delete → View shows removed per plan.md "Integration Tests"
- [X] T-058 [US5] Run `pytest tests/integration/test_cli_flow.py -k "delete"` - verify test passes

**Checkpoint**: US5 complete - users can delete tasks; IDs remain stable

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [X] T-059 Add test_invalid_input_recovery to `tests/integration/test_cli_flow.py`: Bad input → Error message → Menu redisplayed per plan.md "Integration Tests"
- [X] T-060 Add test_add_and_view_flow to `tests/integration/test_cli_flow.py`: Add task → View shows task with correct format per plan.md "Integration Tests"
- [X] T-061 Run full test suite: `pytest tests/ -v` - verify all 30+ tests pass
- [X] T-062 Manual smoke test: Run `python src/todo_app.py` and execute full workflow (add, view, toggle, update, delete, exit) per quickstart.md
- [X] T-063 Verify all error messages match spec.md exactly: "Title cannot be empty...", "Please enter a valid number.", "Task with ID X not found." per spec.md "Error Handling & Edge Cases"
- [X] T-064 Code cleanup: Remove any debug prints, ensure consistent code style, add docstrings to public functions per plan.md "Definition of Done"

**Checkpoint**: Feature complete - all tests pass, manual validation successful

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (validators.py, formatters.py) - BLOCKS ALL USER STORIES
    ↓
    ├── Phase 3: US1 - Add Task (P1)
    │       ↓
    ├── Phase 4: US2 - View Tasks (P1) [depends on US1 for meaningful test]
    │       ↓
    ├── Phase 5: US6 - Menu/Exit (P2) [depends on US1, US2 handlers]
    │       ↓
    ├── Phase 6: US3 - Toggle (P2)
    │       ↓
    ├── Phase 7: US4 - Update (P3)
    │       ↓
    └── Phase 8: US5 - Delete (P3)
            ↓
      Phase 9: Polish
```

### User Story Dependencies

| Story | Can Start After | Notes |
|-------|-----------------|-------|
| US1 (Add) | Phase 2 | First story to implement |
| US2 (View) | US1 | Needs tasks to view |
| US6 (Menu) | US1, US2 | Needs handlers to route to |
| US3 (Toggle) | Phase 2 | Independent of US1/US2 for logic |
| US4 (Update) | Phase 2 | Independent of US1/US2 for logic |
| US5 (Delete) | Phase 2 | Independent of US1/US2 for logic |

### Within Each User Story

1. Task Manager functions first
2. Unit tests second
3. CLI handler third
4. Integration tests fourth

### Parallel Opportunities by Phase

**Phase 1 (Setup)**:
```
T-002, T-003, T-004 can run in parallel (different files)
```

**Phase 2 (Foundational)**:
```
T-005, T-009 can run in parallel (validators.py vs formatters.py)
T-016, T-017 can run in parallel (different test files)
```

**Each User Story**:
```
Unit test creation tasks marked [P] can run in parallel within a story
```

---

## Parallel Example: Phase 2 Foundational

```bash
# These can be executed simultaneously:
Task: T-005 "Create src/validators.py with constants"
Task: T-009 "Create src/formatters.py with constants"

# After constants, these can be parallelized:
Task: T-016 "Create tests/unit/test_validators.py"
Task: T-017 "Create tests/unit/test_formatters.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 + 6 Only)

1. Complete Phase 1: Setup (T-001 to T-004)
2. Complete Phase 2: Foundational (T-005 to T-018)
3. Complete Phase 3: US1 - Add Task (T-019 to T-025)
4. Complete Phase 4: US2 - View Tasks (T-026 to T-029)
5. Complete Phase 5: US6 - Menu/Exit (T-030 to T-036)
6. **STOP and VALIDATE**: Test MVP independently
   - Can add tasks
   - Can view tasks
   - Can exit cleanly
7. Deploy/demo if ready

### Incremental Delivery

1. MVP (US1 + US2 + US6) → Runnable app with add/view/exit
2. Add US3 (Toggle) → Users can mark tasks complete
3. Add US4 (Update) → Users can edit tasks
4. Add US5 (Delete) → Users can remove tasks
5. Each increment is independently testable

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 64 |
| Phase 1 (Setup) | 4 |
| Phase 2 (Foundational) | 14 |
| Phase 3 (US1 - Add) | 7 |
| Phase 4 (US2 - View) | 4 |
| Phase 5 (US6 - Menu) | 7 |
| Phase 6 (US3 - Toggle) | 8 |
| Phase 7 (US4 - Update) | 7 |
| Phase 8 (US5 - Delete) | 7 |
| Phase 9 (Polish) | 6 |
| Parallelizable Tasks | 18 |
| Unit Tests | ~30 |
| Integration Tests | 6 |

---

## Notes

- [P] tasks = different files, no dependencies
- [USx] label maps task to user story for traceability
- Each user story independently completable and testable
- Verify tests exist and pass before moving to next phase
- Commit after each task or logical group
- Error messages MUST match spec.md exactly
