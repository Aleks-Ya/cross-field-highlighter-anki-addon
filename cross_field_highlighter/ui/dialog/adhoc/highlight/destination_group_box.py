import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QGroupBox

from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import \
    AdhocHighlightDialogModelListener, AdhocHighlightDialogModel

log: Logger = logging.getLogger(__name__)


class DestinationGroupBox(QGroupBox, AdhocHighlightDialogModelListener):

    def __init__(self, model: AdhocHighlightDialogModel):
        super().__init__(title="Destination", parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.__model.add_listener(self)
        self.__destination_fields_vbox: FieldsLayout = FieldsLayout()
        self.__destination_fields_vbox.set_on_field_selected_callback(self.__on_field_selected_callback)
        layout: QVBoxLayout = QVBoxLayout()
        layout.addLayout(self.__destination_fields_vbox)
        self.setLayout(layout)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def model_changed(self, source: object) -> None:
        if source != self:
            log.debug(f"Model changed")
            if self.__model.current_state:
                self.__destination_fields_vbox.set_items(self.__model.current_state.get_selected_note_type().fields)
            if self.__model.current_state:
                disabled_fields: FieldNames = FieldNames([self.__model.current_state.get_selected_source_filed()]) \
                    if self.__model.current_state.get_selected_source_filed() is not None else []
                self.__destination_fields_vbox.set_disabled_fields(disabled_fields)
                if self.__model.current_state.selected_destination_fields:
                    self.__destination_fields_vbox.set_selected_fields(
                        self.__model.current_state.selected_destination_fields)

    def __on_field_selected_callback(self, selected_field_names: FieldNames):
        log.debug(f"On field selected: {selected_field_names}")
        if self.__model.current_state.selected_destination_fields != selected_field_names:
            self.__model.current_state.selected_destination_fields = selected_field_names

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
