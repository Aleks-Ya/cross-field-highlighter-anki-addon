from typing import Optional, Callable, Any

from aqt.qt import QHBoxLayout, QLabel, Qt, QComboBox, QLineEdit


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

    def add_current_text_changed_callback(self, callback: Callable[[str], None]) -> None:
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentTextChanged.connect(callback)

    def set_items(self, items: list[str]) -> None:
        self.__combo_box.clear()
        self.__combo_box.addItems(items)

    def add_item(self, item: str, data: Any) -> None:
        self.__combo_box.addItem(item, data)

    def get_current_text(self) -> str:
        return self.__combo_box.currentText()

    def get_current_data(self) -> Any:
        return self.__combo_box.currentData()


class TitledLineEditLayout(QHBoxLayout):
    def __init__(self, title: str, text: str = None, placeholder: str = None, clear_button_enabled: bool = False):
        super().__init__()
        label: QLabel = QLabel(title)
        self.__line_edit: QLineEdit = QLineEdit(text)
        self.__line_edit.setPlaceholderText(placeholder)
        self.__line_edit.setClearButtonEnabled(clear_button_enabled)
        self.addWidget(label)
        self.addWidget(self.__line_edit)

    def get_text(self) -> str:
        return self.__line_edit.text()

    def set_text(self, text: str) -> None:
        self.__line_edit.setText(text)
