from typing import Optional, Callable

from PyQt6.QtWidgets import QLineEdit
from aqt.qt import QHBoxLayout, QLabel, Qt, QComboBox


class TitledComboBoxLayout(QHBoxLayout):
    def __init__(self, title: str, items: Optional[list[str]] = None):
        super().__init__()
        label: QLabel = QLabel(title)
        self.__combo_box: QComboBox = QComboBox(None)
        if items:
            self.__combo_box.addItems(items)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(label)
        self.addWidget(self.__combo_box)

    def set_current_text(self, current_text: str) -> None:
        self.__combo_box.setCurrentText(current_text)

    def add_current_index_changed_callback(self, callback: Callable[[int], None]) -> None:
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentIndexChanged.connect(callback)

    def set_items(self, items: list[str]) -> None:
        self.__combo_box.clear()
        self.__combo_box.addItems(items)


class TitledLineEditLayout(QHBoxLayout):
    def __init__(self, title: str, text: str = None, placeholder: str = None, clear_button_enabled: bool = False):
        super().__init__()
        label: QLabel = QLabel(title)
        line_edit: QLineEdit = QLineEdit(text)
        line_edit.setPlaceholderText(placeholder)
        line_edit.setClearButtonEnabled(clear_button_enabled)
        self.addWidget(label)
        self.addWidget(line_edit)
