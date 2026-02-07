#!/usr/bin/env python3
# [Task T-025, T-029 to T-034, T-041-T-042, T-048-T-049, T-055-T-056] Main CLI application
"""
todo_app.py - Main application entry point + menu loop

Per spec.md US1-US6 and plan.md "CLI Flow State Machine"
"""

from validators import validate_title, validate_description, parse_int
from formatters import format_menu, format_task_list
from task_manager import (
    add_task, get_all_tasks, get_task_by_id,
    update_task, delete_task, toggle_complete
)


# [Task T-030] Display menu
def display_menu() -> None:
    """Print the main menu"""
    print(format_menu(), end="")


# [Task T-031] Get user choice
def get_user_choice() -> str:
    """
    Read user input and return stripped lowercase value.

    Returns:
        str: User input, stripped and lowercased
    """
    try:
        return input().strip().lower()
    except EOFError:
        return "exit"


# [Task T-032] Check exit command
def is_exit_command(choice: str) -> bool:
    """
    Check if choice is an exit command.

    Args:
        choice: User's menu choice (already lowercased)

    Returns:
        bool: True if exit command, False otherwise
    """
    return choice in ('6', 'q', 'exit')


# [Task T-025] Handle add task (US1)
def handle_add() -> None:
    """
    Handle the 'Add task' menu option.

    Prompts for title, validates, prompts for description,
    validates, creates task, prints success message.
    """
    print("\n--- Add New Task ---")

    # Get and validate title
    title = input("Enter task title: ")
    is_valid, error = validate_title(title)
    if not is_valid:
        print(error)
        return

    # Get and validate description
    description = input("Enter description (optional, press Enter to skip): ")
    is_valid, error = validate_description(description)
    if not is_valid:
        print(error)
        return

    # Create task
    task = add_task(title.strip(), description)
    print(f"Task {task['id']} created successfully.")


# [Task T-029] Handle view tasks (US2)
def handle_view() -> None:
    """
    Handle the 'View tasks' menu option.

    Displays all tasks in formatted table or 'No tasks yet' message.
    """
    print("\n--- All Tasks ---")
    tasks = get_all_tasks()
    print(format_task_list(tasks))


# [Task T-041] Handle toggle complete (US3)
def handle_toggle() -> None:
    """
    Handle the 'Toggle complete' menu option.

    Prompts for ID, parses, toggles completion status,
    prints success or not found message.
    """
    print("\n--- Toggle Task Completion ---")

    id_input = input("Enter task ID to toggle: ")
    task_id, error = parse_int(id_input)
    if task_id is None:
        print(error)
        return

    if toggle_complete(task_id):
        task = get_task_by_id(task_id)
        status = "complete" if task["completed"] else "incomplete"
        print(f"Task {task_id} marked as {status}.")
    else:
        print(f"Task with ID {task_id} not found.")


# [Task T-048] Handle update task (US4)
def handle_update() -> None:
    """
    Handle the 'Update task' menu option.

    Prompts for ID, shows current values, prompts for new values
    (Enter to keep current), validates, updates task.
    """
    print("\n--- Update Task ---")

    # Get task ID
    id_input = input("Enter task ID to update: ")
    task_id, error = parse_int(id_input)
    if task_id is None:
        print(error)
        return

    # Check if task exists
    task = get_task_by_id(task_id)
    if task is None:
        print(f"Task with ID {task_id} not found.")
        return

    # Show current values
    print(f"Current title: {task['title']}")
    print(f"Current description: {task['description']}")

    # Get new title (Enter to keep)
    new_title = input("New title (Enter to keep current): ")
    if new_title:
        is_valid, error = validate_title(new_title)
        if not is_valid:
            print(error)
            return
        new_title = new_title.strip()
    else:
        new_title = None

    # Get new description (Enter to keep)
    new_desc = input("New description (Enter to keep current): ")
    if new_desc:
        is_valid, error = validate_description(new_desc)
        if not is_valid:
            print(error)
            return
    else:
        new_desc = None

    # Update task
    update_task(task_id, title=new_title, description=new_desc)
    print(f"Task {task_id} updated successfully.")


# [Task T-055] Handle delete task (US5)
def handle_delete() -> None:
    """
    Handle the 'Delete task' menu option.

    Prompts for ID, parses, deletes task,
    prints success or not found message.
    """
    print("\n--- Delete Task ---")

    id_input = input("Enter task ID to delete: ")
    task_id, error = parse_int(id_input)
    if task_id is None:
        print(error)
        return

    if delete_task(task_id):
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Task with ID {task_id} not found.")


# [Task T-033] Main loop
def main() -> None:
    """
    Main application loop.

    Displays menu, gets user choice, routes to appropriate handler,
    loops until exit command.
    """
    print("Welcome to Todo Application!")

    while True:
        display_menu()
        choice = get_user_choice()

        if is_exit_command(choice):
            print("Goodbye!")
            break
        elif choice == '1':
            handle_add()
        elif choice == '2':
            handle_view()
        elif choice == '3':
            handle_update()
        elif choice == '4':
            handle_delete()
        elif choice == '5':
            handle_toggle()
        else:
            print("Invalid choice. Please enter a number between 1-6.")


# [Task T-034] Entry point
if __name__ == "__main__":
    main()
