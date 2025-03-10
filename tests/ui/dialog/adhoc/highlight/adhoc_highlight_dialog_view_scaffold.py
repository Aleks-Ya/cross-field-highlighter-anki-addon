from PyQtPath.path_chain_pyqt6 import path
from aqt import QComboBox, QDialogButtonBox, QPushButton, Qt, QCheckBox, QLineEdit

from cross_field_highlighter.highlighter.types import FieldName
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.adhoc.highlight.format_group_box import FormatGroupBox
from cross_field_highlighter.ui.widgets.note_type_combo_box_layout import NoteTypeComboBoxLayout
from cross_field_highlighter.ui.widgets.titled_combo_box_layout import TitledComboBoxLayout
from cross_field_highlighter.ui.widgets.titled_line_edit_layout import TitledLineEditLayout
from tests.visual_qtbot import VisualQtBot


class AdhocHighlightDialogViewScaffold:
    def __init__(self, view: AdhocHighlightDialogView, visual_qtbot: VisualQtBot):
        self.__view = view
        self.__visual_qtbot = visual_qtbot

    def select_note_type(self, *keys: Qt.Key) -> None:
        note_type_combo_box: QComboBox = self.__get_note_type_combo_box()
        for key in keys:
            self.__visual_qtbot.key_click(note_type_combo_box, key)
        self.__visual_qtbot.key_click(note_type_combo_box.view(), Qt.Key.Key_Enter)

    def select_source_field(self, *keys: Qt.Key) -> None:
        source_field_combo_box: QComboBox = self.__get_source_field_combo_box()
        for key in keys:
            self.__visual_qtbot.key_click(source_field_combo_box, key)
        self.__visual_qtbot.key_click(source_field_combo_box.view(), Qt.Key.Key_Enter)

    def select_format(self, *keys: Qt.Key) -> None:
        format_combo_box: QComboBox = self.__get_format_combo_box()
        for key in keys:
            self.__visual_qtbot.key_click(format_combo_box, key)
        self.__visual_qtbot.key_click(format_combo_box.view(), Qt.Key.Key_Enter)

    def mark_destination_field(self, field_name: FieldName) -> None:
        checkboxes: list[QCheckBox] = path(self.__view).child(FieldsLayout).children(QCheckBox)
        for check_box in checkboxes:
            if check_box.text() == field_name:
                old: bool = check_box.isChecked()
                self.__visual_qtbot.mouse_click(check_box, Qt.MouseButton.LeftButton)
                if check_box.isChecked() == old:
                    # Mouse click just focus on check_box, but doesn't select it
                    self.__visual_qtbot.key_click(check_box, Qt.Key.Key_Space)
                return
        raise AssertionError(f"Field '{field_name}' not found")

    def print_to_stop_words(self, stop_words: str) -> None:
        stop_words_line_edit: QLineEdit = self.__get_stop_words_line_edit()
        self.__visual_qtbot.key_clicks(stop_words_line_edit, stop_words)

    def click_start_button(self) -> None:
        self.__click_button(self.__get_start_button())

    def click_cancel_button(self) -> None:
        self.__click_button(self.__get_cancel_button())

    def click_restore_defaults_button(self) -> None:
        self.__click_button(self.__get_restore_defaults_button())

    def press_esc(self) -> None:
        self.__visual_qtbot.key_click(self.__view, Qt.Key.Key_Escape)

    def __get_note_type_combo_box(self) -> QComboBox:
        return path(self.__view).group().child(NoteTypeComboBoxLayout).combobox().get()

    def __get_source_field_combo_box(self) -> QComboBox:
        return path(self.__view).group().child(TitledComboBoxLayout).combobox().get()

    def __get_format_combo_box(self) -> QComboBox:
        return path(self.__view).child(FormatGroupBox).child(TitledComboBoxLayout).combobox().get()

    def __click_button(self, button: QPushButton) -> None:
        self.__visual_qtbot.mouse_click(button, Qt.MouseButton.LeftButton)

    def __get_start_button(self) -> QPushButton:
        return self.__get_button(QDialogButtonBox.StandardButton.Ok)

    def __get_cancel_button(self) -> QPushButton:
        return self.__get_button(QDialogButtonBox.StandardButton.Cancel)

    def __get_restore_defaults_button(self) -> QPushButton:
        return self.__get_button(QDialogButtonBox.StandardButton.RestoreDefaults)

    def __get_button(self, button: QDialogButtonBox.StandardButton) -> QPushButton:
        button_box: QDialogButtonBox = path(self.__view).child(QDialogButtonBox).get()
        return button_box.button(button)

    def __get_stop_words_line_edit(self) -> QLineEdit:
        return path(self.__view).group().child(TitledLineEditLayout).child(QLineEdit).get()
