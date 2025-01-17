import logging
from logging import Logger
from typing import Callable, Optional

from aqt import QVBoxLayout, QCheckBox, QLabel, Qt, QPushButton, QIcon, QHBoxLayout, QWidget

from ....config.settings import Settings
from ....highlighter.types import FieldName, FieldNames

log: Logger = logging.getLogger(__name__)


class FieldsLayout(QVBoxLayout):
    def __init__(self, settings: Settings):
        super().__init__()
        self.__settings: Settings = settings
        self.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__select_all_button: QPushButton = self.__create_select_button(
            "select_all", self.__on_select_all_clicked, "Select <u>A</u>ll", "Alt+A")
        self.__select_none_button: QPushButton = self.__create_select_button(
            "select_none", self.__on_select_none_clicked, "Select <u>N</u>one", "Alt+N")
        select_buttons_layout: QHBoxLayout = self.__create_select_buttons_layout(self.__select_all_button,
                                                                                 self.__select_none_button)

        self.addLayout(select_buttons_layout)
        self.__field_name_checkboxes: dict[FieldName, QCheckBox] = {}
        self.__on_field_selected_callback: Optional[Callable[[FieldNames], None]] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __create_select_buttons_layout(self, select_all_button: QPushButton,
                                       select_none_button: QPushButton) -> QHBoxLayout:
        label: QLabel = QLabel("Fields:")
        layout: QHBoxLayout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(select_all_button)
        layout.addWidget(select_none_button)
        return layout

    def set_items(self, field_names: FieldNames) -> None:
        previous_in_focus: QWidget = self.__select_none_button
        for check_box in self.__field_name_checkboxes.values():
            self.removeWidget(check_box)
        self.__field_name_checkboxes.clear()
        for field_name in field_names:
            check_box: QCheckBox = QCheckBox(field_name)
            # noinspection PyUnresolvedReferences
            check_box.stateChanged.connect(self.__on_state_changed)
            self.addWidget(check_box)
            # noinspection PyUnresolvedReferences
            QWidget.setTabOrder(previous_in_focus, check_box)
            previous_in_focus = check_box
            self.__field_name_checkboxes[field_name] = check_box
        self.__enable_select_buttons()

    def set_selected_fields(self, field_names: FieldNames) -> None:
        for field_name, check_box in self.__field_name_checkboxes.items():
            check_box.blockSignals(True)
            check_box.setChecked(field_name in field_names)
            check_box.blockSignals(False)
        self.__enable_select_buttons()

    def set_disabled_fields(self, field_names: FieldNames) -> None:
        log.debug(f"Disable fields: {field_names}")
        for field_name, check_box in self.__field_name_checkboxes.items():
            check_box.blockSignals(True)
            disabled: bool = field_name in field_names
            check_box.setDisabled(disabled)
            check_box.blockSignals(False)

    def set_on_field_selected_callback(self, callback: Callable[[FieldNames], None]) -> None:
        self.__on_field_selected_callback = callback

    def __create_select_button(self, icon_name: str, on_click: Callable[[], None], tooltip: str,
                               shortcut: str) -> QPushButton:
        icon: QIcon = QIcon(str(self.__settings.module_dir / "ui" / "dialog" / "adhoc" / f"{icon_name}.png"))
        button: QPushButton = QPushButton()
        # noinspection PyUnresolvedReferences
        button.setToolTip(tooltip)
        button.setIcon(icon)
        button.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        # noinspection PyUnresolvedReferences
        button.setStyleSheet("QPushButton { padding: 0px; }")
        # noinspection PyUnresolvedReferences
        button.clicked.connect(on_click)
        button.setShortcut(shortcut)
        return button

    def __on_state_changed(self, _: int) -> None:
        self.__enable_select_buttons()
        if self.__on_field_selected_callback:
            selected_field_names: FieldNames = self.__get_selected_field_names()
            self.__on_field_selected_callback(selected_field_names)

    def __on_select_all_clicked(self) -> None:
        for check_box in self.__field_name_checkboxes.values():
            check_box.blockSignals(True)
            check_box.setChecked(True)
            check_box.blockSignals(False)
        self.__on_state_changed(0)

    def __on_select_none_clicked(self) -> None:
        for check_box in self.__field_name_checkboxes.values():
            check_box.blockSignals(True)
            check_box.setChecked(False)
            check_box.blockSignals(False)
        self.__on_state_changed(0)

    def __get_selected_field_names(self) -> FieldNames:
        return FieldNames([field_name for field_name, check_box in self.__field_name_checkboxes.items()
                           if check_box.isChecked()])

    def __enable_select_buttons(self) -> None:
        self.__select_all_button.setEnabled(True)
        self.__select_none_button.setEnabled(True)
        all_selected: bool = len(self.__get_selected_field_names()) == len(self.__field_name_checkboxes)
        if all_selected:
            self.__select_all_button.setEnabled(False)
        none_selected: bool = len(self.__get_selected_field_names()) == 0
        if none_selected:
            self.__select_none_button.setEnabled(False)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
