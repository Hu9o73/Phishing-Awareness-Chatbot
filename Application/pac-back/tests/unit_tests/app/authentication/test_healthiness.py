import requests
from app.common.base_models import HealthResponse
from app.common.settings import settings


def test_healthiness():
    response = requests.get(f"{settings.AUTHENTICATION_URL}/health")
    assert response.status_code == 200
    response = HealthResponse(**response.json())
    assert response.status == "ok"
