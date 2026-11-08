"""Open Chat AI Helper with a minimal host adapter."""

from __future__ import annotations

from typing import Any, Dict, Optional

from PyQt6.QtWidgets import QMessageBox, QWidget

from spock_shell.bridge_host import make_llm_client
from spock_shell.paths import SHIP_COMPUTER_DB, ensure_root_on_path


class _HelperHost:
    """Duck-typed stand-in for MainWindow bits ChatAIHelperWindow expects."""

    def __init__(self, config: Dict[str, Any], theme: Dict[str, str]):
        self.config = config
        self.theme = theme

    def _apply_ask_ai_provider_config(self) -> None:
        from spock_shell.bridge_host import apply_provider_config

        apply_provider_config(self.config)


def _ensure_docs_site(config: Dict[str, Any], parent: Optional[QWidget]) -> None:
    """Start pre-built site/ on docs_port (default :8000); open browser once."""
    try:
        from docs_server import ensure_docs_server
    except Exception as exc:
        print(f"Docs server unavailable: {exc}", file=__import__("sys").stderr)
        return

    result = ensure_docs_server(config=config, open_browser=True)
    url = str(result.get("url") or "http://127.0.0.1:8000")
    if result.get("ok"):
        print(f"Docs site running at {url} ({result.get('detail')})")
        return

    detail = str(result.get("detail") or "docs server failed")
    print(f"Warning: docs site not available at {url}: {detail}")
    if parent is not None:
        QMessageBox.warning(
            parent,
            "AI Helper docs",
            f"Could not serve site/ at {url}.\n\n{detail}",
        )


def open_ai_helper(
    parent: Optional[QWidget],
    theme: Dict[str, str],
    config: Dict[str, Any],
) -> Optional[QWidget]:
    ensure_root_on_path()
    try:
        from chat_ai_helper import ChatAIHelperWindow
        from WarpCore.search import embeddings_endpoint_ok as _emb_ok
        from WarpCore.search import hybrid_search

        _ensure_docs_site(config, parent)

        host = _HelperHost(config, theme)

        def llm_factory():
            return make_llm_client(config)

        def embeddings_ok(url: str = "", timeout: float = 1.0, light: bool = False, **_kwargs):
            return _emb_ok(url or None, timeout=timeout, light=light)

        win = ChatAIHelperWindow(
            theme=theme,
            main_window=host,
            llm_client_factory=llm_factory,
            hybrid_search_fn=hybrid_search,
            embeddings_ok_fn=embeddings_ok,
            db_path=SHIP_COMPUTER_DB,
            parent=None,
        )
        win.show()
        win.raise_()
        return win
    except Exception as e:
        if parent is not None:
            QMessageBox.critical(parent, "AI Helper", f"Could not open AI Helper:\n{e}")
        else:
            print(f"Could not open AI Helper: {e}", file=__import__("sys").stderr)
        return None
