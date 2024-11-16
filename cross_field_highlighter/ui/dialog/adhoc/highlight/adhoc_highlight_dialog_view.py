import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout, QVBoxLayout, QDialogButtonBox, QGroupBox, QPushButton, Qt

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldName, FieldNames, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import \
    AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.destination_group_box import DestinationGroupBox
from cross_field_highlighter.ui.dialog.adhoc.highlight.format_group_box import FormatGroupBox
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout, TitledLineEditLayout

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogView(QDialog):

    def __init__(self, model: AdhocHighlightDialogModel):
        super().__init__(parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('Highlight')

        source_group_box: QGroupBox = self.__create_source_widget()
        self.__format_group_box: FormatGroupBox = FormatGroupBox(model)

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                                        QDialogButtonBox.StandardButton.Cancel |
                                                        QDialogButtonBox.StandardButton.RestoreDefaults)
        ok_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setText("Start")
        self.__destination_group_box: DestinationGroupBox = DestinationGroupBox(model)
        # noinspection PyUnresolvedReferences
        button_box.accepted.connect(self.__accept)
        # noinspection PyUnresolvedReferences
        button_box.rejected.connect(self.__reject)
        restore_defaults_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        # noinspection PyUnresolvedReferences
        restore_defaults_button.setToolTip('Reset settings in this dialog to defaults')
        # noinspection PyUnresolvedReferences
        restore_defaults_button.clicked.connect(self.__restore_defaults)

        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(source_group_box, 0, 0, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.__format_group_box, 0, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.__destination_group_box, 0, 2, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(button_box, 3, 0, Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.resize(300, 200)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_view(self) -> None:
        log.debug(f"Show view")
        self.__fill_ui_from_model()
        # noinspection PyUnresolvedReferences
        self.show()
        self.adjustSize()
        # self.__model.fire_model_changed(self)

    def __fill_ui_from_model(self):
        note_type_names: list[str] = [note_type.name for note_type in self.__model.note_types]
        self.__note_type_combo_box.set_items(note_type_names)
        if self.__model.selected_note_type:
            self.__note_type_combo_box.set_current_text(self.__model.selected_note_type.name)
        self.__update_source_field_from_model()
        if self.__model.selected_stop_words:
            self.__stop_words_layout.set_text(self.__model.selected_stop_words)
        if self.__model.selected_stop_words:
            self.__stop_words_layout.set_text(self.__model.selected_stop_words)

    def __update_source_field_from_model(self):
        if self.__model.selected_note_type:
            if self.__model.selected_source_field:
                if self.__model.selected_note_type.name in self.__model.selected_source_field:
                    selected_source_field: FieldName = self.__model.selected_source_field[
                        self.__model.selected_note_type.name]
                    self.__source_field_combo_box.set_current_text(selected_source_field)

    def __on_note_type_changed(self, index: int):
        log.debug(f"On note type selected: {index}")
        field_names: FieldNames = self.__model.note_types[index].fields
        self.__model.destination_fields = field_names
        self.__source_field_combo_box.set_items(field_names)
        self.__on_source_field_changed(self.__source_field_combo_box.get_current_text())
        self.__model.fire_model_changed(self)

    def __on_source_field_changed(self, item: str):
        log.debug(f"On source field selected: {item}")
        self.__model.disabled_destination_fields = FieldNames([FieldName(item)])
        self.__model.fire_model_changed(self)

    def __create_source_widget(self):
        self.__note_type_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Note Type")
        self.__note_type_combo_box.add_current_index_changed_callback(self.__on_note_type_changed)
        self.__source_field_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Field")
        self.__source_field_combo_box.add_current_text_changed_callback(self.__on_source_field_changed)
        self.__stop_words_layout: TitledLineEditLayout = TitledLineEditLayout(
            "Exclude words:", text="a an to", clear_button_enabled=True)
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__note_type_combo_box)
        group_layout.addLayout(self.__source_field_combo_box)
        group_layout.addLayout(self.__stop_words_layout)
        group_box: QGroupBox = QGroupBox("Source")
        group_box.setLayout(group_layout)
        return group_box

    def __accept(self) -> None:
        log.info("Starting")
        self.__update_model_from_ui()
        self.hide()
        if self.__model.accept_callback:
            self.__model.accept_callback()

    def __get_current_note_type_details(self):
        note_type_names: dict[NoteTypeName, NoteTypeDetails] = {note_type.name: note_type for note_type in
                                                                self.__model.note_types}
        note_type: NoteTypeDetails = note_type_names[NoteTypeName(self.__note_type_combo_box.get_current_text())]
        return note_type

    def __reject(self) -> None:
        log.info("Cancelled")
        self.__update_model_from_ui()
        self.hide()
        if self.__model.reject_callback:
            self.__model.reject_callback()

    def __update_model_from_ui(self):
        source_filed: FieldName = FieldName(self.__source_field_combo_box.get_current_text())
        self.__format_group_box.update_model_from_ui()
        note_type_details: NoteTypeDetails = self.__get_current_note_type_details()
        self.__model.selected_note_type = note_type_details
        self.__model.selected_source_field[note_type_details.name] = source_filed
        self.__model.selected_stop_words = self.__stop_words_layout.get_text()
        self.__destination_group_box.update_model_from_ui()
        self.__model.fire_model_changed(self)

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")
        self.__model.destination_fields = FieldNames([])
        self.__model.disabled_destination_fields = FieldNames([])
        self.__model.selected_note_type = None
        self.__model.selected_source_field = {}
        self.__model.selected_format = None
        self.__model.selected_stop_words = self.__model.default_stop_words
        self.__model.selected_destination_fields = FieldNames([])
        self.__fill_ui_from_model()
        self.__model.fire_model_changed(None)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
