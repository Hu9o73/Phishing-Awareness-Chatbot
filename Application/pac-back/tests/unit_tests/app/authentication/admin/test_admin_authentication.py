from uuid import uuid4

from app.common.interactors.admin.auth_interactor import AdminAuthenticationInteractor
from app.common.interactors.hack.auth_interactor import HackAuthenticationInteractor
from app.common.utils import clean_test, init_test


def test_admin_delete_user():
    env = init_test()
    custom_user = HackAuthenticationInteractor.create_a_user(
        str(uuid4()), str(uuid4()), f"{uuid4()}@user.com", "pass", env.org.id
    )
    try:
        for t, sc, user_id in zip(
            [env.admin_token, "wrong_token", None, env.user_token, env.orgadmin_token, env.admin_token],
            [200, 401, 401, 403, 403, 200],
            [custom_user.id, custom_user.id, custom_user.id, custom_user.id, custom_user.id, uuid4()]
        ):
            response = AdminAuthenticationInteractor.delete_user(t, user_id)
            assert response.status_code == sc
    finally:
        clean_test(env)
        HackAuthenticationInteractor.delete_a_user_by_id(custom_user.id)
