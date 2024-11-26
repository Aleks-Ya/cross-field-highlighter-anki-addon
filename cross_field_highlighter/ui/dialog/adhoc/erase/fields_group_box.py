import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QGroupBox

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModelListener, \
    AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.widgets.note_type_combo_box_layout import NoteTypeComboBoxLayout

log: Logger = logging.getLogger(__name__)


class FieldsGroupBox(QGroupBox, AdhocEraseDialogModelListener):

    def __init__(self, model: AdhocEraseDialogModel):
        super().__init__(title=None, parent=None)
        self.__model: AdhocEraseDialogModel = model
        self.__model.add_listener(self)
        self.__note_type_combo_box: NoteTypeComboBoxLayout = NoteTypeComboBoxLayout()
        self.__note_type_combo_box.add_note_type_changed_callback(self.__on_note_type_changed)
        self.__fields_vbox: FieldsLayout = FieldsLayout()
        self.__fields_vbox.set_on_field_selected_callback(self.__on_field_selected_callback)
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__note_type_combo_box)
        group_layout.addLayout(self.__fields_vbox)
        self.setLayout(group_layout)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def model_changed(self, source: object) -> None:
        if source != self:
            log.debug(f"Model changed")
            self.__note_type_combo_box.set_note_types(self.__model.note_types)
            self.__note_type_combo_box.set_current_note_type(self.__model.get_current_state().get_selected_note_type())
            if self.__model.get_current_state().get_selected_fields():
                self.__fields_vbox.set_selected_fields(self.__model.get_current_state().get_selected_fields())

    def __on_note_type_changed(self, index: int):
        log.debug(f"On combobox changed: {index}")
        selected_note_type: NoteTypeDetails = self.__model.note_types[index]
        field_names: FieldNames = FieldNames(selected_note_type.fields)
        self.__fields_vbox.set_items(field_names)
        self.__model.switch_state(selected_note_type)
        self.__model.fire_model_changed(self)

    def __on_field_selected_callback(self, selected_field_names: FieldNames):
        log.debug(f"On field selected: {selected_field_names}")
        if self.__model.get_current_state().get_selected_fields() != selected_field_names:
            self.__model.get_current_state().select_fields(selected_field_names)
            self.__model.fire_model_changed(self)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
