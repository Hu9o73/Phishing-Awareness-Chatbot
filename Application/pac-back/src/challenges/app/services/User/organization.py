from uuid import UUID

from app.database.interactors.Base.org_members import OrgMembersInteractor
from app.models.base_models import OrgMemberModel
from app.services.Base.authentication import AuthenticationService
from fastapi import HTTPException, status


class UserOrganizationService:
    @staticmethod
    def _get_user_organization_id(token: str) -> UUID:
        user = AuthenticationService.get_current_user(token)
        if user.organization_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User must belong to an organization to view its employees.",
            )
        return user.organization_id

    @staticmethod
    async def list_members(token: str, member_id: UUID | None = None) -> list[OrgMemberModel]:
        organization_id = UserOrganizationService._get_user_organization_id(token)
        if member_id is not None:
            member = await OrgMembersInteractor.get_member(member_id)
            if member is None or member.organization_id != organization_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Member not found.",
                )
            return [member]

        return await OrgMembersInteractor.list_members_by_organization(organization_id)
