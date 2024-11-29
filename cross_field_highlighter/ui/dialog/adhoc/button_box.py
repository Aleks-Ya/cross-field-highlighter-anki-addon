import logging
from logging import Logger
from typing import Callable

from aqt.qt import QDialogButtonBox, QPushButton

log: Logger = logging.getLogger(__name__)


class ButtonBox(QDialogButtonBox):

    def __init__(self, start_callback: Callable[[], None], cancel_callback: Callable[[], None],
                 restore_defaults_callback: Callable[[], None]):
        super().__init__(QDialogButtonBox.StandardButton.Ok |
                         QDialogButtonBox.StandardButton.Cancel |
                         QDialogButtonBox.StandardButton.RestoreDefaults)
        start_button: QPushButton = self.button(QDialogButtonBox.StandardButton.Ok)
        start_button.setText("Start")
        self.accepted.connect(start_callback)
        self.rejected.connect(cancel_callback)
        restore_defaults_button: QPushButton = self.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        restore_defaults_button.setToolTip('Reset settings in this dialog to defaults')
        restore_defaults_button.clicked.connect(restore_defaults_callback)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
