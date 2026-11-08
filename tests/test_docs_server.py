"""Docs site server ensure() unit tests."""

from __future__ import annotations

import socket
import tempfile
from pathlib import Path

from docs_server import docs_http_ok, ensure_docs_server, site_ready


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def test_site_ready_false_for_empty():
    with tempfile.TemporaryDirectory() as tmp:
        assert site_ready(Path(tmp)) is False


def test_ensure_docs_server_serves_index():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "index.html").write_text(
            "<html><body>spock-docs-ok</body></html>", encoding="utf-8"
        )
        port = _free_port()
        result = ensure_docs_server(
            port=port, site_dir=root, open_browser=False, config={"docs_port": port}
        )
        assert result["ok"] is True
        assert result["started"] is True
        assert docs_http_ok(result["url"])

        again = ensure_docs_server(
            port=port, site_dir=root, open_browser=False, config={"docs_port": port}
        )
        assert again["ok"] is True
        assert again["started"] is False


if __name__ == "__main__":
    test_site_ready_false_for_empty()
    test_ensure_docs_server_serves_index()
    print("ok")
