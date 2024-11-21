import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout, QVBoxLayout, QDialogButtonBox, QGroupBox, QPushButton, Qt

from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldName, FieldNames, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import \
    AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.destination_group_box import DestinationGroupBox
from cross_field_highlighter.ui.dialog.adhoc.highlight.format_group_box import FormatGroupBox
from cross_field_highlighter.ui.widgets.titled_combo_box_layout import TitledComboBoxLayout
from cross_field_highlighter.ui.widgets.titled_line_edit_layout import TitledLineEditLayout

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogView(QDialog):

    def __init__(self, model: AdhocHighlightDialogModel, note_type_details_factory: NoteTypeDetailsFactory):
        super().__init__(parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('Highlight')

        source_group_box: QGroupBox = self.__create_source_widget()
        self.__format_group_box: FormatGroupBox = FormatGroupBox(model)

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                                        QDialogButtonBox.StandardButton.Cancel |
                                                        QDialogButtonBox.StandardButton.RestoreDefaults)
        start_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
        start_button.setText("Start")
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

    def __fill_ui_from_model(self):
        note_type_names: list[str] = [note_type.name for note_type in self.__model.note_types]
        self.__note_type_combo_box.set_items(note_type_names)
        if self.__model.selected_note_type:
            self.__note_type_combo_box.set_current_text(self.__model.selected_note_type.name)
        self.__update_source_field_from_model()
        if self.__model.selected_stop_words:
            self.__stop_words_layout.set_text(self.__model.selected_stop_words)
        else:
            if self.__model.default_stop_words:
                self.__stop_words_layout.set_text(self.__model.default_stop_words)
        self.__model.fire_model_changed(self)

    def __update_source_field_from_model(self):
        if self.__model.selected_note_type:
            if self.__model.selected_source_field:
                if self.__model.selected_note_type.name in self.__model.selected_source_field:
                    selected_source_field: FieldName = self.__model.selected_source_field[
                        self.__model.selected_note_type.name]
                    self.__source_field_combo_box.set_current_text(selected_source_field)

    def __on_note_type_changed(self, index: int):
        log.debug(f"On note type selected: {index}")
        self.__model.selected_note_type = self.__model.note_types[index]
        self.__model.destination_fields = self.__model.selected_note_type.fields
        self.__source_field_combo_box.set_items(self.__model.destination_fields)
        if self.__model.selected_note_type.name in self.__model.selected_source_field:
            previous_selected_source_field: FieldName = self.__model.selected_source_field[
                self.__model.selected_note_type.name]
            if previous_selected_source_field in self.__model.selected_note_type.fields:
                self.__model.selected_source_field[
                    self.__model.selected_note_type.name] = previous_selected_source_field
        self.__model.fire_model_changed(self)

    def __on_source_field_changed(self, item: str):
        log.debug(f"On source field selected: {item}")
        field_name: FieldName = FieldName(item)
        if self.__model.selected_note_type:
            self.__model.selected_source_field[self.__model.selected_note_type.name] = field_name
        self.__model.fire_model_changed(self)

    def __create_source_widget(self):
        self.__note_type_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Note Type")
        self.__note_type_combo_box.add_current_index_changed_callback(self.__on_note_type_changed)
        self.__source_field_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Field")
        self.__source_field_combo_box.add_current_text_changed_callback(self.__on_source_field_changed)
        self.__stop_words_layout: TitledLineEditLayout = TitledLineEditLayout(
            "Exclude words:", text="a an to", clear_button_enabled=True)
        self.__stop_words_layout.set_on_text_changed_callback(self.__on_stop_words_text_changed)
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__note_type_combo_box)
        group_layout.addLayout(self.__source_field_combo_box)
        group_layout.addLayout(self.__stop_words_layout)
        group_box: QGroupBox = QGroupBox("Source")
        group_box.setLayout(group_layout)
        return group_box

    def __accept(self) -> None:
        log.info("Starting")
        self.hide()
        if self.__model.accept_callback:
            self.__model.accept_callback()

    def __get_current_note_type_details(self):
        note_type_name: NoteTypeName = NoteTypeName(self.__note_type_combo_box.get_current_text())
        return self.__note_type_details_factory.by_note_type_name(note_type_name)

    def __reject(self) -> None:
        log.info("Cancelled")
        self.hide()
        if self.__model.reject_callback:
            self.__model.reject_callback()

    def __on_stop_words_text_changed(self, text: str):
        self.__model.selected_stop_words = text

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")
        self.__model.destination_fields = FieldNames([])
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
