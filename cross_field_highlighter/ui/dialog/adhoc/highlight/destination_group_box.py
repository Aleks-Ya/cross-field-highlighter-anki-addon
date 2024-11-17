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
        layout: QVBoxLayout = QVBoxLayout()
        layout.addLayout(self.__destination_fields_vbox)
        self.setLayout(layout)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def model_changed(self, source: object) -> None:
        if source != self:
            log.debug(f"Model changed")
            self.__destination_fields_vbox.set_items(self.__model.destination_fields)
            self.__destination_fields_vbox.set_disabled_fields(self.__model.disabled_destination_fields)
            if self.__model.selected_destination_fields:
                self.__destination_fields_vbox.set_selected_fields(self.__model.selected_destination_fields)

    def update_model_from_ui(self):
        destination_fields: FieldNames = self.__destination_fields_vbox.get_selected_field_names()
        self.__model.selected_destination_fields = destination_fields

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
