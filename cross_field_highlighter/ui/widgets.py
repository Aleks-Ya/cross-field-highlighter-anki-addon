from typing import Optional, Callable, Any

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

    def add_current_text_changed_callback(self, callback: Callable[[Any], None]) -> None:
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentTextChanged.connect(callback)

    def set_items(self, items: list[str]) -> None:
        self.__combo_box.clear()
        self.__combo_box.addItems(items)
