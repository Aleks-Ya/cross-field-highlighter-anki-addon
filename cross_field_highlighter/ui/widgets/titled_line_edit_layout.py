import logging
from logging import Logger
from typing import Optional, Callable

from aqt.qt import QHBoxLayout, QLabel, QLineEdit

from ...highlighter.types import Text

log: Logger = logging.getLogger(__name__)


class TitledLineEditLayout(QHBoxLayout):
    def __init__(self, title: str, text: str = None, placeholder: str = None, clear_button_enabled: bool = False):
        super().__init__()
        label: QLabel = QLabel(title)
        self.__line_edit: QLineEdit = QLineEdit(text)
        self.__line_edit.setPlaceholderText(placeholder)
        self.__line_edit.setClearButtonEnabled(clear_button_enabled)
        # noinspection PyUnresolvedReferences
        self.__line_edit.textChanged.connect(self.__on_state_changed)
        self.addWidget(label)
        self.addWidget(self.__line_edit, stretch=1)
        self.__on_text_changed_callback: Optional[Callable[[Text], None]] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def set_text(self, text: str) -> None:
        self.__line_edit.blockSignals(True)
        self.__line_edit.setText(text)
        self.__line_edit.blockSignals(False)

    def set_on_text_changed_callback(self, callback: Callable[[Text], None]):
        self.__on_text_changed_callback = callback

    def __on_state_changed(self, text: str):
        if self.__on_text_changed_callback:
            self.__on_text_changed_callback(Text(text))

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
