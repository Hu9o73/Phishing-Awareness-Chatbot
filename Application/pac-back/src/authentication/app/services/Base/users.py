from uuid import UUID

from app.database.interactors.Base.users import UsersInteractor
from app.models.base_models import PublicUserModel


class UsersService:
    @staticmethod
    async def get_user_from_id(user_id: UUID) -> PublicUserModel:
        return await UsersInteractor.get_user_from_id(user_id=user_id)
