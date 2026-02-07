# Research: Console Todo Application

**Feature**: 001-console-todo-app
**Date**: 2026-01-28
**Status**: Complete

## Overview

This document captures research findings and decisions for the Console Todo Application. Given the straightforward nature of this feature (in-memory, Python stdlib only), most decisions are clear from the specification.

---

## Research Topics

### 1. Data Storage Approach

**Decision**: List of dictionaries with module-level state

**Rationale**:
- Simple, readable, no abstraction overhead
- Dictionaries provide flexible key-value access
- List maintains insertion order (Python 3.7+)
- Module-level state is appropriate for single-user, single-session application

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Class-based TaskManager | Over-engineering for simple CRUD |
| Named tuples | Immutable; updates would require replacement |
| Dataclasses | Adds complexity without benefit for dict-based storage |
| SQLite in-memory | External dependency feel, overkill for list operations |

---

### 2. ID Generation Strategy

**Decision**: Monotonic integer counter, never recycled

**Rationale**:
- Simplest implementation (single integer)
- Matches spec requirement FR-002 and SC-007
- No race conditions (single-user)
- Gaps after deletion are acceptable per spec assumptions

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| UUID | Overkill, harder to type for users |
| Recycled IDs | Violates SC-007 (IDs must remain stable) |
| Timestamp-based | Millisecond collisions possible, less user-friendly |

---

### 3. Input Validation Pattern

**Decision**: Return tuple `(success: bool, error_message: str)`

**Rationale**:
- Clear success/failure indication
- Error message ready for display
- No exceptions for expected validation failures
- Consistent pattern across all validators

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Raise exceptions | Control flow via exceptions is anti-pattern for validation |
| Return only bool | Loses error message context |
| Result object/class | Over-engineering for simple validation |

---

### 4. CLI Menu Pattern

**Decision**: While-loop with match/switch on user input

**Rationale**:
- Simple state machine
- Easy to extend with new options
- Clear exit conditions ('6', 'q', 'exit')
- Returns to menu after each operation

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Recursive menu calls | Stack overflow risk, harder to reason about |
| Event-driven | Over-engineering for sequential CLI |
| External CLI framework (click, argparse) | Violates FR-015 (stdlib only) |

---

### 5. Display Formatting

**Decision**: Fixed-width columns with truncation

**Rationale**:
- Consistent visual alignment
- Works in any terminal
- 50-char description truncation per spec assumption
- Unicode status icons (✓/☐) for visual clarity

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Dynamic column widths | More complex, unnecessary for simple app |
| ASCII-only icons ([x]/[ ]) | Less visual appeal, though acceptable fallback |
| JSON output | Not user-friendly for CLI interaction |

---

### 6. Datetime Handling

**Decision**: Use `datetime.datetime.now()` with "YYYY-MM-DD HH:MM" format

**Rationale**:
- Stdlib `datetime` module
- Human-readable format per spec assumption
- No timezone complexity needed (local time sufficient)

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| ISO 8601 full format | Too verbose for display |
| Unix timestamp | Not human-readable |
| Third-party (arrow, pendulum) | Violates FR-015 (stdlib only) |

---

### 7. Error Message Handling

**Decision**: Centralized constants in validators.py or constants.py

**Rationale**:
- Single source of truth
- Easy to verify against spec
- Consistent messaging across application

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|------------------|
| Inline strings | Duplication, harder to maintain |
| Localization files | Over-engineering for English-only app |

---

## Technical Decisions Summary

| Area | Decision | Spec Reference |
|------|----------|----------------|
| Storage | List of dicts | FR-014 |
| ID generation | Monotonic counter | FR-002, SC-007 |
| Validation | Tuple returns | FR-009, FR-011 |
| CLI pattern | While loop | FR-012 |
| Display | Fixed-width table | FR-004 |
| Datetime | stdlib datetime | FR-015 |
| Error messages | Constants | FR-013 |

---

## Open Questions

None. All technical decisions are resolved based on specification constraints.

---

## Dependencies

**Runtime**: None (Python 3.8+ stdlib only)

**Development**:
- pytest (for testing, not bundled with app)

---

## Risks Identified

| Risk | Mitigation |
|------|------------|
| Unicode display on Windows cmd | Document fallback ASCII icons |
| Large task lists | Document memory limitation |
| Input encoding edge cases | Trust Python's `input()` handling |

---

## Next Steps

1. Create data-model.md with entity definitions
2. Create contracts/ with function signatures
3. Create quickstart.md for developer onboarding
4. Proceed to /sp.tasks for task generation
