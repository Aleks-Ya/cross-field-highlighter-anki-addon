import logging
from logging import Logger
from typing import Callable, Any

from aqt.qt import QHBoxLayout, QLabel, Qt, QComboBox

log: Logger = logging.getLogger(__name__)


class TitledComboBoxLayout(QHBoxLayout):
    def __init__(self, title: str):
        super().__init__()
        label: QLabel = QLabel(title)
        self.__combo_box: QComboBox = QComboBox(None)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(label)
        self.addWidget(self.__combo_box, stretch=1)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def set_current_text(self, current_text: str) -> None:
        self.__combo_box.blockSignals(True)
        self.__combo_box.setCurrentText(current_text)
        self.__combo_box.blockSignals(False)

    def add_current_index_changed_callback(self, callback: Callable[[int], None]) -> None:
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentIndexChanged.connect(callback)

    def add_current_text_changed_callback(self, callback: Callable[[str], None]) -> None:
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentTextChanged.connect(callback)

    def set_items(self, items: list[str]) -> None:
        self.__combo_box.blockSignals(True)
        self.__combo_box.clear()
        self.__combo_box.addItems(items)
        self.__combo_box.blockSignals(False)

    def set_data_items(self, items: dict[str, Any]) -> None:
        self.__combo_box.blockSignals(True)
        current_item: object = self.get_current_data()
        self.__combo_box.clear()
        for item, data in items.items():
            self.__combo_box.addItem(item, data)
        if current_item in items.values():
            index: int = list(items.values()).index(current_item)
            self.__combo_box.setCurrentIndex(index)
        self.__combo_box.blockSignals(False)

    def get_current_text(self) -> str:
        return self.__combo_box.currentText()

    def get_current_data(self) -> Any:
        return self.__combo_box.currentData()

    def on_current_text_changed(self, callback: Callable[[str], None]) -> None:
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentTextChanged.connect(callback)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
