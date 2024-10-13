import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout, QVBoxLayout, QDialogButtonBox, QGroupBox, QPushButton

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldName, Word, NoteTypeDetails, FieldNames
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import \
    AdhocHighlightDialogModelListener, AdhocHighlightDialogModel
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout, TitledLineEditLayout

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogView(QDialog, AdhocHighlightDialogModelListener):

    def __init__(self, model: AdhocHighlightDialogModel):
        super().__init__(parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.__model.add_listener(self)
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
        log.debug(f"{self.__class__.__name__} was instantiated")

    def model_changed(self, source: object) -> None:
        if source != self:
            log.debug(f"Model changed")
            note_type_names: list[str] = [note_type.name for note_type in self.__model.note_types]
            self.__note_type_combo_box.set_items(note_type_names)

            format_names: list[str] = [highlight_format.name for highlight_format in self.__model.formats]
            self.__format_combo_box.set_items(format_names)

            if self.__model.selected_note_type:
                self.__note_type_combo_box.set_current_text(self.__model.selected_note_type.name)
            if self.__model.selected_source_field:
                self.__source_field_combo_box.set_current_text(self.__model.selected_source_field)
            if self.__model.selected_format:
                self.__format_combo_box.set_current_text(self.__model.selected_format.name)
            if self.__model.selected_destination_fields:
                self.__destination_fields_vbox.select_fields(self.__model.selected_destination_fields)

            # noinspection PyUnresolvedReferences
            self.show()
            self.adjustSize()

    def __on_combobox_changed(self, index: int):
        log.debug(f"On combobox changed: {index}")
        field_names: FieldNames = self.__model.note_types[index].fields
        self.__source_field_combo_box.set_items(field_names)
        self.__destination_fields_vbox.set_items(field_names)

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
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__format_combo_box)
        group_box: QGroupBox = QGroupBox("Format")
        group_box.setLayout(group_layout)
        return group_box

    def __create_destination_widget(self):
        self.__destination_fields_vbox: FieldsLayout = FieldsLayout()
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__destination_fields_vbox)
        group_box: QGroupBox = QGroupBox("Destination")
        group_box.setLayout(group_layout)
        return group_box

    def __accept(self) -> None:
        log.info("Starting")
        source_filed: FieldName = FieldName(self.__source_field_combo_box.get_current_text())
        destination_fields: FieldNames = self.__destination_fields_vbox.get_selected_field_names()
        stop_words: set[Word] = {Word(word) for word in self.__stop_words_layout.get_text().split(" ")}
        highlight_format: HighlightFormat = HighlightFormat(self.__format_combo_box.get_current_text())

        note_type_names: dict[str, NoteTypeDetails] = {note_type.name: note_type for note_type in
                                                       self.__model.note_types}
        note_type: NoteTypeDetails = note_type_names[self.__note_type_combo_box.get_current_text()]
        self.__model.selected_note_type = note_type
        self.__model.selected_source_field = source_filed
        self.__model.selected_format = highlight_format
        self.__model.selected_destination_fields = destination_fields
        self.__model.fire_model_changed(self)

        self.hide()
        self.__model.run_op_callback(self.parent(), source_filed, destination_fields, stop_words, highlight_format)

    def __reject(self) -> None:
        log.info("Cancelled")
        self.hide()

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")

    def __repr__(self):
        return self.__class__.__name__
