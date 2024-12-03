from PyQt6.QtWidgets import QLineEdit
from PyQtPath.path_chain_pyqt6 import path
from aqt import QComboBox, QDialogButtonBox, QPushButton, Qt, QCheckBox

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
        self.__visual_qtbot.mouseClick(note_type_combo_box, Qt.MouseButton.LeftButton)
        for key in keys:
            self.__visual_qtbot.keyClick(note_type_combo_box, key)
        self.__visual_qtbot.keyClick(note_type_combo_box.view(), Qt.Key.Key_Enter)

    def select_2nd_source_field_combo_box(self) -> None:
        source_field_combo_box: QComboBox = self.__get_source_field_combo_box()
        self.__visual_qtbot.mouseClick(source_field_combo_box, Qt.MouseButton.LeftButton)
        self.__visual_qtbot.keyClick(source_field_combo_box, Qt.Key.Key_Down)
        self.__visual_qtbot.keyClick(source_field_combo_box.view(), Qt.Key.Key_Enter)

    def select_2nd_format_combo_box(self) -> None:
        format_combo_box: QComboBox = self.get_format_combo_box()
        self.__visual_qtbot.mouseClick(format_combo_box, Qt.MouseButton.LeftButton)
        self.__visual_qtbot.keyClick(format_combo_box, Qt.Key.Key_Down)
        self.__visual_qtbot.keyClick(format_combo_box.view(), Qt.Key.Key_Enter)

    def mark_destination_field(self, field_name: FieldName) -> None:
        checkboxes: list[QCheckBox] = path(self.__view).child(FieldsLayout).children(QCheckBox)
        for check_box in checkboxes:
            if check_box.text() == field_name:
                self.__visual_qtbot.mouseClick(check_box, Qt.MouseButton.LeftButton)
                # Mouse click just focus on check_box, but doesn't select it
                self.__visual_qtbot.keyClick(check_box, Qt.Key.Key_Space)
                return
        raise AssertionError(f"Field '{field_name}' not found")

    def print_to_stop_words(self, stop_words: str) -> None:
        stop_words_line_edit: QLineEdit = self.__get_stop_words_line_edit()
        self.__visual_qtbot.keyClicks(stop_words_line_edit, stop_words)

    def get_format_combo_box(self) -> QComboBox:
        return path(self.__view).child(FormatGroupBox).child(TitledComboBoxLayout).combobox().get()

    def click_space_delimited_language(self) -> None:
        checkbox: QCheckBox = self.__get_space_delimited_language_checkbox()
        self.__visual_qtbot.mouseClick(checkbox, Qt.MouseButton.LeftButton)

    def click_start_button(self) -> None:
        self.__click_button(self.__get_start_button())

    def click_cancel_button(self) -> None:
        self.__click_button(self.__get_cancel_button())

    def click_restore_defaults_button(self) -> None:
        self.__click_button(self.__get_restore_defaults_button())

    def __get_note_type_combo_box(self) -> QComboBox:
        return path(self.__view).group().child(NoteTypeComboBoxLayout).combobox().get()

    def __get_source_field_combo_box(self) -> QComboBox:
        return path(self.__view).group().child(TitledComboBoxLayout).combobox().get()

    def __get_space_delimited_language_checkbox(self) -> QCheckBox:
        return path(self.__view).group().checkbox().get()

    def __click_button(self, button: QPushButton) -> None:
        self.__visual_qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

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
