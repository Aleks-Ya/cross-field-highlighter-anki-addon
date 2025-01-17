import logging
from logging import Logger
from typing import Callable

from aqt.editor import Editor

from .editor_button_creator import EditorButtonCreator

log: Logger = logging.getLogger(__name__)


class EditorDidInitButtonsHook(Callable[[list[str], Editor], None]):
    def __init__(self, editor_button_creator: EditorButtonCreator) -> None:
        self.__editor_button_creator: EditorButtonCreator = editor_button_creator
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __call__(self, buttons: list[str], editor: Editor) -> None:
        log.debug("On Editor did init buttons...")
        highlight_button: str = self.__editor_button_creator.create_highlight_button(editor)
        buttons.append(highlight_button)
        erase_button: str = self.__editor_button_creator.create_erase_button(editor)
        buttons.append(erase_button)
        log.info("Buttons were added to Editor")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
