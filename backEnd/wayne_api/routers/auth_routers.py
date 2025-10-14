from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

from wayne_api.models import User
from wayne_api.database import get_session
from wayne_api.schemas import UserBase, UserLogin, Message
from wayne_api.dependencies import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, verify_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"])

def criar_token(id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire = datetime.now(tz=timezone.utc) + duracao_token
    to_encode = {"exp": expire, "sub": str(id)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def autenticar_usuario(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email == email).first()
    if not user: 
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    return user



@router.post("/register", response_model=Message, status_code=status.HTTP_201_CREATED)
def register_user(user: UserBase, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = bcrypt_context.hash(user.password)
    user_dict = user.model_dump()
    user_dict["password"] = hashed_password
    new_user = User(**user_dict)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"mensagem": "usuario criado com sucesso"}

@router.post("/login")
def login_user(user: UserLogin, session: Session = Depends(get_session)):
    authenticated_user = autenticar_usuario(user.email, user.password, session)
    if not authenticated_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    else:
        access_token = criar_token(str(authenticated_user.id))
        refresh_token = criar_token(str(authenticated_user.id), duracao_token=timedelta(days=7))
        return {
            "access_token": access_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer"
            }
    
@router.post("/login-form")
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    authenticated_user = autenticar_usuario(form_data.username, form_data.password, session)
    if not authenticated_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    else:
        access_token = criar_token(str(authenticated_user.id))
        return {
            "access_token": access_token, 
            "token_type": "bearer"
            }


@router.post("/refresh")
def refresh_token(current_user: User = Depends(verify_token)):
    new_access_token = criar_token(str(current_user.id))
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserBase)
def read_current_user(current_user: User = Depends(verify_token)):
    return current_user