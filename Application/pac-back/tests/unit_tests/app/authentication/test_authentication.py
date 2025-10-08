from uuid import uuid4, UUID

import pytest
from app.common.base_models import UserModel
from app.common.interactors.auth_interactor import AuthenticationInteractor
from app.common.enum_models import RoleEnum

authentication_interactor = AuthenticationInteractor()


@pytest.mark.parametrize(
    "first_name, last_name, uuid, password",
    [("John", "Doe", uuid4(), "StrongPass123!"), ("Jane", "Doe", uuid4(), "StrongPass123!")],
)
def test_authentication(first_name: str, last_name: str, uuid: UUID, password: str):
    email = f"{uuid}@example.com"

    # Signup
    response = authentication_interactor.signup(first_name, last_name, email, password)
    assert response.status_code == 200

    user = UserModel(**response.json())
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.role == RoleEnum.MEMBER
    assert user.credits == 0


    response = authentication_interactor.signup(first_name, last_name, email, password)
    assert response.status_code == 409
    assert response.json().get("detail", "") == "Email already registered"


    # Login
    response = authentication_interactor.login(email, password)
    assert response.status_code == 200
    response_dict: dict = response.json()
    token = str(response_dict.get("access_token"))
    print(token)
    assert len(token) > 0

    for e, p in zip([email, "wrong_email", "wrong_email"], ["wrong_password", password, "wrong_password"]):
        response = authentication_interactor.login(e, p)
        assert response.status_code == 401
        assert response.json().get("detail", "") == "Invalid email or password"

    # VerifyJWT
    for t, sc in zip([token, "invalid_token", None], [200, 401, 403]):
        response = authentication_interactor.verifyjwt(t)
        assert response.status_code == sc
        if response.status_code == 401:
            assert response.json().get("detail") == "Invalid JWT token"

    # Cleanup
    authentication_interactor.delete(email)
    response = authentication_interactor.login(email, password)
    assert response.status_code == 401
