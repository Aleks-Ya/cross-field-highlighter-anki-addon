import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout

from ....number_formatter import NumberFormatter
from .....config.settings import Settings
from .....ui.dialog.adhoc.button_box import ButtonBox
from .....ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
from .....ui.dialog.adhoc.erase.fields_group_box import FieldsGroupBox

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogView(QDialog):

    def __init__(self, adhoc_erase_dialog_model: AdhocEraseDialogModel, settings: Settings):
        super().__init__(parent=None)
        self.__model: AdhocEraseDialogModel = adhoc_erase_dialog_model
        self.setVisible(False)
        # noinspection PyUnresolvedReferences

        fields_group_layout: FieldsGroupBox = FieldsGroupBox(adhoc_erase_dialog_model, settings)
        button_box: ButtonBox = ButtonBox(self.__accept, self.__reject, self.__restore_defaults)
        self.__model.add_listener(button_box)

        layout: QGridLayout = QGridLayout(None)
        layout.addWidget(fields_group_layout, 0, 0)
        layout.addWidget(button_box, 3, 0)

        self.setLayout(layout)
        self.resize(300, 200)
        # noinspection PyUnresolvedReferences
        self.rejected.connect(self.__reject)
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
        number: str = NumberFormatter.with_thousands_separator(self.__model.get_note_number())
        return f'Erase {number} {noun}'

    def __accept(self) -> None:
        log.info("Starting")
        self.hide()
        self.__model.call_accept_callback()
        log.debug(f"{self.__class__.__name__} was instantiated")

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
