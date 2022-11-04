from datetime import datetime, timedelta, timezone
from typing import Dict, Union

import jwt
from decouple import config
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from apps.users import crud as UserDAL

JWT_SECRET = config("JWT_SECRET", default="gt74dg*&@%#Y#$)#@#$ssjdhgshdgf", cast=str)
JWT_ALGORITHM = config("JWT_ALGORITHM", default="HS256", cast=str)
JWT_EXP = config("JWT_EXP", default=3, cast=int)


class HashManager:
    @staticmethod
    def hash_password(pwd: str) -> str:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").hash(pwd)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(
            plain_password, hashed_password
        )

    @staticmethod
    def encode_data(data_to_encode: Dict) -> str:
        return jwt.encode(
            {
                **data_to_encode,
                "exp": datetime.now(tz=timezone.utc) + timedelta(days=JWT_EXP),
                # "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=3),
            },
            JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )

    @staticmethod
    def decode_data(jwt_string: str) -> Union[Dict, bool]:
        try:
            return jwt.decode(jwt_string, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            auth_payload = self.verify_jwt(credentials.credentials)
            if not auth_payload:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            user = UserDAL.get_user_by_username(username=auth_payload.get("username"))
            return user
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        try:
            payload = HashManager.decode_data(jwt_token)
        except:
            payload = None
        return payload
