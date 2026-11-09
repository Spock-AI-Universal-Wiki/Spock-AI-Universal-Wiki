"""Non-modal Wiki Scan filter + live progress dialog."""

from __future__ import annotations

from typing import Callable, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from spock_wiki_adapter.scan_filters import (
    PRESET_ALL,
    env_value_for_preset,
    preset_choices,
)
from spock_wiki_adapter.scan_progress import WikiScanProgressWidget


def _btn(text: str, bg: str) -> QPushButton:
    b = QPushButton(text)
    b.setStyleSheet(
        f"QPushButton {{ background:{bg}; color:#FFFFFF; padding:10px 16px; "
        f"border:none; border-radius:4px; font-weight:bold; }}"
        f"QPushButton:disabled {{ background:#555; color:#999; }}"
    )
    return b


class WikiScanOptionsDialog(QDialog):
    """Filter radios + Start/Stop; stays open during scan with live progress."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        on_start: Optional[Callable[[str, bool], None]] = None,
        on_stop: Optional[Callable[[], None]] = None,
        continuous_default: bool = False,
    ) -> None:
        super().__init__(parent)
        self._on_start = on_start
        self._on_stop = on_stop
        self.setWindowTitle("Wiki Scan — Filter & Progress")
        self.setModal(False)
        self.setMinimumSize(560, 520)
        self.resize(620, 580)
        self.setWindowFlag(Qt.WindowType.Window, True)
        self._build(continuous_default)
        self.set_running(False)

    def _build(self, continuous_default: bool) -> None:
        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 14, 14, 14)
        lay.setSpacing(10)

        title = QLabel("Wiki Scan filter")
        f = QFont()
        f.setPointSize(13)
        f.setBold(True)
        title.setFont(f)
        title.setStyleSheet("color: #FF9800;")
        lay.addWidget(title)

        tip = QLabel(
            "Choose what to ingest, then Start Scan. This window stays open and "
            "shows live progress (same accounting as Embedding Status)."
        )
        tip.setWordWrap(True)
        tip.setStyleSheet("color: #8aa0ad;")
        lay.addWidget(tip)

        self._group = QButtonGroup(self)
        self._radios: dict[str, QRadioButton] = {}
        self._hint = QLabel("")
        self._hint.setWordWrap(True)
        self._hint.setStyleSheet("color: #90A4AE;")

        for i, (preset_id, label, hint) in enumerate(preset_choices()):
            radio = QRadioButton(label)
            radio.setProperty("preset_id", preset_id)
            radio.setProperty("preset_hint", hint)
            self._group.addButton(radio, i)
            self._radios[preset_id] = radio
            lay.addWidget(radio)
            radio.toggled.connect(self._on_radio)

        default = self._radios[PRESET_ALL]
        default.setChecked(True)
        self._hint.setText(default.property("preset_hint") or "")
        lay.addWidget(self._hint)

        self.continuous = QCheckBox("Continuous watch (until Stop Scan)")
        self.continuous.setChecked(bool(continuous_default))
        self.continuous.setToolTip(
            "Off (default): scan once — exit when the queue is idle.\n"
            "On: keep the watcher running until Stop Scan."
        )
        lay.addWidget(self.continuous)

        row = QHBoxLayout()
        self.start_btn = _btn("Start Scan", "#5C6BC0")
        self.stop_btn = _btn("Stop Scan", "#C44A4A")
        self.close_btn = _btn("Close", "#546E7A")
        self.start_btn.clicked.connect(self._start_clicked)
        self.stop_btn.clicked.connect(self._stop_clicked)
        self.close_btn.clicked.connect(self.close)
        row.addWidget(self.start_btn)
        row.addWidget(self.stop_btn)
        row.addStretch()
        row.addWidget(self.close_btn)
        lay.addLayout(row)

        self.progress = WikiScanProgressWidget(self, interval_ms=1000, auto_start=True)
        lay.addWidget(self.progress, 1)

        self.setStyleSheet(
            "QDialog, QWidget { background:#1a1f24; color:#E6EEF2; }"
            "QRadioButton { spacing:8px; padding:4px 0; }"
            "QCheckBox { padding:4px 0; }"
        )

    def _on_radio(self, checked: bool) -> None:
        if not checked:
            return
        btn = self.sender()
        if isinstance(btn, QRadioButton):
            self._hint.setText(str(btn.property("preset_hint") or ""))

    def selected_preset(self) -> str:
        for preset_id, radio in self._radios.items():
            if radio.isChecked():
                return preset_id
        return PRESET_ALL

    def selected_extensions_env(self) -> str:
        return env_value_for_preset(self.selected_preset())

    def continuous_checked(self) -> bool:
        return bool(self.continuous.isChecked())

    def set_running(self, running: bool) -> None:
        for radio in self._radios.values():
            radio.setEnabled(not running)
        self.continuous.setEnabled(not running)
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)
        if running:
            self.progress.start()

    def _start_clicked(self) -> None:
        if self._on_start:
            self._on_start(self.selected_extensions_env(), self.continuous_checked())

    def _stop_clicked(self) -> None:
        if self._on_stop:
            self._on_stop()

    def closeEvent(self, event) -> None:  # noqa: N802
        # Keep polling elsewhere (Live Monitor); stop only this dialog's timer.
        self.progress.stop()
        super().closeEvent(event)
