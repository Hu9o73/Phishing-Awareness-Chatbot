pip install pytest

set -e

echo "Waiting for user-manager to be healthy..."

until curl -s http://pac-authentication:8001/health | grep -q "ok"; do
  sleep 2
done

echo "STARTING AUTHENTICATION TESTS"

export PYTHONPATH=$(pwd)

pytest ./app/authentication
