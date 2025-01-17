import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks
from aqt.editor import Editor

from .editor_button_creator import EditorButtonCreator

log: Logger = logging.getLogger(__name__)


class EditorButtonHooks:
    def __init__(self, editor_button_creator: EditorButtonCreator) -> None:
        self.__editor_button_creator: EditorButtonCreator = editor_button_creator
        self.__hook_editor_did_init_buttons: Callable[[list[str], Editor], None] = self.__on_editor_did_init_buttons
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        hook = gui_hooks.editor_did_init_buttons
        count_before: int = hook.count()
        self.remove_hooks()
        hook.append(self.__hook_editor_did_init_buttons)
        count_after: int = hook.count()
        log.info(f"Hooks were set: count_before={count_before}, count_after={count_after}")

    def remove_hooks(self) -> None:
        hook = gui_hooks.editor_did_init_buttons
        count_before: int = hook.count()
        hook.remove(self.__hook_editor_did_init_buttons)
        count_after: int = hook.count()
        log.info(f"Hooks were removed: count_before={count_before}, count_after={count_after}")

    def __on_editor_did_init_buttons(self, buttons: list[str], editor: Editor) -> None:
        log.debug("On Editor did init buttons...")
        highlight_button: str = self.__editor_button_creator.create_highlight_button(editor)
        buttons.append(highlight_button)
        erase_button: str = self.__editor_button_creator.create_erase_button(editor)
        buttons.append(erase_button)
        log.info("Buttons were added to Editor")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
