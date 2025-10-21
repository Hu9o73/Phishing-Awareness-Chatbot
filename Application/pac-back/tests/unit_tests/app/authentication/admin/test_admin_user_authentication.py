from uuid import uuid4
import pytest

from app.common.interactors.admin.auth_interactor import AdminAuthenticationInteractor
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.utils import clean_test, init_test



@pytest.mark.parametrize(
    "token_attr,expected_status,user_id_type",
    [
        ("admin_token", 200, "custom"),
        ("wrong_token", 401, "custom"),
        (None, 401, "custom"),
        ("user_token", 403, "custom"),
        ("orgadmin_token", 403, "custom"),
        ("admin_token", 200, "random"),
    ],
    ids=[
        "admin_ok",
        "wrong_token",
        "missing_token",
        "user_forbidden",
        "orgadmin_forbidden",
        "admin_nonexistent_user",
    ],
)
def test_admin_delete_user(token_attr, expected_status, user_id_type):
    env = init_test()
    custom_user = HackAuthenticationInteractor.create_a_user(
        str(uuid4()), str(uuid4()), f"{uuid4()}@user.com", "pass", env.org.id
    )

    try:
        token = getattr(env, token_attr) if token_attr and hasattr(env, token_attr) else token_attr
        user_id = custom_user.id if user_id_type == "custom" else uuid4()

        response = AdminAuthenticationInteractor.delete_user(token, user_id)
        assert response.status_code == expected_status
    finally:
        clean_test(env)
        HackAuthenticationInteractor.delete_a_user_by_id(custom_user.id)
