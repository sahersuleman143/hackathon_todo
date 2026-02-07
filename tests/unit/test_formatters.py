# [Task T-017] Unit tests for formatters.py
"""
test_formatters.py - Unit tests for display formatting functions

Per plan.md "Test Strategy"
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from datetime import datetime
from formatters import (
    truncate_text, format_datetime, get_status_icon,
    format_task, format_task_list,
    ICON_COMPLETE, ICON_INCOMPLETE, MSG_NO_TASKS
)


class TestTruncateText:
    """Tests for truncate_text function"""

    def test_truncate_short_text(self):
        """Short text is not truncated"""
        result = truncate_text("Short text")
        assert result == "Short text"

    def test_truncate_long_text(self):
        """Long text is truncated with '...'"""
        long_text = "x" * 60
        result = truncate_text(long_text, max_length=50)
        assert result == "x" * 50 + "..."
        assert len(result) == 53  # 50 + 3 for "..."

    def test_truncate_exact_length(self):
        """Text at exact length is not truncated"""
        exact_text = "x" * 50
        result = truncate_text(exact_text, max_length=50)
        assert result == exact_text
        assert len(result) == 50


class TestFormatDatetime:
    """Tests for format_datetime function"""

    def test_format_datetime(self):
        """Datetime is formatted correctly"""
        dt = datetime(2026, 1, 28, 10, 30)
        result = format_datetime(dt)
        assert result == "2026-01-28 10:30"

    def test_format_datetime_single_digits(self):
        """Single digit months/days/hours are zero-padded"""
        dt = datetime(2026, 1, 5, 9, 5)
        result = format_datetime(dt)
        assert result == "2026-01-05 09:05"


class TestGetStatusIcon:
    """Tests for get_status_icon function"""

    def test_get_status_icon_complete(self):
        """Complete task returns checkmark"""
        result = get_status_icon(True)
        assert result == ICON_COMPLETE

    def test_get_status_icon_incomplete(self):
        """Incomplete task returns empty box"""
        result = get_status_icon(False)
        assert result == ICON_INCOMPLETE


class TestFormatTaskList:
    """Tests for format_task_list function"""

    def test_format_task_list_empty(self):
        """Empty list shows 'No tasks yet'"""
        result = format_task_list([])
        assert result == MSG_NO_TASKS

    def test_format_task_list_populated(self):
        """Populated list shows header and tasks"""
        tasks = [
            {
                "id": 1,
                "title": "Buy groceries",
                "description": "Get milk and bread",
                "completed": False,
                "created_at": datetime(2026, 1, 28, 10, 30)
            },
            {
                "id": 2,
                "title": "Call mom",
                "description": "Wish her happy birthday",
                "completed": True,
                "created_at": datetime(2026, 1, 28, 10, 35)
            }
        ]
        result = format_task_list(tasks)

        # Check header exists
        assert "ID" in result
        assert "Title" in result
        assert "Description" in result
        assert "Status" in result
        assert "Created" in result

        # Check task data appears
        assert "Buy groceries" in result
        assert "Call mom" in result
        assert ICON_COMPLETE in result
        assert ICON_INCOMPLETE in result


class TestFormatTask:
    """Tests for format_task function"""

    def test_format_task_basic(self):
        """Task is formatted with all fields"""
        task = {
            "id": 1,
            "title": "Test task",
            "description": "Test description",
            "completed": False,
            "created_at": datetime(2026, 1, 28, 10, 30)
        }
        result = format_task(task)

        assert "1" in result
        assert "Test task" in result
        assert "Test description" in result
        assert ICON_INCOMPLETE in result
        assert "2026-01-28 10:30" in result

    def test_format_task_truncates_long_description(self):
        """Long description is truncated"""
        task = {
            "id": 1,
            "title": "Test task",
            "description": "x" * 100,
            "completed": False,
            "created_at": datetime(2026, 1, 28, 10, 30)
        }
        result = format_task(task)

        # Should have truncation indicator
        assert "..." in result
