pip install pytest

set -e

echo "Waiting for user-manager to be healthy..."

until curl -s http://pac-authentication:8001/health | grep -q "ok"; do
  sleep 2
done

echo "STARTING USER MANAGER TESTS"
echo "USER MANAGER - AUTHENTICATION"

export PYTHONPATH=$(pwd)

pytest ./app/authentication/test_healthiness.py
pytest ./app/authentication/test_authentication.py
pytest ./app/authentication/base/test_base_authentication.py
pytest ./app/authentication/admin/test_admin_authentication.py
