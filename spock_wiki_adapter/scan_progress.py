"""Reusable Wiki Scan progress panel (wiki_agent_status refresh cadence)."""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class WikiScanProgressWidget(QWidget):
    """Live ingest progress — polls ``collect_status_snapshot`` ~1 Hz by default."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        interval_ms: int = 1000,
        auto_start: bool = True,
    ) -> None:
        super().__init__(parent)
        self._interval_ms = max(500, int(interval_ms))
        self._build()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh)
        if auto_start:
            self.start()

    def _build(self) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        head = QHBoxLayout()
        title = QLabel("Wiki Scan progress")
        f = QFont()
        f.setBold(True)
        title.setFont(f)
        title.setStyleSheet("color: #FF9800;")
        head.addWidget(title)
        head.addStretch()
        self._live_lbl = QLabel("STANDBY")
        self._live_lbl.setStyleSheet("color: #C9A227; font-weight:700;")
        head.addWidget(self._live_lbl)
        lay.addLayout(head)

        self._bar = QProgressBar()
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        self._bar.setTextVisible(True)
        self._bar.setFormat("%p%")
        self._bar.setMinimumHeight(22)
        self._bar.setStyleSheet(
            "QProgressBar { border:1px solid #2c3e4a; border-radius:4px; "
            "background:#12171c; text-align:center; color:#E6EEF2; }"
            "QProgressBar::chunk { background:#5C6BC0; border-radius:3px; }"
        )
        lay.addWidget(self._bar)

        self._detail = QLabel("Idle — start a Wiki Scan to see live ingest progress.")
        self._detail.setWordWrap(True)
        self._detail.setStyleSheet(
            "QLabel { background:#0f1419; color:#E6EEF2; border:1px solid #2c3e4a; "
            "border-radius:4px; padding:8px; font-family: Consolas, monospace; }"
        )
        self._detail.setMinimumHeight(120)
        lay.addWidget(self._detail, 1)

    def start(self) -> None:
        if not self._timer.isActive():
            self._timer.start(self._interval_ms)
        self.refresh()

    def stop(self) -> None:
        self._timer.stop()

    def set_interval_ms(self, ms: int) -> None:
        self._interval_ms = max(500, int(ms))
        if self._timer.isActive():
            self._timer.setInterval(self._interval_ms)

    def refresh(self) -> None:
        try:
            from wiki_agent_status import collect_status_snapshot

            snap = collect_status_snapshot()
        except Exception as e:
            self._live_lbl.setText("ERROR")
            self._live_lbl.setStyleSheet("color: #E57373; font-weight:700;")
            self._detail.setText(f"Status refresh failed:\n{e}")
            return

        if not snap.get("ok"):
            self._live_lbl.setText("NO DB")
            self._bar.setValue(0)
            self._detail.setText(str(snap.get("summary") or snap.get("error") or "—"))
            return

        pct = int(snap.get("pct") or 0)
        self._bar.setValue(max(0, min(100, pct)))
        alive = bool(snap.get("alive"))
        active = int(snap.get("pending") or 0) + int(snap.get("running") or 0)
        if alive and active:
            self._live_lbl.setText("SCANNING")
            self._live_lbl.setStyleSheet("color: #81C784; font-weight:700;")
        elif alive:
            self._live_lbl.setText("AGENT IDLE")
            self._live_lbl.setStyleSheet("color: #C9A227; font-weight:700;")
        else:
            self._live_lbl.setText("STANDBY")
            self._live_lbl.setStyleSheet("color: #90A4AE; font-weight:700;")
        self._detail.setText(str(snap.get("summary") or ""))
