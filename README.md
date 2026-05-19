# aiomultiprocess-loadtest

Example comparing async I/O, [aiomultiprocess](https://github.com/jreese/aiomultiprocess), and threads — including on [Python 3.14 free-threaded](https://docs.python.org/3/howto/free-threading-python.html) builds (GIL optional).

## Setup

Requires [uv](https://docs.astral.sh/uv/). The project is pinned to the **free-threaded** 3.14 build (see `.python-version`).

```bash
uv sync
```

Verify the interpreter:

```bash
uv run python -c "import sys; print(sys.version); print('GIL enabled:', sys._is_gil_enabled())"
```

You should see `free-threading build` and `GIL enabled: False` before importing extension modules that are not GIL-safe.

### Standard (GIL) vs free-threaded

| Build | Pin | GIL |
|-------|-----|-----|
| Free-threaded (default for this repo) | `uv python pin 3.14t` | Off at startup; see note below |
| Standard | `uv python pin 3.14` | Always on |

After changing the pin, run `uv sync` to recreate `.venv`.

### Free-threading caveats

- **C extensions** must ship free-threaded wheels or uv builds them from source (slower `uv sync`). `httptools` is built from source on this platform.
- Some packages **re-enable the GIL** when imported if they have not declared GIL compatibility (e.g. `ujson` warns and enables the GIL). `loadtest.py` prints GIL status before and after such imports.
- To keep the GIL disabled despite that (unsafe): `PYTHON_GIL=0 uv run python loadtest/loadtest.py` or `uv run python -Xgil=0 loadtest/loadtest.py`.
- Thread-heavy code can expose races that the GIL previously hid; use locks or message passing for shared mutable state.

## Test

Integration tests run against a minimal stdlib test server (`loadtest/test_server.py`):

```bash
make test          # start server, run pytest, stop server
make server        # run test server only (foreground, port 18080)
make test-pytest   # pytest only (server must already be running)
```

CI runs `make test` on push/PR via [`.github/workflows/test.yml`](.github/workflows/test.yml).

## Run (manual benchmark)

Start the example API (terminal 1):

```bash
uv run python loadtest/example_api.py
```

Run the load test (terminal 2):

```bash
uv run python loadtest/loadtest.py
```

The script runs three modes in order:

1. **async** — `asyncio` + `aiohttp`
2. **aiomultiprocess** — process pool + async workers
3. **threaded** — `ThreadPoolExecutor` + sync `httpx` (meaningful comparison on free-threaded Python)
