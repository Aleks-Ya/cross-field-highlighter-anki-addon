import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout

from .....ui.dialog.adhoc.button_box import ButtonBox
from .....ui.dialog.adhoc.erase.fields_group_box import FieldsGroupBox
from .....ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogView(QDialog):

    def __init__(self, adhoc_erase_dialog_model: AdhocEraseDialogModel):
        super().__init__(parent=None)
        self.__model: AdhocEraseDialogModel = adhoc_erase_dialog_model
        self.setVisible(False)
        # noinspection PyUnresolvedReferences

        fields_group_layout: FieldsGroupBox = FieldsGroupBox(adhoc_erase_dialog_model)
        button_box: ButtonBox = ButtonBox(self.__accept, self.__reject, self.__restore_defaults)

        layout: QGridLayout = QGridLayout(None)
        layout.addWidget(fields_group_layout, 0, 0)
        layout.addWidget(button_box, 3, 0)

        self.setLayout(layout)
        self.resize(300, 200)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_view(self) -> None:
        log.debug("Show view")
        # noinspection PyUnresolvedReferences
        self.setWindowTitle(self.__get_window_title())
        # noinspection PyUnresolvedReferences
        self.show()
        self.adjustSize()
        self.__model.fire_model_changed(self)

    def __get_window_title(self) -> str:
        noun: str = "note" if self.__model.get_note_number() == 1 else "notes"
        return f'Erase {self.__model.get_note_number()} {noun}'

    def __accept(self) -> None:
        log.info("Starting")
        self.hide()
        self.__model.call_accept_callback()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __reject(self) -> None:
        log.info("Cancelled")
        self.reject()
        self.__model.call_reject_callback()

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")
        self.__model.reset_states()
        self.__model.fire_model_changed(None)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
