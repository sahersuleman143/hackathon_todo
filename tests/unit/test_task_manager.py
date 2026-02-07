# [Task T-023, T-027, T-039, T-046, T-053] Unit tests for task_manager.py
"""
test_task_manager.py - Unit tests for task CRUD operations

Per plan.md "Test Strategy"
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

import pytest
from datetime import datetime
from task_manager import (
    add_task, get_all_tasks, get_task_by_id,
    update_task, delete_task, toggle_complete, reset
)


@pytest.fixture(autouse=True)
def clean_state():
    """Reset task manager state before each test"""
    reset()
    yield
    reset()


# [Task T-023] Tests for add_task (US1)
class TestAddTask:
    """Tests for add_task function"""

    def test_add_task_minimal(self):
        """Title only creates task with empty description"""
        task = add_task("Buy groceries")
        assert task["title"] == "Buy groceries"
        assert task["description"] == ""

    def test_add_task_with_description(self):
        """Title + description creates complete task"""
        task = add_task("Buy groceries", "Get milk and bread")
        assert task["title"] == "Buy groceries"
        assert task["description"] == "Get milk and bread"

    def test_add_task_auto_id(self):
        """IDs increment correctly"""
        task1 = add_task("Task 1")
        task2 = add_task("Task 2")
        task3 = add_task("Task 3")

        assert task1["id"] == 1
        assert task2["id"] == 2
        assert task3["id"] == 3

    def test_add_task_sets_created_at(self):
        """Task has created_at timestamp"""
        before = datetime.now()
        task = add_task("Test task")
        after = datetime.now()

        assert task["created_at"] >= before
        assert task["created_at"] <= after

    def test_add_task_sets_completed_false(self):
        """New task has completed=False"""
        task = add_task("Test task")
        assert task["completed"] is False


# [Task T-027] Tests for get_all_tasks (US2)
class TestGetAllTasks:
    """Tests for get_all_tasks function"""

    def test_get_all_tasks_empty(self):
        """Returns empty list when no tasks"""
        tasks = get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_populated(self):
        """Returns all tasks in order"""
        add_task("Task 1")
        add_task("Task 2")
        add_task("Task 3")

        tasks = get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0]["title"] == "Task 1"
        assert tasks[1]["title"] == "Task 2"
        assert tasks[2]["title"] == "Task 3"


# [Task T-039] Tests for get_task_by_id and toggle_complete (US3)
class TestGetTaskById:
    """Tests for get_task_by_id function"""

    def test_get_task_by_id_exists(self):
        """Returns correct task when ID exists"""
        add_task("Task 1")
        task2 = add_task("Task 2")

        result = get_task_by_id(2)
        assert result is not None
        assert result["id"] == 2
        assert result["title"] == "Task 2"

    def test_get_task_by_id_not_found(self):
        """Returns None when ID not found"""
        add_task("Task 1")

        result = get_task_by_id(999)
        assert result is None


class TestToggleComplete:
    """Tests for toggle_complete function"""

    def test_toggle_complete_false_to_true(self):
        """Toggles from False to True"""
        task = add_task("Test task")
        assert task["completed"] is False

        result = toggle_complete(1)
        assert result is True
        assert task["completed"] is True

    def test_toggle_complete_true_to_false(self):
        """Toggles from True back to False"""
        task = add_task("Test task")
        toggle_complete(1)  # False -> True
        assert task["completed"] is True

        result = toggle_complete(1)  # True -> False
        assert result is True
        assert task["completed"] is False

    def test_toggle_complete_not_found(self):
        """Returns False when task not found"""
        add_task("Test task")

        result = toggle_complete(999)
        assert result is False


# [Task T-046] Tests for update_task (US4)
class TestUpdateTask:
    """Tests for update_task function"""

    def test_update_task_title(self):
        """Updates title only"""
        task = add_task("Original title", "Original desc")

        result = update_task(1, title="New title")
        assert result is True
        assert task["title"] == "New title"
        assert task["description"] == "Original desc"

    def test_update_task_description(self):
        """Updates description only"""
        task = add_task("Original title", "Original desc")

        result = update_task(1, description="New desc")
        assert result is True
        assert task["title"] == "Original title"
        assert task["description"] == "New desc"

    def test_update_task_both(self):
        """Updates both title and description"""
        task = add_task("Original title", "Original desc")

        result = update_task(1, title="New title", description="New desc")
        assert result is True
        assert task["title"] == "New title"
        assert task["description"] == "New desc"

    def test_update_task_not_found(self):
        """Returns False when task not found"""
        add_task("Test task")

        result = update_task(999, title="New title")
        assert result is False

    def test_update_task_keeps_other_fields(self):
        """Preserves id, completed, created_at"""
        task = add_task("Original title", "Original desc")
        original_id = task["id"]
        original_created = task["created_at"]
        toggle_complete(1)  # Set completed to True

        update_task(1, title="New title")

        assert task["id"] == original_id
        assert task["created_at"] == original_created
        assert task["completed"] is True


# [Task T-053] Tests for delete_task (US5)
class TestDeleteTask:
    """Tests for delete_task function"""

    def test_delete_task_exists(self):
        """Deletes task when exists, returns True"""
        add_task("Task 1")
        add_task("Task 2")

        result = delete_task(1)
        assert result is True

        tasks = get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]["id"] == 2

    def test_delete_task_not_found(self):
        """Returns False when task not found"""
        add_task("Task 1")

        result = delete_task(999)
        assert result is False

    def test_delete_preserves_other_ids(self):
        """Other task IDs remain unchanged after deletion"""
        add_task("Task 1")
        add_task("Task 2")
        add_task("Task 3")

        delete_task(2)

        tasks = get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0]["id"] == 1
        assert tasks[1]["id"] == 3

    def test_delete_id_not_recycled(self):
        """Deleted IDs are not reused"""
        add_task("Task 1")
        add_task("Task 2")
        delete_task(2)

        task3 = add_task("Task 3")
        assert task3["id"] == 3  # Not 2
