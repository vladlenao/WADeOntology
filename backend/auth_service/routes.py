from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from auth_service.schemas import UserCreate
from database import get_db
from services import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_username = AuthService.get_user_by_username(db, user_data.username)
    existing_email = AuthService.get_user_by_email(db, user_data.email)
    if existing_username or existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = AuthService.create_user(db, user_data.username, user_data.email, user_data.password)
    return {"username": user.username, "email": user.email}

@router.post("/login")
def login_for_access_token(user_data:UserCreate, db: Session = Depends(get_db)):
    user = AuthService.get_user_by_username(db, user_data.username)
    if not user or not AuthService.verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = AuthService.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = AuthService.decode_access_token(token, db)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    username = payload.get("sub")
    user = AuthService.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": user.username, "email": user.email}

@router.post("/logout")
def logout(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    return AuthService.logout(token, db)
