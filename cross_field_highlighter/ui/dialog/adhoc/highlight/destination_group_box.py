import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QGroupBox

from .....config.settings import Settings
from .....highlighter.types import FieldNames
from .....ui.dialog.adhoc.fields_layout import FieldsLayout
from .....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModelListener, \
    AdhocHighlightDialogModel

log: Logger = logging.getLogger(__name__)


class DestinationGroupBox(QGroupBox, AdhocHighlightDialogModelListener):

    def __init__(self, model: AdhocHighlightDialogModel, settings: Settings):
        super().__init__(title="Destination", parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.__model.add_listener(self)
        self.__destination_fields_vbox: FieldsLayout = FieldsLayout(settings)
        self.__destination_fields_vbox.set_on_field_selected_callback(self.__on_field_selected_callback)
        layout: QVBoxLayout = QVBoxLayout()
        layout.addLayout(self.__destination_fields_vbox)
        self.setLayout(layout)
        self.setMinimumWidth(150)
        self.adjustSize()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def highlight_model_changed(self, source: object, _: AdhocHighlightDialogModel) -> None:
        if source != self:
            log.debug("Model changed")
            self.__destination_fields_vbox.set_items(self.__model.get_current_state().get_selected_note_type().fields)
            disabled_fields: FieldNames = FieldNames([self.__model.get_current_state().get_selected_source_field()]) \
                if self.__model.get_current_state().get_selected_source_field() is not None else []
            self.__destination_fields_vbox.set_disabled_fields(disabled_fields)
            if self.__model.get_current_state().get_selected_destination_fields():
                self.__destination_fields_vbox.set_selected_fields(
                    self.__model.get_current_state().get_selected_destination_fields())

    def __on_field_selected_callback(self, selected_field_names: FieldNames):
        log.debug(f"On field selected: {selected_field_names}")
        if self.__model.get_current_state().get_selected_destination_fields() != selected_field_names:
            self.__model.get_current_state().select_destination_fields(selected_field_names)
            self.__model.fire_model_changed(self)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
