from PyQtPath.path_chain_pyqt6 import path
from aqt import QComboBox, QDialogButtonBox, QPushButton, Qt, QCheckBox

from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.adhoc.highlight.format_group_box import FormatGroupBox
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout
from tests.visual_qtbot import VisualQtBot


class AdhocHighlightDialogViewScaffold:
    def __init__(self, view: AdhocHighlightDialogView, visual_qtbot: VisualQtBot):
        self.__view = view
        self.__visual_qtbot = visual_qtbot

    def select_1st_note_type(self) -> None:
        note_type_combo_box: QComboBox = self.__get_note_type_combo_box()
        self.__visual_qtbot.mouseClick(note_type_combo_box, Qt.MouseButton.LeftButton)
        self.__visual_qtbot.keyClick(note_type_combo_box, Qt.Key.Key_Up)
        self.__visual_qtbot.keyClick(note_type_combo_box.view(), Qt.Key.Key_Enter)

    def select_2nd_note_type(self) -> None:
        note_type_combo_box: QComboBox = self.__get_note_type_combo_box()
        self.__visual_qtbot.mouseClick(note_type_combo_box, Qt.MouseButton.LeftButton)
        self.__visual_qtbot.keyClick(note_type_combo_box, Qt.Key.Key_Down)
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

    def mark_destination_field(self) -> None:
        check_box: QCheckBox = path(self.__view).child(FieldsLayout).checkbox().get()
        self.__visual_qtbot.mouseClick(check_box, Qt.MouseButton.LeftButton)
        self.__visual_qtbot.keyClick(check_box,
                                     Qt.Key.Key_Space)  # Mouse click just focus on check_box, but doesn't select it

    def get_format_combo_box(self) -> QComboBox:
        return path(self.__view).child(FormatGroupBox).child(TitledComboBoxLayout).combobox().get()

    def click_start_button(self) -> None:
        self.__click_button(self.__get_start_button())

    def click_cancel_button(self) -> None:
        self.__click_button(self.__get_cancel_button())

    def click_restore_defaults_button(self) -> None:
        self.__click_button(self.__get_restore_defaults_button())

    def __get_note_type_combo_box(self) -> QComboBox:
        return path(self.__view).group(0).child(TitledComboBoxLayout, 0).combobox().get()

    def __get_source_field_combo_box(self) -> QComboBox:
        return path(self.__view).group(0).child(TitledComboBoxLayout, 1).combobox().get()

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