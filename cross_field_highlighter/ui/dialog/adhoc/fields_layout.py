from aqt import QVBoxLayout, QCheckBox, QLabel

from cross_field_highlighter.highlighter.types import FieldName


class FieldsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        label: QLabel = QLabel("Fields:")
        self.addWidget(label)
        self.__field_name_checkboxes: dict[FieldName, QCheckBox] = {}

    def set_items(self, field_names: list[FieldName]) -> None:
        for check_box in self.__field_name_checkboxes:
            self.removeWidget(check_box)
        self.__field_name_checkboxes.clear()
        for field_name in field_names:
            check_box: QCheckBox = QCheckBox(field_name)
            self.addWidget(check_box)
            self.__field_name_checkboxes[field_name] = check_box

    def get_selected_field_names(self) -> list[FieldName]:
        return [field_name for field_name, check_box in self.__field_name_checkboxes.items() if check_box.isChecked()]
