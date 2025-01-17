import logging
from logging import Logger

from aqt import gui_hooks

from .editor_button_creator import EditorButtonCreator
from .editor_did_init_buttons_hook import EditorDidInitButtonsHook

log: Logger = logging.getLogger(__name__)


class EditorButtonHooks:
    def __init__(self, editor_button_creator: EditorButtonCreator) -> None:
        self.__editor_did_init_buttons_hook: EditorDidInitButtonsHook = EditorDidInitButtonsHook(editor_button_creator)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        hook = gui_hooks.editor_did_init_buttons
        count_before: int = hook.count()
        self.remove_hooks()
        hook.append(self.__editor_did_init_buttons_hook)
        count_after: int = hook.count()
        log.info(f"Hooks were set: count_before={count_before}, count_after={count_after}")

    def remove_hooks(self) -> None:
        hook = gui_hooks.editor_did_init_buttons
        count_before: int = hook.count()
        hook.remove(self.__editor_did_init_buttons_hook)
        count_after: int = hook.count()
        log.info(f"Hooks were removed: count_before={count_before}, count_after={count_after}")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
