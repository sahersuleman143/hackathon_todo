# Feature Specification: Console Todo Application

**Feature Branch**: `001-console-todo-app`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "Phase I Specification - Evolution of Todo: In-memory Python console application for single-user task management with CRUD operations and completion toggling"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add a New Task (Priority: P1)

As a user, I can add a task with a title and optional description so that I can track items I need to complete.

**Why this priority**: Creating tasks is the foundational capability. Without this, no other feature has meaning.

**Independent Test**: Can be fully tested by launching the application, selecting "Add task", entering a title and description, and verifying the task is stored. Delivers immediate value by allowing users to capture tasks.

**Acceptance Scenarios**:

1. **Given** the application is running and I select "Add task", **When** I enter a valid title "Buy groceries", **Then** a new task is created with auto-assigned ID, the title is saved, completed is false, and created_at is set to current datetime.

2. **Given** the application is running and I select "Add task", **When** I enter a valid title "Call mom" with description "Wish her happy birthday", **Then** both title and description are saved to the task.

3. **Given** the application is running and I select "Add task", **When** I enter an empty title, **Then** I see "Title cannot be empty. Please try again." and am prompted to enter a valid title.

4. **Given** the application is running and I select "Add task", **When** I enter a title longer than 200 characters, **Then** I see an error message indicating the title exceeds the maximum length.

---

### User Story 2 - View All Tasks (Priority: P1)

As a user, I can see all my current tasks with their status so that I know what needs to be done.

**Why this priority**: Viewing tasks is essential to understand what work exists. Tied with adding tasks as core functionality.

**Independent Test**: Can be tested by adding a few tasks, then selecting "View tasks" and verifying all tasks display correctly with their attributes.

**Acceptance Scenarios**:

1. **Given** I have added tasks "Task A" and "Task B", **When** I select "View tasks", **Then** I see a formatted list showing ID, Title, Description (truncated if over 50 characters), Status indicator, and Created date for each task.

2. **Given** no tasks exist, **When** I select "View tasks", **Then** I see "No tasks yet" message.

3. **Given** a task is complete, **When** I view tasks, **Then** it shows a checkmark indicator for complete status.

4. **Given** a task is incomplete, **When** I view tasks, **Then** it shows an empty box indicator for incomplete status.

---

### User Story 3 - Toggle Task Completion (Priority: P2)

As a user, I can mark tasks done or undo if needed so that I can track my progress.

**Why this priority**: Marking tasks complete is the primary way to show progress. Essential after basic CRUD.

**Independent Test**: Can be tested by adding a task, toggling its completion status, and verifying the visual change in the task list.

**Acceptance Scenarios**:

1. **Given** an incomplete task with ID 1 exists, **When** I select "Toggle complete" and enter ID 1, **Then** the task's completed status becomes true.

2. **Given** a complete task with ID 1 exists, **When** I select "Toggle complete" and enter ID 1, **Then** the task's completed status becomes false.

3. **Given** I enter a non-existent task ID 99, **When** I try to toggle complete, **Then** I see "Task with ID 99 not found."

4. **Given** I enter a non-numeric value "abc", **When** I try to toggle complete, **Then** I see "Please enter a valid number."

---

### User Story 4 - Update an Existing Task (Priority: P3)

As a user, I can edit a task's title or description so that I can correct mistakes or add details.

**Why this priority**: Updating is useful but less critical than creating, viewing, or completing tasks.

**Independent Test**: Can be tested by adding a task, selecting "Update task", modifying the title or description, and verifying changes are reflected.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 and title "Old Title" exists, **When** I select "Update task", enter ID 1, and provide new title "New Title", **Then** the task's title is updated to "New Title".

2. **Given** a task with ID 1 exists, **When** I select "Update task", enter ID 1, and provide only a new description, **Then** only the description is updated while title remains unchanged.

3. **Given** I enter a non-existent task ID 99, **When** I try to update, **Then** I see "Task with ID 99 not found."

4. **Given** I try to update a task with an empty title, **When** I submit the update, **Then** I see "Title cannot be empty. Please try again."

---

### User Story 5 - Delete a Task (Priority: P3)

As a user, I can remove a task I no longer need so that my list stays clean.

**Why this priority**: Deletion is useful for list hygiene but not essential for core task tracking.

**Independent Test**: Can be tested by adding a task, selecting "Delete task", providing the ID, and verifying the task no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** I select "Delete task" and enter ID 1, **Then** the task is removed from the list.

2. **Given** tasks with IDs 1, 2, 3 exist and I delete task 2, **When** I view tasks, **Then** tasks 1 and 3 remain with their original IDs unchanged.

3. **Given** I enter a non-existent task ID 99, **When** I try to delete, **Then** I see "Task with ID 99 not found."

