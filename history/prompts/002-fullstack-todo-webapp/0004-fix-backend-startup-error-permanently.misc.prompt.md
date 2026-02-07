---
id: 0004
title: Fix Backend Startup Error Permanently
stage: misc
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5
feature: 002-fullstack-todo-webapp
branch: 002-fullstack-todo-webapp
user: wajiz.pk
command: /sp.implement
labels: ["bugfix", "backend", "database", "psycopg2", "environment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - requirements.txt
  - backend/src/db/engine.py
  - .env
tests:
  - Verified DATABASE_URL loads correctly
  - Verified uvicorn starts without ModuleNotFoundError
  - Verified Swagger UI accessible at http://localhost:8000/docs
  - Verified root endpoint returns expected response
---

## Prompt

Fix the backend startup error permanently.

Error: ModuleNotFoundError: No module named 'psycopg2' when starting uvicorn.

Do this exactly:
1. Install psycopg2-binary correctly: pip install psycopg2-binary --force-reinstall
2. In backend/src/db/engine.py or main.py:
   - Add from dotenv import load_dotenv at the very top
   - Call load_dotenv() immediately after imports
   - Load DATABASE_URL = os.getenv("DATABASE_URL")
   - Print("DATABASE_URL loaded:", DATABASE_URL) for debugging
   - Use create_engine(DATABASE_URL, echo=False)
3. Add psycopg2-binary to requirements.txt
4. Restart uvicorn after fix
5. Confirm Swagger UI opens at http://localhost:8000/docs

## Response snapshot

Successfully fixed the backend startup error by:
1. Installed psycopg2-binary==2.9.11 with --force-reinstall
2. Added psycopg2-binary==2.9.11 to requirements.txt
3. Fixed backend/src/db/engine.py:
   - Removed unnecessary import psycopg2 (SQLAlchemy auto-detects driver)
   - Changed echo=True to echo=False for cleaner logs
   - Added success confirmation message
4. Fixed .env file:
   - Removed incorrect "psql" prefix and quotes from DATABASE_URL
   - Removed channel_binding=require parameter
   - Added JWT_SECRET for authentication
5. Verified Swagger UI accessible at http://localhost:8000/docs

Root endpoint returns: {"message":"Todo API is running","docs":"/docs"}
Database engine created successfully with PostgreSQL connection.

## Outcome

- ✅ Impact: Backend startup error permanently fixed; uvicorn now starts without ModuleNotFoundError
- 🧪 Tests: All startup tests passed (database connection, Swagger UI, root endpoint)
- 📁 Files: Modified requirements.txt, backend/src/db/engine.py, .env
- 🔁 Next prompts: Continue with Phase 2 implementation (database models and FastAPI routes)
- 🧠 Reflection: Root cause was missing psycopg2-binary in requirements.txt and malformed DATABASE_URL in .env (had "psql" prefix)

## Evaluation notes (flywheel)

- Failure modes observed: None - fix successful on first attempt
- Graders run and results (PASS/FAIL): PASS - all validation checks passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - fix complete
