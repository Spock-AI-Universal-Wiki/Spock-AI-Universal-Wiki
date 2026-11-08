"""Pre-built mkdocs site server — serves ./site (port from config / SPOCK_DOCS_PORT).

Uses Python stdlib http.server (ThreadingHTTPServer).
"""

from __future__ import annotations

import http.server
import socket
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

_HERE = Path(__file__).resolve().parent
SITE_DIR = _HERE / "site"

try:
    from WarpCore.service_endpoints import DEFAULT_DOCS_PORT, resolve_ports
except ImportError:  # pragma: no cover
    DEFAULT_DOCS_PORT = 8000

    def resolve_ports(cfg=None):
        return {"docs": DEFAULT_DOCS_PORT}


_lock = threading.Lock()
_active: Optional["DocsServer"] = None


class _DocsHandler(http.server.SimpleHTTPRequestHandler):
    """Serves static files from the pre-built mkdocs site directory."""

    def __init__(self, *args, directory: str = "", **kwargs):
        super().__init__(*args, directory=directory or str(SITE_DIR), **kwargs)

    def log_message(self, format: str, *args) -> None:
        pass

    def handle_one_request(self) -> None:
        try:
            super().handle_one_request()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            pass

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self) -> None:
        root = Path(getattr(self, "directory", None) or SITE_DIR)
        parsed = self.path.split("?", 1)[0]
        target = root / parsed.lstrip("/")

        if target.is_dir():
            index = target / "index.html"
            if index.exists():
                self.path = parsed.rstrip("/") + "/index.html"

        if not target.exists() and not (root / parsed.lstrip("/")).exists():
            fallback = root / "index.html"
            if fallback.exists():
                self.path = "/index.html"

        super().do_GET()


class DocsServer:
    """Lightweight docs server for the pre-built site."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: Optional[int] = None,
        site_dir: Optional[Path] = None,
        config: Optional[dict] = None,
    ):
        self.host = host
        if port is None:
            port = int(resolve_ports(config).get("docs", DEFAULT_DOCS_PORT))
        self.port = int(port)
        self.site_dir = Path(site_dir) if site_dir else SITE_DIR
        self._server: Optional[http.server.ThreadingHTTPServer] = None
        self._thread: Optional[threading.Thread] = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def _make_handler(self, *args, **kwargs):
        return _DocsHandler(*args, directory=str(self.site_dir), **kwargs)

    def start_background(self) -> None:
        """Start server in a daemon thread."""
        if self._server is not None:
            return
        self._server = http.server.ThreadingHTTPServer(
            (self.host, self.port), self._make_handler
        )
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def serve_forever(self) -> None:
        """Block and serve (non-background)."""
        self._server = http.server.ThreadingHTTPServer(
            (self.host, self.port), self._make_handler
        )
        print(f"Spock AI Helper docs: {self.url}")
        try:
            self._server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down docs server.")
            self._server.shutdown()

    def shutdown(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server = None


def site_ready(site_dir: Optional[Path] = None) -> bool:
    root = Path(site_dir) if site_dir else SITE_DIR
    return root.is_dir() and (root / "index.html").is_file()


def docs_http_ok(url: str, timeout: float = 0.6) -> bool:
    """True when ``url`` answers HTTP 200 (our static index or equivalent)."""
    target = url.rstrip("/") + "/"
    try:
        # HEAD avoids downloading site/index.html (~150KB) on every probe.
        req = urllib.request.Request(target, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= int(resp.status) < 300
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        try:
            req = urllib.request.Request(target, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                ok = 200 <= int(resp.status) < 300
                try:
                    resp.read()
                except Exception:
                    pass
                return ok
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            return False


def _port_free(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
            return True
        except OSError:
            return False


def ensure_docs_server(
    *,
    config: Optional[dict] = None,
    port: Optional[int] = None,
    site_dir: Optional[Path] = None,
    open_browser: bool = False,
) -> Dict[str, Any]:
    """Idempotently serve pre-built ``site/`` for AI Helper / Bringup Menu.

    Returns ``{ok, url, started, detail}``. Safe to call from multiple suite
    entry points; only one background server is kept per process.
    """
    global _active

    try:
        from WarpCore.service_endpoints import docs_base_url

        url = docs_base_url(config) if port is None else f"http://127.0.0.1:{int(port)}"
    except Exception:
        resolved = int(port) if port is not None else int(
            resolve_ports(config).get("docs", DEFAULT_DOCS_PORT)
        )
        url = f"http://127.0.0.1:{resolved}"

    host = "127.0.0.1"
    try:
        port_i = int(port) if port is not None else int(
            resolve_ports(config).get("docs", DEFAULT_DOCS_PORT)
        )
    except (TypeError, ValueError):
        port_i = int(DEFAULT_DOCS_PORT)

    root = Path(site_dir) if site_dir else SITE_DIR
    if not site_ready(root):
        return {
            "ok": False,
            "url": url,
            "started": False,
            "detail": f"site/ not found or empty at {root} (build with: mkdocs build)",
        }

    if docs_http_ok(url):
        # External or prior listener already up — open browser once for discovery.
        if open_browser:
            _maybe_open_browser(url)
        return {
            "ok": True,
            "url": url,
            "started": False,
            "detail": "already serving",
        }

    with _lock:
        if _active is not None and _active.port == port_i and docs_http_ok(url):
            # Same process already owns the docs server; do not reopen browser.
            return {
                "ok": True,
                "url": url,
                "started": False,
                "detail": "already started in this process",
            }

        if not _port_free(host, port_i):
            detail = (
                f"port {port_i} is in use but does not serve the Spock docs site. "
                "Free it or change docs_port / SPOCK_DOCS_PORT."
            )
            return {
                "ok": False,
                "url": url,
                "started": False,
                "detail": detail,
            }

        server = DocsServer(
            host=host, port=port_i, site_dir=root, config=config
        )
        try:
            server.start_background()
        except OSError as exc:
            return {
                "ok": False,
                "url": url,
                "started": False,
                "detail": f"could not bind docs server: {exc}",
            }
        _active = server

    # Brief wait so the first browser hit does not race the bind.
    for _ in range(20):
        if docs_http_ok(url, timeout=0.2):
            break
        threading.Event().wait(0.05)

    if not docs_http_ok(url):
        return {
            "ok": False,
            "url": url,
            "started": True,
            "detail": "docs server started but HTTP check failed",
        }

    if open_browser:
        _maybe_open_browser(url)
    return {
        "ok": True,
        "url": url,
        "started": True,
        "detail": "started",
    }


def _maybe_open_browser(url: str) -> None:
    def _open() -> None:
        import time

        time.sleep(0.4)
        try:
            from spock_shell.open_url import open_url

            open_url(url)
        except Exception:
            pass

    threading.Thread(target=_open, daemon=True).start()


def main() -> int:
    port = None
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass

    server = DocsServer(port=port)
    if not SITE_DIR.exists() or not (SITE_DIR / "index.html").exists():
        print(f"Warning: site/ directory not found or empty at {SITE_DIR}")
        print("Build with: mkdocs build (from the Spock-Onboarding root)")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
