---
id: 0002
title: Revert Urdu to English messages
stage: refactor
date: 2026-01-29
surface: agent
model: claude-sonnet-4-5
feature: 001-console-todo-app
branch: 001-console-todo-app
user: wajiz.pk
command: /sp.implement
labels: ["refactor", "localization", "revert", "english"]
links:
  spec: specs/001-console-todo-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/validators.py
  - src/formatters.py
  - src/todo_app.py
  - tests/integration/test_cli_flow.py
tests:
  - tests/unit/test_validators.py (16 tests)
  - tests/unit/test_formatters.py (11 tests)
  - tests/unit/test_task_manager.py (20 tests)
  - tests/integration/test_cli_flow.py (14 tests)
---

## Prompt

Revert all Urdu messages back to original English in todo_app.py, validators.py, and formatters.py.

Restore all prompts, error messages, success messages, menu options to their English versions as they were before the Urdu update.

Examples:

- "ٹاسک کا عنوان درج کریں: " → "Enter task title: "

- "عنوان خالی نہیں ہو سکتا۔" → "Title cannot be empty. Please try again."

- "ٹاسک کامیابی سے بنایا گیا۔" → "Task {id} created successfully."

- "اللہ حافظ!" → "Goodbye!"

- Menu back to "Add task", "View tasks", etc.

Keep English as default, remove any Urdu-specific code or comments.

No breaking changes, keep all logic intact.

## Response snapshot

Reverted all Urdu messages back to English in:

**Files Modified:**
- `src/validators.py`: Error messages restored to English
- `src/formatters.py`: Menu and MSG_NO_TASKS restored to English
- `src/todo_app.py`: All prompts and messages restored to English
- `tests/integration/test_cli_flow.py`: Test assertions updated to check for English messages

**Messages Restored:**
- Error messages: "Title cannot be empty.", "Please enter a valid number.", etc.
- Menu: "Add task", "View tasks", "Update task", "Delete task", "Toggle complete", "Exit"
- Prompts: "Enter task title:", "Enter description (optional):", etc.
- Status messages: "Task {id} created successfully.", "Goodbye!", etc.

**Test Results:** 61/61 tests passed

## Outcome

- ✅ Impact: All user-facing messages reverted to English
- 🧪 Tests: 61/61 passed (100% pass rate)
- 📁 Files: 4 files modified
- 🔁 Next prompts: Ready for next feature or commit
- 🧠 Reflection: Clean revert preserving all logic and functionality

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): pytest 61/61 PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - revert complete
