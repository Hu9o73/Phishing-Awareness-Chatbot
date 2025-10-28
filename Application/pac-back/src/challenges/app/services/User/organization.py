from app.database.interactors.Base.org_members import OrgMembersInteractor
from app.models.base_models import OrgMemberModel
from app.services.Base.authentication import AuthenticationService


class UserOrganizationService:
    @staticmethod
    async def list_members(token: str) -> list[OrgMemberModel]:
        user = AuthenticationService.get_current_user(token)
        return await OrgMembersInteractor.list_members_by_organization(user.organization_id)
