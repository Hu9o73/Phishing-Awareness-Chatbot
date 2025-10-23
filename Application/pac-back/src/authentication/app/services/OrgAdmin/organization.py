from uuid import UUID

from app.database.interactors.Base.users import UsersInteractor
from app.database.interactors.OrgAdmin.organization import OrgAdminOrganizationInteractor
from app.models.base_models import OrgMemberCreationModel, OrgMemberModel, StatusResponse
from app.services.Base.authentication import AuthenticationService


class OrgAdminOrganizationService:
    @staticmethod
    async def get_member_by_id(member_id: UUID, user_token: str) -> OrgMemberModel:
        jwt_decoded = await AuthenticationService.decode_jwt(user_token)
        orgadmin_user = await UsersInteractor.get_user_from_id(jwt_decoded.user_id)
        return await OrgAdminOrganizationInteractor.get_member_by_id(member_id, orgadmin_user.organization_id)

    @staticmethod
    async def get_members_in_organization(user_token: str) -> list[OrgMemberModel]:
        jwt_decoded = await AuthenticationService.decode_jwt(user_token)
        orgadmin_user = await UsersInteractor.get_user_from_id(jwt_decoded.user_id)
        return await OrgAdminOrganizationInteractor.get_members_in_organization(orgadmin_user.organization_id)

    @staticmethod
    async def create_member(email: str, first_name: str, last_name: str, user_token: str) -> OrgMemberModel:
        jwt_decoded = await AuthenticationService.decode_jwt(user_token)

        orgadmin_user = await UsersInteractor.get_user_from_id(jwt_decoded.user_id)
        member = OrgMemberCreationModel(
            email=email, first_name=first_name, last_name=last_name, organization_id=orgadmin_user.organization_id
        )

        return await OrgAdminOrganizationInteractor.create_member(member)

    @staticmethod
    async def delete_member(member_id: UUID, user_token: str) -> StatusResponse:
        jwt_decoded = await AuthenticationService.decode_jwt(user_token)
        orgadmin_user = await UsersInteractor.get_user_from_id(jwt_decoded.user_id)
        return await OrgAdminOrganizationInteractor.delete_member(member_id, orgadmin_user.organization_id)
