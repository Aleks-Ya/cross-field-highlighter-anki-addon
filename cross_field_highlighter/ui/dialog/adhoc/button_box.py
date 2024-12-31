import logging
from logging import Logger
from typing import Callable

from aqt.qt import QDialogButtonBox, QPushButton

from ....ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModelListener, AdhocEraseDialogModel
from ....ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModelListener, \
    AdhocHighlightDialogModel

log: Logger = logging.getLogger(__name__)


class ButtonBox(QDialogButtonBox, AdhocHighlightDialogModelListener, AdhocEraseDialogModelListener):

    def __init__(self, start_callback: Callable[[], None], cancel_callback: Callable[[], None],
                 restore_defaults_callback: Callable[[], None]):
        super().__init__(QDialogButtonBox.StandardButton.Ok |
                         QDialogButtonBox.StandardButton.Cancel |
                         QDialogButtonBox.StandardButton.RestoreDefaults)
        self.__start_button: QPushButton = self.button(QDialogButtonBox.StandardButton.Ok)
        self.__start_button.setText("&Start")
        self.__start_button.setEnabled(False)
        cancel_button: QPushButton = self.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setText("&Cancel")
        # noinspection PyUnresolvedReferences
        self.accepted.connect(start_callback)
        # noinspection PyUnresolvedReferences
        self.rejected.connect(cancel_callback)
        restore_defaults_button: QPushButton = self.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        # noinspection PyUnresolvedReferences
        restore_defaults_button.setToolTip('Reset settings in this dialog to defaults')
        # noinspection PyUnresolvedReferences
        restore_defaults_button.clicked.connect(restore_defaults_callback)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def highlight_model_changed(self, source: object, model: AdhocHighlightDialogModel) -> None:
        if source != self:
            start_button_enabled: bool = len(model.get_current_state().get_selected_enabled_destination_fields()) > 0
            self.__enable_start_button(start_button_enabled)

    def erase_model_changed(self, source: object, model: AdhocEraseDialogModel) -> None:
        if source != self:
            start_button_enabled: bool = len(model.get_current_state().get_selected_fields()) > 0
            self.__enable_start_button(start_button_enabled)

    def __enable_start_button(self, enabled: bool) -> None:
        log.debug(f"Enable start button: {enabled}")
        if enabled:
            self.__start_button.setEnabled(True)
            # noinspection PyUnresolvedReferences
            self.__start_button.setToolTip('Start processing')
        else:
            self.__start_button.setEnabled(False)
            # noinspection PyUnresolvedReferences
            self.__start_button.setToolTip('Select at least one destination field')

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
