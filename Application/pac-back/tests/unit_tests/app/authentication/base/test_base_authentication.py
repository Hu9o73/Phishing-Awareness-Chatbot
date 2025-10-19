
from app.common.base_models import PublicUserModel
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from app.common.utils import clean_test, init_test


def test_get_current_user():
    te = init_test()
    try:
        for t, sc, user in zip(
            [te.admin_token, te.orgadmin_token, te.user_token, "wrong_token", None],
            [200, 200, 200, 401, 403],
            [te.admin, te.orgadmin, te.user, None, None],
        ):
            response = AuthenticationInteractor.get_current_user(t)
            assert response.status_code == sc
            if response.status_code == 200:
                fetched_user = PublicUserModel(**response.json())
                assert fetched_user.first_name == user.first_name
                assert fetched_user.email == user.email
    finally:
        clean_test(te)
