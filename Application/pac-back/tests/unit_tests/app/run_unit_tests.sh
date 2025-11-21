pip install pytest

set -e

echo "Waiting for user-manager to be healthy..."

until curl -s http://pac-authentication:8001/health | grep -q "ok"; do
  sleep 2
done

echo "Waiting for challenges to be healthy..."

until curl -s http://pac-challenges:8002/health | grep -q "ok"; do
  sleep 2
done

echo "Waiting for monitoring to be healthy..."

until curl -s http://pac-monitoring:8003/health | grep -q "ok"; do
  sleep 2
done

echo "STARTING AUTHENTICATION TESTS"

export PYTHONPATH=$(pwd)

pytest ./app/authentication -v

pytest ./app/challenges -v

pytest ./app/monitoring -v
