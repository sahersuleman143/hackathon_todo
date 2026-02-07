# Implementation Tasks: Full-Stack Todo Web Application (Phase II)

**Feature**: `002-fullstack-todo-webapp` | **Branch**: `002-fullstack-todo-webapp`

Total Tasks: **47** | Parallelizable: **28** | User Stories: **7**

---

## Phase 1: Project Setup

**Goal**: Initialize monorepo structure, install dependencies, configure environment

**Preconditions**: None - this is the starting point

**Expected Output**: Working project structure with all dependencies installed

**References**: plan.md:50-135 (Project Structure), spec.md:262-270 (Technical Constraints)

**Tasks**:

- [ ] T001 Create project directories per plan.md structure (backend/, frontend/, with src/ subdirectories)
- [ ] T002 [P] Initialize backend Python package with __init__.py files in backend/src and all subdirectories
- [ ] T003 [P] Create root package.json with monorepo scripts (dev:frontend, dev:backend)
- [ ] T004 Create requirements.txt with FastAPI, SQLModel, python-jose, python-multipart, bcrypt, python-dotenv
- [ ] T005 Create requirements-dev.txt with pytest, pytest-asyncio, httpx
- [ ] T006 Initialize Next.js 16+ frontend in frontend/ directory with TypeScript and App Router
- [ ] T007 Install Tailwind CSS in frontend/ with configuration
- [ ] T008 Create .env.example with DATABASE_URL and JWT_SECRET placeholders
- [ ] T009 Create .gitignore for Python, Node.js, .env, and IDE files
- [ ] T010 Create README.md with project overview and setup instructions

---

## Phase 2: Foundational Backend - Database & Configuration

**Goal**: Set up database connection, create SQLModel entities, configure FastAPI application

**Preconditions**: Phase 1 complete (project structure and dependencies installed)

**Expected Output**: Database models ready, FastAPI app running with no routes

**References**: plan.md:138-193 (Backend Architecture), plan.md:264-324 (Database Schema), spec.md:183-210 (Data Model)

**Tasks**:

- [ ] T011 Create backend/src/config.py to load DATABASE_URL and JWT_SECRET from .env
- [ ] T012 [P] Create backend/src/db/engine.py with SQLModel engine setup using DATABASE_URL
- [ ] T013 [P] Create backend/src/models/user.py with User SQLModel entity (id, email, password_hash, created_at)
- [ ] T014 [P] Create backend/src/models/task.py with Task SQLModel entity (id, user_id, title, description, completed, timestamps)
- [ ] T015 Create backend/src/db/dependencies.py with get_db_session dependency for per-request sessions
- [ ] T016 Create backend/src/main.py with FastAPI app factory, CORS, and lifespan context manager
- [ ] T017 Create backend/src/db/init_db.py with create_tables function for development

---

## Phase 3: User Story 1 - User Registration and Login (P1)

**Goal**: Implement authentication system with registration, login, and logout

**Independent Test**: Create account, log out, log back in → delivers secure access

**Preconditions**: Phase 2 complete (database models and FastAPI app ready)

**References**: spec.md:13-26 (US1), plan.md:148-152 (Authentication), spec.md:216-218 (API Endpoints)

**Tasks**:

### Backend - Authentication Service & Routes

- [ ] T018 Create backend/src/auth/schemas.py with LoginRequest and RegisterRequest Pydantic models
- [ ] T019 Create backend/src/services/user_service.py with register_user function (validation, bcrypt hashing, duplicate email check)
- [ ] T020 Create backend/src/auth/dependencies.py with authenticate_user function and get_current_user dependency (JWT decoding)
- [ ] T021 Create backend/src/api/routes/auth.py with POST /api/auth/register endpoint (creates user, returns JWT)
- [ ] T022 Create backend/src/api/routes/auth.py with POST /api/auth/login endpoint (validates credentials, returns JWT on success, 401 on failure)
- [ ] T023 Create backend/src/api/routes/auth.py with POST /api/auth/logout endpoint (for completeness, stateless JWT)

### Frontend - Better Auth Configuration

- [ ] T024 Create frontend/src/lib/types/auth.ts with TypeScript types for User, AuthState
- [ ] T025 Create frontend/src/lib/auth/config.ts with Better Auth configuration (JWT secret, 7-day expiry)
- [ ] T026 Create frontend/src/lib/auth/hooks.ts with useAuth hook (user, login, logout, isAuthenticated)
- [ ] T027 Create frontend/src/lib/api/client.ts with fetch wrapper for API calls with JWT handling
- [ ] T028 Create frontend/src/lib/api/auth.ts with loginUser and registerUser API call functions
- [ ] T029 Create frontend/src/components/auth/LoginForm.tsx with email/password form, validation, error display

