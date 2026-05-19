"""Block until TEST_BASE_URL responds with HTTP 200."""

from __future__ import annotations

import os
import sys
import time

import httpx

URL = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:18080")
TIMEOUT = float(os.environ.get("TEST_SERVER_WAIT_TIMEOUT", "15"))


def main() -> None:
    deadline = time.monotonic() + TIMEOUT
    while time.monotonic() < deadline:
        try:
            response = httpx.get(URL, timeout=1.0)
            if response.status_code == 200:
                print(f"server ready: {URL}", flush=True)
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.2)
    print(f"server not ready after {TIMEOUT}s: {URL}", file=sys.stderr, flush=True)
    sys.exit(1)


if __name__ == "__main__":
    main()
