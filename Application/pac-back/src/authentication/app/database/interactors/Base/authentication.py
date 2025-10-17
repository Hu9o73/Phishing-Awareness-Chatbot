import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

import bcrypt
import dotenv
import jwt
from app.database.client import get_db
from app.models.base_models import JWTModel, LoginResponse, UserCreationModel, UserModel
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from supabase import Client


class AuthenticationInteractor(ABC):
    async def password_hasher(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    async def verify_password(password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

    @staticmethod
    async def login_user(email: str, password: str) -> str:
        supabase: Client = get_db()
        response = supabase.table("users").select("id, password").eq("email", email).execute()

        if not response.data:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        hashed_password = response.data[0]["password"]
        result = await AuthenticationInteractor.verify_password(password, hashed_password)

        if not result:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        dotenv.load_dotenv()
        payload = {
            "user_id": response.data[0]["id"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        }
        token = jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm=os.getenv("ALGORITHM"))

        return LoginResponse(access_token=token)

    @staticmethod
    async def decode_jwt(jwt_str: str) -> JWTModel:
        dotenv.load_dotenv()
        try:
            decoded_jwt = jwt.decode(jwt_str, os.getenv("JWT_SECRET"), os.getenv("ALGORITHM"))
            return JWTModel(**decoded_jwt)
        except InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token")
        except ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired JWT token")

    @staticmethod
    @abstractmethod
    async def create_user(user: UserCreationModel) -> UserModel:
        pass

    @staticmethod
    async def get_user_org(jwt_str: str) -> str:
        supabase: Client = get_db()
        decoded_jwt = await AuthenticationInteractor.decode_jwt(jwt_str)
        response = supabase.table("users").select("organization_id").eq("id", decoded_jwt.user_id).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization not found for user {decoded_jwt.user_id}"
            )
        return response.data[0]["organization_id"]
