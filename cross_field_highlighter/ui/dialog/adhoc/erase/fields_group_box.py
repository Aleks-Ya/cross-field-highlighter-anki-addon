import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QGroupBox

from cross_field_highlighter.highlighter.types import FieldNames, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModelListener, \
    AdhocEraseDialogModel
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.widgets.titled_combo_box_layout import TitledComboBoxLayout

log: Logger = logging.getLogger(__name__)


class FieldsGroupBox(QGroupBox, AdhocEraseDialogModelListener):

    def __init__(self, model: AdhocEraseDialogModel):
        super().__init__(title=None, parent=None)
        self.__model: AdhocEraseDialogModel = model
        self.__model.add_listener(self)
        self.__note_type_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Note Type")
        self.__note_type_combo_box.add_current_index_changed_callback(self.__on_note_type_changed)
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
            note_type_names: list[NoteTypeName] = [note_type.name for note_type in self.__model.note_types]
            self.__note_type_combo_box.set_items(note_type_names)
            if self.__model.selected_note_type:
                self.__note_type_combo_box.set_current_text(self.__model.selected_note_type.name)
            if self.__model.selected_fields:
                self.__fields_vbox.set_selected_fields(self.__model.selected_fields)

    def __on_note_type_changed(self, index: int):
        log.debug(f"On combobox changed: {index}")
        field_names: FieldNames = FieldNames(self.__model.note_types[index].fields)
        self.__fields_vbox.set_items(field_names)

    def __on_field_selected_callback(self, selected_field_names: FieldNames):
        log.debug(f"On field selected: {selected_field_names}")
        self.__model.selected_fields = selected_field_names

    def get_selected_note_type_name(self) -> NoteTypeName:
        return NoteTypeName(self.__note_type_combo_box.get_current_text())

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
