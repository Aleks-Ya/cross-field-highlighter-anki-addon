import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout, Qt

from .....config.settings import Settings
from .....ui.dialog.adhoc.button_box import ButtonBox
from .....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from .....ui.dialog.adhoc.highlight.destination_group_box import DestinationGroupBox
from .....ui.dialog.adhoc.highlight.format_group_box import FormatGroupBox
from .....ui.dialog.adhoc.highlight.source_group_box import SourceGroupBox

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogView(QDialog):

    def __init__(self, model: AdhocHighlightDialogModel, settings: Settings):
        super().__init__(parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.setVisible(False)

        source_group_box: SourceGroupBox = SourceGroupBox(model)
        format_group_box: FormatGroupBox = FormatGroupBox(model)
        destination_group_box: DestinationGroupBox = DestinationGroupBox(model, settings)
        button_box: ButtonBox = ButtonBox(self.__accept, self.__reject, self.__restore_defaults)
        self.__model.add_listener(button_box)

        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(source_group_box, 0, 0, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(format_group_box, 0, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(destination_group_box, 0, 2, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(button_box, 3, 0, 1, 3, Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.resize(300, 200)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_view(self) -> None:
        log.debug("Show view")
        # noinspection PyUnresolvedReferences
        self.setWindowTitle(self.__get_window_title())
        self.__model.get_current_state()  # select 1st if not chosen
        self.__model.fire_model_changed(self)
        # noinspection PyUnresolvedReferences
        self.show()
        self.adjustSize()

    def __get_window_title(self) -> str:
        noun: str = "note" if self.__model.get_note_number() == 1 else "notes"
        return f'Highlight {self.__model.get_note_number()} {noun}'

    def __accept(self) -> None:
        log.info("Starting")
        self.hide()
        self.__model.call_accept_callback()

    def __reject(self) -> None:
        log.info("Cancelled")
        self.hide()
        self.__model.call_reject_callback()

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")
        self.__model.reset_states()
        self.__model.fire_model_changed(None)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
