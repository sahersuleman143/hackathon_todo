# [Task T021, T022, T023] Authentication routes
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from src.auth.dependencies import create_access_token, verify_token
from src.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from src.db.dependencies import get_db_session
from src.models.user import User
from src.services.user_service import authenticate_user, create_user, get_user_by_email

router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db_session)):
    """Register new user."""
    try:
        print(f"[REGISTER] Attempting to register: {request.email}")
        user = create_user(db, request.email, request.password)
        print(f"[REGISTER] User created successfully: {user.id}")
        token = create_access_token({"sub": str(user.id), "email": user.email})
        return {"access_token": token, "token_type": "bearer", "user_id": user.id}
    except ValueError as e:
        print(f"[REGISTER] ValueError: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        print(f"[REGISTER] Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_session)):
    """Login user and return JWT token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    """Logout user (stateless JWT - client should clear token)."""
    return {"message": "Logout successful. Please clear your token."}


@router.get("/me")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    """Get current authenticated user."""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = int(payload.get("sub"))
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"id": user.id, "email": user.email, "created_at": user.created_at}
