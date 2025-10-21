import pytest

from app.common.base_models import PublicUserModel
from app.common.interactors.base.auth_interactor import AuthenticationInteractor
from app.common.utils import clean_test, init_test


@pytest.mark.parametrize(
    "email,password,expected_status",
    [
        ("admin.email", "pass", 200),
        ("orgadmin.email", "pass", 200),
        ("user.email", "pass", 200),
        ("wrong_email", "pass", 401),
        ("admin.email", "wrong_pass", 401),
        (None, "pass", 422),
        ("admin.email", None, 422),
    ],
    ids=[
        "admin_ok",
        "orgadmin_ok",
        "user_ok",
        "invalid_email",
        "invalid_password",
        "missing_email",
        "missing_password",
    ],
)
def test_login(email, password, expected_status):
    te = init_test()
    try:
        # Resolve dynamic attributes if necessary
        email_val = getattr(te, email.split(".")[0]).email if email and "." in email else email

        response = AuthenticationInteractor.login(email_val, password)

        assert response.status_code == expected_status

        if expected_status == 200:
            fetched_token = response.json().get("access_token", "")
            assert fetched_token
    finally:
        clean_test(te)


@pytest.mark.parametrize(
    "token_attr,expected_status,expected_user_attr",
    [
        ("admin_token", 200, "admin"),
        ("orgadmin_token", 200, "orgadmin"),
        ("user_token", 200, "user"),
        ("wrong_token", 401, None),
        (None, 403, None),
    ],
    ids=[
        "admin_ok",
        "orgadmin_ok",
        "user_ok",
        "invalid_token",
        "missing_token",
    ],
)
def test_get_current_user(token_attr, expected_status, expected_user_attr):
    te = init_test()
    try:
        token = getattr(te, token_attr) if token_attr and hasattr(te, token_attr) else token_attr
        expected_user = getattr(te, expected_user_attr) if expected_user_attr else None

        response = AuthenticationInteractor.get_current_user(token)

        assert response.status_code == expected_status

        if expected_status == 200:
            fetched_user = PublicUserModel(**response.json())
            assert fetched_user.first_name == expected_user.first_name
            assert fetched_user.email == expected_user.email
    finally:
        clean_test(te)
