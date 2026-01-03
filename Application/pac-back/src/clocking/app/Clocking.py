import logging
import os
import threading
import time
from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clocking")

DEFAULT_MONITORING_URL = "http://pac-monitoring:8003"
DEFAULT_AGENTIC_URL = "http://pac-agentic:8004"
DEFAULT_POLLING_INTERVAL = 600


def _get_polling_interval() -> int:
    raw_value = os.getenv("POLLING_INTERVAL_SECONDS", str(DEFAULT_POLLING_INTERVAL))
    try:
        interval = int(raw_value)
    except (TypeError, ValueError):
        logger.warning("Invalid POLLING_INTERVAL_SECONDS=%s, using %s", raw_value, DEFAULT_POLLING_INTERVAL)
        return DEFAULT_POLLING_INTERVAL
    return max(1, interval)


def _build_headers() -> dict[str, str]:
    super_clock_token = os.getenv("SUPER_CLOCK_TOKEN")
    if not super_clock_token:
        return {}
    return {"X-Super-Clock-Token": super_clock_token}


def _clocking_loop() -> None:
    base_url = os.getenv("MONITORING_SERVICE_URL", DEFAULT_MONITORING_URL).rstrip("/")
    agentic_url = os.getenv("AGENTIC_SERVICE_URL", DEFAULT_AGENTIC_URL).rstrip("/")
    interval = _get_polling_interval()

    while True:
        headers = _build_headers()
        if not headers:
            logger.error("SUPER_CLOCK_TOKEN is not set; skipping polling cycle.")
            time.sleep(interval)
            continue

        try:
            response = requests.get(f"{base_url}/retrieve-answers", headers=headers, timeout=600.0)
            if response.ok:
                logger.info("retrieve-answers: %s", response.json().get("message", "ok"))
            else:
                logger.warning("retrieve-answers failed: %s", response.text)
        except requests.RequestException as exc:
            logger.warning("retrieve-answers request error: %s", exc)

        try:
            response = requests.post(f"{agentic_url}/email-agentic-flow-all", headers=headers, timeout=600.0)
            if response.ok:
                logger.info("email-agentic-flow-all: %s", response.json().get("message", "ok"))
            else:
                logger.warning("email-agentic-flow-all failed: %s", response.text)
        except requests.RequestException as exc:
            logger.warning("email-agentic-flow-all request error: %s", exc)

        try:
            response = requests.post(f"{base_url}/send-all-pending-emails", headers=headers, timeout=600.0)
            if response.ok:
                logger.info("send-all-pending: %s", response.json().get("message", "ok"))
            else:
                logger.warning("send-all-pending failed: %s", response.text)
        except requests.RequestException as exc:
            logger.warning("send-all-pending request error: %s", exc)

        time.sleep(interval)


@asynccontextmanager
async def lifespan(_: FastAPI):
    thread = threading.Thread(target=_clocking_loop, daemon=True)
    thread.start()
    yield


app = FastAPI(title="Clocking Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
