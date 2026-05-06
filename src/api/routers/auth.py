from jose import jwt
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()
algorithm = 'HS256'
key = os.getenv("JWT_SECRET")
oauth_verif = OAuth2PasswordBearer(tokenUrl="login")

def getCurrentUser(token : str = Depends(oauth_verif)):
    notVerified = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="ta sem token doidao",headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, key, algorithms=[algorithm])
        username : str = payload.get(sub)
        if username is None:
            raise notVerified
        return username
    except JWTError:
        raise notVerified