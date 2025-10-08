import os
from datetime import datetime, timedelta, timezone
from typing import Literal

from fastapi import HTTPException, status

import bcrypt
import dotenv
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from app.database.client import get_db
from app.models.base_models import UserCreationModel, UserModel, JWTModel, LoginResponse
from supabase import Client


class AuthenticationInteractor:
    async def password_hasher(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    async def verify_password(password: str, hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

    @staticmethod
    async def create_user(user: UserCreationModel) -> UserModel:
        supabase: Client = get_db()

        # Check if email already exists
        email_check = supabase.table("users").select("id").eq("email", user.email).limit(1).execute()
        if email_check.data:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        # Hash the password
        hashed_password = await AuthenticationInteractor.password_hasher(user.password)

        # Insert new user
        response = (
            supabase.table("users")
            .insert(
                {
                    "email": user.email,
                    "password": hashed_password,
                    "credits": user.credits,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            )
            .execute()
        )

        return UserModel(**response.data[0])

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
