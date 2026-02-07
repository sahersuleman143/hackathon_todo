# [Task T-035, T-043, T-050, T-057, T-059, T-060] Integration tests for CLI flow
"""
test_cli_flow.py - Integration tests for CLI menu and workflow

Per plan.md "Integration Tests"
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from unittest.mock import patch
from io import StringIO

from task_manager import reset, get_all_tasks, add_task, get_task_by_id
from todo_app import (
    main, is_exit_command, handle_add, handle_view,
    handle_toggle, handle_update, handle_delete
)
from formatters import ICON_COMPLETE, ICON_INCOMPLETE


@pytest.fixture(autouse=True)
def clean_state():
    """Reset task manager state before each test"""
    reset()
    yield
    reset()


# [Task T-035] Tests for exit commands (US6)
class TestExitCommands:
    """Tests for exit command recognition"""

    def test_exit_command_6(self):
        """'6' is recognized as exit"""
        assert is_exit_command('6') is True

    def test_exit_command_q(self):
        """'q' is recognized as exit"""
        assert is_exit_command('q') is True

    def test_exit_command_exit(self):
        """'exit' is recognized as exit"""
        assert is_exit_command('exit') is True

    def test_non_exit_command(self):
        """Other commands are not exit"""
        assert is_exit_command('1') is False
        assert is_exit_command('2') is False
        assert is_exit_command('hello') is False


class TestMainLoop:
    """Tests for main loop behavior"""

    def test_exit_with_6(self):
        """Main exits with choice '6'"""
        with patch('builtins.input', return_value='6'):
            with patch('sys.stdout', new_callable=StringIO) as mock_out:
                main()
                output = mock_out.getvalue()
                assert "Goodbye!" in output

    def test_exit_with_q(self):
        """Main exits with choice 'q'"""
        with patch('builtins.input', return_value='q'):
            with patch('sys.stdout', new_callable=StringIO) as mock_out:
                main()
                output = mock_out.getvalue()
                assert "Goodbye!" in output

    def test_exit_with_exit(self):
        """Main exits with choice 'exit'"""
        with patch('builtins.input', return_value='exit'):
            with patch('sys.stdout', new_callable=StringIO) as mock_out:
                main()
                output = mock_out.getvalue()
                assert "Goodbye!" in output


# [Task T-060] Test add and view flow
class TestAddAndViewFlow:
    """Tests for add task then view flow"""

    def test_add_and_view_flow(self):
        """Add task -> View shows task with correct format"""
        # Simulate adding a task
        inputs = iter(['Buy groceries', 'Get milk and bread'])
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO):
                handle_add()

        # Verify task was created
        tasks = get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Buy groceries"
        assert tasks[0]["description"] == "Get milk and bread"

        # Verify view shows the task
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            handle_view()
            output = mock_out.getvalue()
            assert "Buy groceries" in output
            assert ICON_INCOMPLETE in output


# [Task T-043] Test complete workflow (US3)
class TestCompleteWorkflow:
    """Tests for toggle completion workflow"""

    def test_complete_workflow(self):
        """Add task -> Toggle -> View shows checkmark"""
        # Add a task
        task = add_task("Test task", "Test description")
        assert task["completed"] is False

        # Toggle completion
        with patch('builtins.input', return_value='1'):
            with patch('sys.stdout', new_callable=StringIO):
                handle_toggle()

        # Verify task is now complete
        task = get_task_by_id(1)
        assert task["completed"] is True

        # Verify view shows checkmark
        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            handle_view()
            output = mock_out.getvalue()
            assert ICON_COMPLETE in output


# [Task T-050] Test update flow (US4)
class TestUpdateFlow:
    """Tests for update task workflow"""

    def test_update_flow(self):
        """Add -> Update title -> View shows change"""
        # Add a task
        add_task("Original title", "Original description")

        # Update title only (empty description keeps current)
        inputs = iter(['1', 'Updated title', ''])
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO):
                handle_update()

        # Verify update
        task = get_task_by_id(1)
        assert task["title"] == "Updated title"
        assert task["description"] == "Original description"


# [Task T-057] Test delete flow (US5)
class TestDeleteFlow:
    """Tests for delete task workflow"""

    def test_delete_flow(self):
        """Add -> Delete -> View shows removed"""
        # Add tasks
        add_task("Task 1")
        add_task("Task 2")
        add_task("Task 3")

        # Delete task 2
        with patch('builtins.input', return_value='2'):
            with patch('sys.stdout', new_callable=StringIO) as mock_out:
                handle_delete()
                output = mock_out.getvalue()
                assert "deleted successfully" in output

        # Verify tasks 1 and 3 remain with original IDs
        tasks = get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0]["id"] == 1
        assert tasks[0]["title"] == "Task 1"
        assert tasks[1]["id"] == 3
        assert tasks[1]["title"] == "Task 3"


# [Task T-059] Test invalid input recovery
class TestInvalidInputRecovery:
    """Tests for error handling and menu redisplay"""

    def test_invalid_choice_shows_error(self):
        """Invalid choice shows error message"""
        # Simulate invalid choice then exit
        inputs = iter(['invalid', '6'])
        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new_callable=StringIO) as mock_out:
                main()
                output = mock_out.getvalue()
                assert "Invalid choice" in output

    def test_invalid_id_shows_error(self):
        """Invalid ID format shows error"""
        add_task("Test task")

        with patch('builtins.input', return_value='abc'):
            with patch('sys.stdout', new_callable=StringIO) as mock_out:
                handle_toggle()
                output = mock_out.getvalue()
                assert "valid number" in output

    def test_not_found_id_shows_error(self):
        """Non-existent ID shows not found message"""
        add_task("Test task")

        with patch('builtins.input', return_value='999'):
            with patch('sys.stdout', new_callable=StringIO) as mock_out:
                handle_delete()
                output = mock_out.getvalue()
                assert "not found" in output
