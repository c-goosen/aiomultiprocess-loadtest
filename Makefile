UV ?= uv
HOST ?= 127.0.0.1
PORT ?= 18080
TEST_BASE_URL ?= http://$(HOST):$(PORT)
TEST_REQ_NUM ?= 20

export TEST_BASE_URL
export TEST_SERVER_HOST := $(HOST)
export TEST_SERVER_PORT := $(PORT)
export TEST_REQ_NUM

.PHONY: help install sync server wait-server test test-pytest clean

help:
	@echo "Targets:"
	@echo "  install   Install runtime + dev dependencies (uv sync)"
	@echo "  server    Run the test HTTP server (foreground)"
	@echo "  test      Start test server, run pytest, then stop server"
	@echo "  test-pytest  Run pytest only (server must already be running)"
	@echo "  clean     Remove pytest and Python caches"

install sync:
	$(UV) sync --group dev

server:
	$(UV) run python loadtest/test_server.py --host $(HOST) --port $(PORT)

wait-server:
	$(UV) run python scripts/wait_for_server.py

test-pytest:
	$(UV) run pytest tests/ -v

test: install
	@set -e; \
	$(UV) run python loadtest/test_server.py --host $(HOST) --port $(PORT) & \
	pid=$$!; \
	trap 'kill $$pid 2>/dev/null || true' EXIT INT TERM; \
	$(MAKE) wait-server; \
	$(MAKE) test-pytest; \
	echo "tests passed"

clean:
	rm -rf .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
