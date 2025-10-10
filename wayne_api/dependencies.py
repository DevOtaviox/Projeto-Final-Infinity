import os 
from dotenv import load_dotenv
from passlib.context import CryptContext
from wayne_api.models import User
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from wayne_api.database import get_session


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

def verify_token(token:str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(dic_info.get("sub"))    
    except JWTError:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso negado")
    
    usuario = session.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Acesso negado")
    return usuario