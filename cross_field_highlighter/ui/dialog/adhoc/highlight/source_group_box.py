import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QGroupBox

from .....highlighter.note_type_details import NoteTypeDetails
from .....highlighter.types import FieldName, Text
from .....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModelListener, \
    AdhocHighlightDialogModel
from .....ui.widgets.note_type_combo_box_layout import NoteTypeComboBoxLayout
from .....ui.widgets.titled_combo_box_layout import TitledComboBoxLayout
from .....ui.widgets.titled_line_edit_layout import TitledLineEditLayout

log: Logger = logging.getLogger(__name__)


class SourceGroupBox(QGroupBox, AdhocHighlightDialogModelListener):

    def __init__(self, model: AdhocHighlightDialogModel):
        super().__init__(title="Source", parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.__model.add_listener(self)
        self.__note_type_combo_box: NoteTypeComboBoxLayout = NoteTypeComboBoxLayout()
        self.__note_type_combo_box.set_note_type_changed_callback(self.__on_note_type_changed)
        self.__source_field_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Field:")
        self.__source_field_combo_box.add_current_text_changed_callback(self.__on_source_field_changed)
        self.__stop_words_layout: TitledLineEditLayout = TitledLineEditLayout(
            "Exclude words:", text="a an to", clear_button_enabled=True)
        self.__stop_words_layout.set_on_text_changed_callback(self.__on_stop_words_text_changed)
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__note_type_combo_box)
        group_layout.addLayout(self.__source_field_combo_box)
        group_layout.addLayout(self.__stop_words_layout)
        self.setLayout(group_layout)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def highlight_model_changed(self, source: object, _: AdhocHighlightDialogModel) -> None:
        if source != self:
            log.debug("Model changed")
            self.__note_type_combo_box.set_note_types(self.__model.get_note_types())
            self.__note_type_combo_box.set_current_note_type(self.__model.get_current_state().get_selected_note_type())
            self.__update_source_field_from_model()
            self.__stop_words_layout.set_text(self.__model.get_current_state().get_selected_stop_words())

    def __update_source_field_from_model(self):
        self.__source_field_combo_box.set_items(self.__model.get_current_state().get_selected_note_type().fields)
        selected_source_field: FieldName = self.__model.get_current_state().get_selected_source_field()
        self.__source_field_combo_box.set_current_text(selected_source_field)

    def __on_note_type_changed(self, selected_note_type: NoteTypeDetails):
        log.debug("On note type selected")
        self.__model.switch_state(selected_note_type)
        self.__update_source_field_from_model()
        self.__model.fire_model_changed(self)

    def __on_source_field_changed(self, item: str):
        log.debug(f"On source field selected: {item}")
        field_name: FieldName = FieldName(item)
        if self.__model.get_current_state().get_selected_source_field() != field_name:
            self.__model.get_current_state().select_source_field(field_name)
            self.__model.fire_model_changed(self)

    def __on_stop_words_text_changed(self, text: Text):
        if self.__model.get_current_state().get_selected_stop_words() != text:
            self.__model.get_current_state().set_stop_words(text)
            self.__model.fire_model_changed(self)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
