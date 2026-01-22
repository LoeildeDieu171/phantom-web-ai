from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt, time

SECRET = "PHANTOM_SECRET"
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

def create_token(user_id):
    return jwt.encode(
        {"user": user_id, "exp": time.time() + 86400},
        SECRET,
        algorithm="HS256"
    )

def get_user(token: str = Depends(oauth2)):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data["user"]
    except:
        raise HTTPException(status_code=401)
