# [Task T-016] Unit tests for validators.py
"""
test_validators.py - Unit tests for input validation functions

Per plan.md "Test Strategy"
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from validators import (
    validate_title, validate_description, parse_int,
    MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH,
    ERROR_EMPTY_TITLE, ERROR_TITLE_TOO_LONG,
    ERROR_DESC_TOO_LONG, ERROR_INVALID_NUMBER
)


class TestValidateTitle:
    """Tests for validate_title function"""

    def test_validate_title_valid(self):
        """Normal title passes validation"""
        is_valid, error = validate_title("Buy groceries")
        assert is_valid is True
        assert error == ""

    def test_validate_title_empty(self):
        """Empty string fails with correct message"""
        is_valid, error = validate_title("")
        assert is_valid is False
        assert error == ERROR_EMPTY_TITLE

    def test_validate_title_whitespace_only(self):
        """Whitespace-only title fails"""
        is_valid, error = validate_title("   ")
        assert is_valid is False
        assert error == ERROR_EMPTY_TITLE

    def test_validate_title_too_long(self):
        """Title > 200 chars fails"""
        long_title = "x" * 201
        is_valid, error = validate_title(long_title)
        assert is_valid is False
        assert error == ERROR_TITLE_TOO_LONG

    def test_validate_title_boundary(self):
        """Exactly 200 chars passes"""
        boundary_title = "x" * 200
        is_valid, error = validate_title(boundary_title)
        assert is_valid is True
        assert error == ""


class TestValidateDescription:
    """Tests for validate_description function"""

    def test_validate_description_valid(self):
        """Normal description passes"""
        is_valid, error = validate_description("Some details here")
        assert is_valid is True
        assert error == ""

    def test_validate_description_empty(self):
        """Empty string passes (optional field)"""
        is_valid, error = validate_description("")
        assert is_valid is True
        assert error == ""

    def test_validate_description_too_long(self):
        """Description > 1000 chars fails"""
        long_desc = "x" * 1001
        is_valid, error = validate_description(long_desc)
        assert is_valid is False
        assert error == ERROR_DESC_TOO_LONG

    def test_validate_description_boundary(self):
        """Exactly 1000 chars passes"""
        boundary_desc = "x" * 1000
        is_valid, error = validate_description(boundary_desc)
        assert is_valid is True
        assert error == ""


class TestParseInt:
    """Tests for parse_int function"""

    def test_parse_int_valid(self):
        """Valid integer string returns (int, "")"""
        value, error = parse_int("123")
        assert value == 123
        assert error == ""

    def test_parse_int_invalid(self):
        """Non-integer returns (None, error)"""
        value, error = parse_int("abc")
        assert value is None
        assert error == ERROR_INVALID_NUMBER

    def test_parse_int_negative(self):
        """Negative integer is valid"""
        value, error = parse_int("-5")
        assert value == -5
        assert error == ""

    def test_parse_int_zero(self):
        """Zero is valid"""
        value, error = parse_int("0")
        assert value == 0
        assert error == ""

    def test_parse_int_whitespace(self):
        """Whitespace around number is stripped"""
        value, error = parse_int("  42  ")
        assert value == 42
        assert error == ""

    def test_parse_int_float(self):
        """Float string is invalid"""
        value, error = parse_int("3.14")
        assert value is None
        assert error == ERROR_INVALID_NUMBER