4. **Given** I enter a non-numeric value "abc", **When** I try to delete, **Then** I see "Please enter a valid number."

---

### User Story 6 - Navigate Menu and Exit (Priority: P2)

As a user, I can navigate a menu-driven interface and exit gracefully so that I have a clear, intuitive experience.

**Why this priority**: Menu navigation is the interaction backbone. Exit functionality ensures users can close the application cleanly.

**Independent Test**: Can be tested by launching the application, verifying menu displays, selecting various options, and exiting with 'q', 'exit', or option 6.

**Acceptance Scenarios**:

1. **Given** the application starts, **When** I see the main menu, **Then** I see options: 1. Add task, 2. View tasks, 3. Update task, 4. Delete task, 5. Toggle complete, 6. Exit.

2. **Given** the main menu is displayed, **When** I enter 'q' or 'exit', **Then** the application exits gracefully.

3. **Given** the main menu is displayed, **When** I enter an invalid option like '7' or 'abc', **Then** I see an error message and the menu is redisplayed.

4. **Given** I am in any sub-menu or prompt, **When** I complete an action, **Then** I return to the main menu.

---

### Edge Cases

- What happens when the user enters very long descriptions (over 1000 characters)? **System displays an error message indicating the description exceeds maximum length.**
- How does system handle special characters in title/description? **Special characters are allowed and preserved.**
- What happens if the task list grows very large? **In-memory list will eventually hit memory limits; this is acceptable for single-session use.**
- How does system handle rapid consecutive operations? **Operations complete sequentially; no concurrent access concerns for single-user application.**

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a task with a required title (1-200 characters) and optional description (max 1000 characters).
- **FR-002**: System MUST auto-assign a unique, incrementing integer ID to each new task starting from 1.
- **FR-003**: System MUST set completed status to false and created_at to current datetime when creating a task.
- **FR-004**: System MUST display all tasks in a formatted list showing ID, Title, truncated Description, Status indicator, and Created date.
- **FR-005**: System MUST display "No tasks yet" when viewing an empty task list.
- **FR-006**: System MUST allow users to update a task's title and/or description by ID.
- **FR-007**: System MUST allow users to delete a task by ID without affecting other task IDs.
- **FR-008**: System MUST allow users to toggle a task's completed status between true and false.
- **FR-009**: System MUST validate that title is not empty for add and update operations.
- **FR-010**: System MUST validate that task ID exists before update, delete, or toggle operations.
- **FR-011**: System MUST validate that user input for ID is a valid integer.
- **FR-012**: System MUST display a menu with numbered options and support 'q' or 'exit' to quit.
- **FR-013**: System MUST display appropriate error messages for invalid inputs and return to menu.
- **FR-014**: System MUST store all tasks in-memory only (no persistence beyond runtime).
- **FR-015**: System MUST use Python standard library only (no external dependencies).

### Key Entities

- **Task**: Represents a unit of work to be tracked.
  - `id`: Unique integer identifier (auto-incremented, starts at 1)
  - `title`: Required string (1-200 characters) describing the task
  - `description`: Optional string (max 1000 characters) with additional details
  - `completed`: Boolean indicating completion status (default: false)
  - `created_at`: Datetime when the task was created (auto-set)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 30 seconds (entering title and optional description).
- **SC-002**: Users can view their complete task list with a single menu selection.
- **SC-003**: Users can toggle task completion status in under 10 seconds (select option + enter ID).
- **SC-004**: 100% of invalid inputs result in clear, actionable error messages.
- **SC-005**: Users can exit the application at any time using 'q', 'exit', or menu option 6.
- **SC-006**: All task data persists correctly throughout a single application session.
- **SC-007**: Task IDs remain stable after deletions (no renumbering).
- **SC-008**: Application runs entirely in-memory with zero external dependencies.

## Assumptions

- Single user operating the application at a time (no concurrency).
- User has access to a terminal/console that supports standard input/output.
- Task IDs do not need to be reused after deletion (gaps in ID sequence are acceptable).
- Description truncation in view display uses 50 characters as the cutoff, showing "..." for longer descriptions.
- Created datetime display format uses a human-readable format (e.g., "2026-01-28 10:30").
- Application does not need to handle Ctrl+C gracefully beyond standard Python behavior.

## Scope Boundaries

### In Scope
- Single-user, in-memory task management
- CRUD operations (Create, Read, Update, Delete)
- Task completion toggling
- Menu-driven console interface
- Input validation and error handling

### Out of Scope
- Data persistence (database, file storage)
- Multi-user support
- Task prioritization or sorting
- Due dates or reminders
- Categories or tags
- Search or filter functionality
- Undo/redo history
- Export/import functionality
