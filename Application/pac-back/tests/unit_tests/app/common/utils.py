from uuid import uuid4

from app.common.base_models import TestEnv
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor


def get_token_and_assert_login(email: str, password: str, expected_status_code: int) -> str | None:
    login_response = AuthenticationInteractor.login(email, password)
    assert login_response.status_code == expected_status_code
    if login_response.status_code == 200:
        return login_response.json().get("access_token")
    return None


def init_test() -> TestEnv:
    user_email = f"{uuid4()}@user.com"
    orgadmin_email = f"{uuid4()}@orgadmin.com"
    admin_email = f"{uuid4()}@admin.com"
    password = "pass"
    org = HackAuthenticationInteractor.create_an_organization(str(uuid4()))
    user = HackAuthenticationInteractor.create_a_user(str(uuid4()), str(uuid4()), user_email, password, org.id)
    orgadmin = HackAuthenticationInteractor.create_an_org_admin(
        str(uuid4()), str(uuid4()), orgadmin_email, password, org.id
    )
    admin = HackAuthenticationInteractor.create_an_admin(str(uuid4()), str(uuid4()), admin_email, password)

    admin_token = get_token_and_assert_login(admin_email, password, 200)
    orgadmin_token = get_token_and_assert_login(orgadmin_email, password, 200)
    user_token = get_token_and_assert_login(user_email, password, 200)

    return TestEnv(
        org=org,
        user=user,
        orgadmin=orgadmin,
        admin=admin,
        user_token=user_token,
        orgadmin_token=orgadmin_token,
        admin_token=admin_token,
    )


def clean_test(testenv: TestEnv):
    HackAuthenticationInteractor.delete_a_user_by_id(testenv.user.id)
    HackAuthenticationInteractor.delete_a_user_by_id(testenv.orgadmin.id)
    HackAuthenticationInteractor.delete_a_user_by_id(testenv.admin.id)
    HackAuthenticationInteractor.delete_an_org_by_id(testenv.org.id)
