from PyQtPath.path_chain_pyqt6 import path
from aqt import QDialogButtonBox, QPushButton, Qt, QComboBox, QCheckBox

from cross_field_highlighter.highlighter.types import FieldName
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.widgets.note_type_combo_box_layout import NoteTypeComboBoxLayout
from tests.visual_qtbot import VisualQtBot


class AdhocEraseDialogViewScaffold:
    def __init__(self, view: AdhocEraseDialogView, visual_qtbot: VisualQtBot):
        self.__view = view
        self.__visual_qtbot = visual_qtbot

    def select_note_type(self, *keys: Qt.Key) -> None:
        note_type_combo_box: QComboBox = self.__get_note_type_combo_box()
        self.__visual_qtbot.mouse_click(note_type_combo_box, Qt.MouseButton.LeftButton)
        for key in keys:
            self.__visual_qtbot.key_click(note_type_combo_box, key)
        self.__visual_qtbot.key_click(note_type_combo_box.view(), Qt.Key.Key_Enter)

    def mark_destination_field(self, field_name: FieldName) -> None:
        checkboxes: list[QCheckBox] = path(self.__view).child(FieldsLayout).children(QCheckBox)
        for check_box in checkboxes:
            if check_box.text() == field_name:
                self.__visual_qtbot.mouse_click(check_box, Qt.MouseButton.LeftButton)
                # Mouse click just focus on check_box, but doesn't select it
                self.__visual_qtbot.key_click(check_box, Qt.Key.Key_Space)
                return
        raise AssertionError(f"Field '{field_name}' not found")

    def click_start_button(self) -> None:
        self.__click_button(self.__get_start_button())

    def click_cancel_button(self) -> None:
        self.__click_button(self.__get_cancel_button())

    def click_restore_defaults_button(self) -> None:
        self.__click_button(self.__get_restore_defaults_button())

    def press_esc(self) -> None:
        self.__visual_qtbot.key_click(self.__view, Qt.Key.Key_Escape)

    def __get_note_type_combo_box(self) -> QComboBox:
        return path(self.__view).child(NoteTypeComboBoxLayout).combobox().get()

    def __get_start_button(self) -> QPushButton:
        return self.__get_button(QDialogButtonBox.StandardButton.Ok)

    def __get_cancel_button(self) -> QPushButton:
        return self.__get_button(QDialogButtonBox.StandardButton.Cancel)

    def __get_restore_defaults_button(self) -> QPushButton:
        return self.__get_button(QDialogButtonBox.StandardButton.RestoreDefaults)

    def __click_button(self, button: QPushButton) -> None:
        self.__visual_qtbot.mouse_click(button, Qt.MouseButton.LeftButton)

    def __get_button(self, button: QDialogButtonBox.StandardButton) -> QPushButton:
        button_box: QDialogButtonBox = path(self.__view).child(QDialogButtonBox).get()
        return button_box.button(button)
