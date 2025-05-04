from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime,timedelta,timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "23b419df33f9ea6b938864652f81aff4cf4d8bddb6d1d7e759ed7477a3d61cbb"
algorithm = "HS256"
ACCESS_TOKEN_EXPIRATION_MINUTES = 30 

def create_access_token(data : dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=algorithm)

    return encoded_jwt 

# def verify_access_token(token : str,credentials_exception):
    
#     try :
#         payload = jwt.encode(token,SECRET_KEY,algorithms=algorithm)
#         id : str = payload.get("user")