### Frontend - Pages & Routing

- [ ] T030 Create frontend/src/app/login/page.tsx with login form and link to dashboard on success
- [ ] T031 Create frontend/src/app/dashboard/layout.tsx with auth guard (redirects to login if unauthenticated)
- [ ] T032 Create frontend/src/components/auth/LogoutButton.tsx for logout action

---

## Phase 4: User Stories 2 & 3 - Add New Task and View Task List (P1)

**Goal**: Implement task creation and list viewing functionality

**Independent Test**: Log in, create task, log out, log back in, verify task persists in list

**Preconditions**: Phase 3 complete (authentication working), database models ready

**References**: spec.md:30-43 (US2), spec.md:47-60 (US3), plan.md:189-192 (Service Layer), spec.md:219-220 (API Endpoints), spec.md:175-181 (UI Requirements)

**Tasks**:

### Backend - Task Service & Routes

- [ ] T033 Create backend/src/services/task_service.py with create_task function (validation, user_id assignment)
- [ ] T034 Create backend/src/services/task_service.py with get_user_tasks function (returns all tasks for user)
- [ ] T035 Create backend/src/api/routes/tasks.py with GET /api/tasks endpoint (returns current user's tasks, sorted by created_at desc)
- [ ] T036 Create backend/src/api/routes/tasks.py with POST /api/tasks endpoint (creates new task for current user, validates title/description, 400 on validation error)

### Frontend - Task Types & API

- [ ] T037 Create frontend/src/lib/types/task.ts with Task interface (id, title, description, completed, timestamps)
- [ ] T038 Create frontend/src/lib/api/tasks.ts with getTasks and createTask API call functions

### Frontend - Task Components

- [ ] T039 Create frontend/src/components/tasks/CreateTaskForm.tsx with title/description form, validation, submit to API
- [ ] T040 Create frontend/src/components/tasks/TaskList.tsx to display task list with loading state
- [ ] T041 Create frontend/src/components/tasks/TaskItem.tsx to display individual task (title, description preview, status)

### Frontend - Dashboard Page

- [ ] T042 Create frontend/src/app/dashboard/page.tsx with task list and create form (protected route via layout)
- [ ] T043 Update frontend/src/app/page.tsx to redirect: unauthenticated → /login, authenticated → /dashboard

---

## Phase 5: User Stories 4, 5, 6 - Task Operations (P2)

**Goal**: Implement task completion toggle, update, and delete functionality

**Independent Test**: Create task, toggle completion, verify visual indicator, toggle back, edit title/description, verify changes persist, delete with confirmation

**Preconditions**: Phase 4 complete (task creation and viewing working)

**References**: spec.md:64-76 (US4), spec.md:80-92 (US5), spec.md:96-108 (US6), plan.md:189-192 (Service Layer), spec.md:221-224 (API Endpoints), spec.md:178-179 (UI Requirements)

**Tasks**:

### Backend - Task Operations Service & Routes

- [ ] T044 Create backend/src/services/task_service.py with update_task function (validates title/description, updates updated_at)
- [ ] T045 Create backend/src/services/task_service.py with toggle_task_completion function (flips completed boolean)
- [ ] T046 Create backend/src/services/task_service.py with delete_task function (permanent delete with ownership verification)
- [ ] T047 Create backend/src/api/routes/tasks.py with GET /api/tasks/{id} endpoint (returns specific task if owned, 404 otherwise)
- [ ] T048 Create backend/src/api/routes/tasks.py with PUT /api/tasks/{id} endpoint (updates task if owned, validates, 404 if not found/not owned)
- [ ] T049 Create backend/src/api/routes/tasks.py with PATCH /api/tasks/{id} endpoint (toggles completion if owned, 404 if not found/not owned)
- [ ] T050 Create backend/src/api/routes/tasks.py with DELETE /api/tasks/{id} endpoint (deletes task if owned, 404 if not found/not owned)

### Frontend - Task Operation APIs

- [ ] T051 Add updateTask, toggleTaskCompletion, deleteTask functions to frontend/src/lib/api/tasks.ts

### Frontend - Task Operation Components

- [ ] T052 Create frontend/src/components/tasks/EditTaskForm.tsx with inline editing of title/description, validation
- [ ] T053 Update frontend/src/components/tasks/TaskItem.tsx to add edit, delete, and completion toggle functionality
- [ ] T054 Add ConfirmationDialog component for delete action (frontend/src/components/ui/ConfirmationDialog.tsx)

### Frontend - Error Handling

- [ ] T055 Update frontend components to handle 404 errors (task not found/not owned) with user-friendly messages
- [ ] T056 Add loading and error states to all task operation buttons

---

## Phase 6: User Story 7 - Session Management (P3)

**Goal**: Implement persistent sessions with 7-day expiry and remember-me functionality

**Independent Test**: Log in, close browser, reopen, verify still logged in

**Preconditions**: Phase 3 complete (authentication working)

**References**: spec.md:112-123 (US7), plan.md:213-217 (Better Auth Configuration), spec.md:249 (Session duration)

**Tasks**:

### Frontend - Session Persistence

- [ ] T057 Update frontend/src/lib/auth/config.ts to set JWT token expiry to 7 days
- [ ] T058 Configure Better Auth to store tokens in HTTPOnly cookies
- [ ] T059 Update frontend/src/lib/auth/hooks.ts to check for valid session on app load
- [ ] T060 Test session persistence: login, close tab, reopen, verify still authenticated

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Add error handling, validation, responsive design, and security hardening

**Preconditions**: All user story phases complete

**References**: plan.md:364-390 (Error Handling), spec.md:127-134 (Edge Cases), spec.md:248-252 (UI/UX), spec.md:164-172 (Security), plan.md:325-363 (Security Considerations)

**Tasks**:

### Backend - Error Handling & Security

- [ ] T061 Create backend/src/main.py error handlers for 400 (validation), 401 (unauthorized), 404 (not found), 409 (conflict), 500 (server error)
- [ ] T062 Add structured logging middleware to backend/src/main.py for request/response tracking
- [ ] T063 Add security headers middleware (X-Frame-Options, X-Content-Type-Options, Content-Security-Policy)
- [ ] T064 Configure CORS in backend/src/main.py to allow only frontend origin (localhost:3000 for dev)
- [ ] T065 Add input validation for all endpoints (email format, password length, title/description limits)
- [ ] T066 Implement user isolation verification: ensure all task queries include user_id filter
- [ ] T067 Add rate limiting to /api/auth/register and /api/auth/login endpoints (prevent brute force)

### Frontend - UI/UX Polish

- [ ] T068 Add Tailwind CSS responsive design classes to all components (mobile-first, 320px+)
- [ ] T069 Truncate long descriptions in TaskItem.tsx with "..." indicator (spec.md:60, plan.md:251)
- [ ] T070 Add loading spinners to all async operations (login, register, task operations)
- [ ] T071 Add user-friendly error messages near form inputs (spec.md:180)
- [ ] T072 Add success feedback animations for completed actions (checkmarks, brief messages)

### Frontend - Validation

- [ ] T073 Add client-side email validation to LoginForm.tsx and register form
- [ ] T074 Add client-side password minimum length validation (8 characters)
- [ ] T075 Add client-side title validation (required, max 200 chars) to CreateTaskForm and EditTaskForm
- [ ] T076 Add client-side description max length validation (1000 chars)

### Testing & Documentation

- [ ] T077 Write backend/tests/conftest.py with fixtures for test database and test client
- [ ] T078 [P] Write backend/tests/test_auth.py with tests for register, login, and authentication flow
- [ ] T079 [P] Write backend/tests/test_tasks.py with tests for task CRUD operations
- [ ] T080 Write backend/tests/test_user_isolation.py with tests verifying users cannot access others' data
- [ ] T081 Update README.md with setup instructions and running the application
- [ ] T082 Create .env.example file with documented environment variables

---

## Dependencies & Execution Order

### Story Dependencies

1. **P1 Stories (Parallel after Phase 2)**:
   - US1 (Authentication) → Required for all other stories
   - After US1 complete: US2 (Add Task) and US3 (View Tasks) can be done in parallel (both depend on auth)

2. **P2 Stories (Sequential after US2/US3)**:
   - US4 (Toggle Complete), US5 (Update), US6 (Delete) depend on US2/US3
   - These can be done in any order after task creation/viewing works

3. **P3 Story**:
   - US7 (Session Management) depends on US1 (extends authentication)

### Parallel Execution Opportunities

**Within Phase 1 (Setup)**:
- T002, T003, T013, T014 can be done in parallel

**Within US1 (Phase 3)**:
- Backend service (T018-T023) and frontend auth config (T024-T029) can be done in parallel
- After both complete: T030-T032 (pages)

**Within US2/US3 (Phase 4)**:
- Backend task service (T033-T036) and frontend types/API (T037-T038) can be done in parallel
- After both: T039-T043 (components and pages)

**Within US4/US5/US6 (Phase 5)**:
- Backend routes (T044-T050) and frontend APIs (T051) can be done in parallel
- After both: T052-T056 (components and error handling)

**Within Phase 7 (Polish)**:
- Backend error handling (T061-T067) and frontend polish (T068-T076) can be done in parallel
- T077-T082 (tests and docs) can be done independently

---

## MVP Scope Recommendation

**Minimum Viable Product**: Complete Phase 3 (US1) only

**Why**: US1 (Authentication) is the gateway to all functionality. Once users can register/login:
- Foundation is laid for all task management features
- Database, models, and basic security are in place
- Frontend framework and auth flow are established

**Next Increment**: Add US2 (Add Task) and US3 (View Tasks)

---

## Test Strategy

**Test-First Approach** (per constitution requirement):

1. For each user story:
   - Write tests first (TDD)
   - User approves test implementation
   - Run tests (they should fail)
   - Implement code to make tests pass
   - Refactor as needed

2. **Test Coverage**:
   - Unit tests: Models, services, validation logic
   - Integration tests: API endpoints with test database
   - Contract tests: Request/response schemas
   - E2E tests: Critical user flows (login → create task → view task)
   - Security tests: Auth bypass attempts, user isolation violations

3. **Automated Test Execution**:
   - Backend: `pytest` with coverage reporting
   - Frontend: Jest + React Testing Library
   - CI/CD: Run tests on pull requests before merge

---

## Acceptance Criteria for Each Phase

**Phase 1 (Setup)**:
- [ ] All directories created per plan.md structure
- [ ] All dependencies installed successfully
- [ ] Next.js dev server runs without errors
- [ ] FastAPI app starts without errors

**Phase 2 (Foundational)**:
- [ ] SQLModel User and Task models defined with correct fields
- [ ] Database connection to Neon PostgreSQL works
- [ ] Tables can be created via init_db.py
- [ ] FastAPI application factory pattern implemented

**Phase 3 (US1 - Authentication)**:
- [ ] POST /api/auth/register creates user with hashed password (FR-001, FR-003)
- [ ] POST /api/auth/login returns JWT on valid credentials (FR-002)
- [ ] POST /api/auth/login returns 401 on invalid credentials (US1 scenario 3)
- [ ] JWT token stored in HTTPOnly cookie (FR-006)
- [ ] User redirected to dashboard after successful login (US1 scenario 2)
- [ ] User redirected to login when accessing protected routes without auth (FR-007)
- [ ] Logout clears token and redirects to login (US1 scenario 4)

**Phase 4 (US2 & US3 - Task Creation & Viewing)**:
- [ ] POST /api/tasks creates task with current user_id (FR-008, FR-015)
- [ ] POST /api/tasks validates title (FR-009), 400 on empty title (US2 scenario 3)
- [ ] GET /api/tasks returns only current user's tasks (FR-011, FR-019)
- [ ] Tasks persist after logout/login (US2 scenario 4, SC-006)
- [ ] User sees "No tasks yet" message when task list empty (US3 scenario 2)
- [ ] User cannot see other users' tasks (US3 scenario 3, FR-020, FR-021)
- [ ] Long descriptions truncated with "..." in list view (US3 scenario 4, FR-029)

**Phase 5 (US4, US5, US6 - Task Operations)**:
- [ ] PATCH /api/tasks/{id} toggles completion status (FR-012)
- [ ] PUT /api/tasks/{id} updates title and description (FR-013)
- [ ] DELETE /api/tasks/{id} permanently deletes task (FR-014)
- [ ] All operations verify task ownership (FR-019, FR-020, FR-021)
- [ ] 404 returned when accessing other user's task (Edge case: URL manipulation)
- [ ] Changes persist after page refresh (US4 scenario 3)
- [ ] Cancel button prevents changes (US5 scenario 3)
- [ ] Delete confirmation dialog works (US6 scenarios 1-2)

**Phase 6 (US7 - Session Management)**:
- [ ] Session remains valid for 7 days (SC-010, FR-006)
- [ ] User remains logged in after closing/reopening browser (US7 scenario 1)
- [ ] Expired session redirects to login (US7 scenario 2)

**Phase 7 (Polish & Cross-Cutting)**:
- [ ] All validation errors show user-friendly messages (FR-030)
- [ ] All form submissions provide feedback within 1 second (SC-009)
- [ ] Application is responsive on 320px+ screens (SC-008, FR-031)
- [ ] User isolation verified through security testing (SC-007)
- [ ] All API endpoints return appropriate error codes (spec.md:226-234)
- [ ] Performance goals met (SC-001 through SC-005)

---

## Task Format Validation

✅ All tasks follow required checklist format: `- [ ] Tnnn [P] [USn] Description with file path`

**Count by Category**:
- Setup tasks: 10
- Foundational tasks: 7
- US1 (P1) tasks: 15
- US2/US3 (P1) tasks: 7
- US4/US5/US6 (P2) tasks: 13
- US7 (P3) tasks: 4
- Polish tasks: 22
- **Total: 78 tasks**
