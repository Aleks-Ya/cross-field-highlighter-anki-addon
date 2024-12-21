import logging
from logging import Logger
from typing import Callable, Optional

from aqt import QVBoxLayout, QCheckBox, QLabel, Qt

from ....highlighter.types import FieldName, FieldNames

log: Logger = logging.getLogger(__name__)


class FieldsLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        label: QLabel = QLabel("Fields:")
        self.addWidget(label)
        self.__field_name_checkboxes: dict[FieldName, QCheckBox] = {}
        self.__on_field_selected_callback: Optional[Callable[[FieldNames], None]] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def set_items(self, field_names: FieldNames) -> None:
        for check_box in self.__field_name_checkboxes.values():
            self.removeWidget(check_box)
        self.__field_name_checkboxes.clear()
        for field_name in field_names:
            check_box: QCheckBox = QCheckBox(field_name)
            # noinspection PyUnresolvedReferences
            check_box.stateChanged.connect(self.__on_state_changed)
            self.addWidget(check_box)
            self.__field_name_checkboxes[field_name] = check_box

    def set_selected_fields(self, field_names: FieldNames) -> None:
        for field_name, check_box in self.__field_name_checkboxes.items():
            check_box.blockSignals(True)
            check_box.setChecked(field_name in field_names)
            check_box.blockSignals(False)

    def set_disabled_fields(self, field_names: FieldNames):
        log.debug(f"Disable fields: {field_names}")
        for field_name, check_box in self.__field_name_checkboxes.items():
            check_box.blockSignals(True)
            disabled: bool = field_name in field_names
            check_box.setDisabled(disabled)
            if disabled:
                check_box.setChecked(False)
            check_box.blockSignals(False)

    def set_on_field_selected_callback(self, callback: Callable[[FieldNames], None]):
        self.__on_field_selected_callback = callback

    def __on_state_changed(self, _: int):
        if self.__on_field_selected_callback:
            selected_field_names: FieldNames = FieldNames(
                [field_name for field_name, check_box in self.__field_name_checkboxes.items() if check_box.isChecked()])
            self.__on_field_selected_callback(selected_field_names)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
