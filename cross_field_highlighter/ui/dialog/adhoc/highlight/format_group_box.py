import logging
from logging import Logger

from aqt.qt import QVBoxLayout, QGroupBox

from .....highlighter.formatter.highlight_format import HighlightFormat
from .....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModelListener, \
    AdhocHighlightDialogModel
from .....ui.widgets.titled_combo_box_layout import TitledComboBoxLayout

log: Logger = logging.getLogger(__name__)


class FormatGroupBox(QGroupBox, AdhocHighlightDialogModelListener):

    def __init__(self, model: AdhocHighlightDialogModel):
        super().__init__(title="Format", parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.__model.add_listener(self)
        self.__combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Format:")
        self.__combo_box.add_current_text_changed_callback(self.__on_current_text_changed)
        layout: QVBoxLayout = QVBoxLayout()
        layout.addLayout(self.__combo_box)
        self.setLayout(layout)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def highlight_model_changed(self, source: object, _: AdhocHighlightDialogModel) -> None:
        if source != self:
            log.debug("Model changed")
            highlight_formats: dict[str, HighlightFormat] = {highlight_format.name: highlight_format for
                                                             highlight_format in self.__model.get_formats()}
            self.__combo_box.set_data_items(highlight_formats)
            if self.__model.get_current_state().get_selected_format():
                self.__combo_box.set_current_text(self.__model.get_current_state().get_selected_format().name)

    def __on_current_text_changed(self, _: str) -> None:
        highlight_format: HighlightFormat = self.__combo_box.get_current_data()
        if self.__model.get_current_state().get_selected_format() != highlight_format:
            self.__model.get_current_state().select_format(highlight_format)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
