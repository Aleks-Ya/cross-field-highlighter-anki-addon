import logging
from logging import Logger
from typing import Callable

from aqt.qt import QDialog, QGridLayout, QVBoxLayout, QDialogButtonBox, QGroupBox, QWidget, QPushButton

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import NoteTypeDetails, FieldName, Word
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout, TitledLineEditLayout

log: Logger = logging.getLogger(__name__)


class AdhocDialog(QDialog):

    def __init__(self):
        super().__init__(parent=None)
        self.__callback: Callable[[FieldName, FieldName, set[str]], None]
        self.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('Highlight')

        source_group_box: QGroupBox = self.__create_source_widget()
        formate_group_box: QGroupBox = self.__create_format_widget()

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                                        QDialogButtonBox.StandardButton.Cancel |
                                                        QDialogButtonBox.StandardButton.RestoreDefaults)
        destination_group_box: QGroupBox = self.__create_destination_widget()
        # noinspection PyUnresolvedReferences
        button_box.accepted.connect(self.__accept)
        # noinspection PyUnresolvedReferences
        button_box.rejected.connect(self.__reject)
        restore_defaults_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        # noinspection PyUnresolvedReferences
        restore_defaults_button.setToolTip(
            'Reset settings in this dialog to defaults. You will need to click the "OK" button to apply it.')
        # noinspection PyUnresolvedReferences
        restore_defaults_button.clicked.connect(self.__restore_defaults)

        layout: QGridLayout = QGridLayout(None)
        layout.addWidget(source_group_box, 0, 0)
        layout.addWidget(formate_group_box, 1, 0)
        layout.addWidget(destination_group_box, 2, 0)
        layout.addWidget(button_box, 3, 0)

        self.setLayout(layout)
        self.resize(300, 200)

    def show_dialog(self, params: DialogParams,
                    callback: Callable[[QWidget, FieldName, FieldName, set[str], HighlightFormat], None]) -> None:
        log.debug(f"Show dialog: {params}")
        self.__callback = callback
        self.__note_types: list[NoteTypeDetails] = params.note_types
        note_type_names: list[str] = [note_type.name for note_type in params.note_types]
        self.__note_type_combo_box.set_items(note_type_names)
        # noinspection PyUnresolvedReferences
        self.show()
        self.adjustSize()

    def __on_combobox_changed(self, index: int):
        log.debug(f"On combobox changed: {index}")
        field_names: list[str] = self.__note_types[index].fields
        self.__source_field_combo_box.set_items(field_names)
        self.__destination_field_combo_box.set_items(field_names)

    def __create_source_widget(self):
        self.__note_type_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Note Type")
        self.__note_type_combo_box.add_current_index_changed_callback(self.__on_combobox_changed)
        self.__source_field_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Field")
        self.__stop_words_layout: TitledLineEditLayout = TitledLineEditLayout(
            "Stop words:", text="a an to", clear_button_enabled=True)
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__note_type_combo_box)
        group_layout.addLayout(self.__source_field_combo_box)
        group_layout.addLayout(self.__stop_words_layout)
        group_box: QGroupBox = QGroupBox("Source")
        group_box.setLayout(group_layout)
        return group_box

    def __create_format_widget(self):
        self.__format_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Format")
        self.__format_combo_box.set_items([HighlightFormat.BOLD.name, HighlightFormat.ITALIC.name])
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__format_combo_box)
        group_box: QGroupBox = QGroupBox("Format")
        group_box.setLayout(group_layout)
        return group_box

    def __create_destination_widget(self):
        self.__destination_field_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Field")
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__destination_field_combo_box)
        group_box: QGroupBox = QGroupBox("Destination")
        group_box.setLayout(group_layout)
        return group_box

    def __accept(self) -> None:
        log.info("Starting")
        source_filed: FieldName = FieldName(self.__source_field_combo_box.get_current_text())
        destination_filed: FieldName = FieldName(self.__destination_field_combo_box.get_current_text())
        stop_words: set[Word] = {Word(word) for word in self.__stop_words_layout.get_text().split(" ")}
        highlight_format: HighlightFormat = HighlightFormat(self.__format_combo_box.get_current_text())
        self.__callback(self.parent(), source_filed, destination_filed, stop_words, highlight_format)

    def __reject(self) -> None:
        log.info("Cancelled")
        self.reject()

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")
