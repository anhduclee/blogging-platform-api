from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timezone, timedelta

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
password_hash = PasswordHash.recommended()

def get_password_hash(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)

def create_access_token(username: str):
    iat = datetime.now(timezone.utc)
    exp = iat + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": username,
        "iat": iat,
        "exp": exp
    }
    encoded_jwt = jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except:
        return None
    sub = payload.get("sub")
    return sub