from uuid import UUID

from app.database.client import get_db
from app.database.interactors.Base.authentication import AuthenticationInteractor
from app.services.Base.authentication import AuthenticationService
from app.database.interactors.Base.users import UsersInteractor
from app.models.base_models import OrgMemberCreationModel, OrgMemberModel, StatusResponse
from fastapi import HTTPException, status
from supabase import Client


class OrgAdminOrganizationInteractor:
    @staticmethod
    async def get_member_by_id(member_id: UUID) -> OrgMemberModel:
        supabase: Client = get_db()
        response = supabase.table("org_members").select("*").eq("id", member_id).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with id {member_id} not found")
        return OrgMemberModel(**response.data[0])

    @staticmethod
    async def get_members_in_organization(user_token: str) -> list[OrgMemberModel]:
        jwt_decoded = await AuthenticationService.decode_jwt(user_token)
        organization_id = await UsersInteractor.get_user_organization_from_id(jwt_decoded.user_id)
        supabase: Client = get_db()
        response = supabase.table("org_members").select("*").eq("organization_id", organization_id).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No members in organization."
            )
        return [OrgMemberModel(**member) for member in response.data]

    @staticmethod
    async def create_member(member: OrgMemberCreationModel) -> OrgMemberModel:
        supabase: Client = get_db()
        response = (
            supabase.table("org_members")
            .insert(
                {
                    "organization_id": str(member.organization_id),
                    "email": member.email,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                }
            )
            .execute()
        )
        return OrgMemberModel(**response.data[0])

    @staticmethod
    async def delete_member(member_id: UUID) -> StatusResponse:
        supabase: Client = get_db()
        existence_check = supabase.table("org_members").select("*").eq("id", member_id).execute()
        if not existence_check.data or len(existence_check.data) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Member with id {member_id} not found")
        supabase.table("org_members").delete().eq("id", member_id).execute()
        return StatusResponse(status="ok", message=f"Member {member_id} deleted succesfully")
