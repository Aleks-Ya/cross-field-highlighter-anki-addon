import logging
from logging import Logger

from aqt import gui_hooks, DialogManager, QDesktopServices
from aqt.addons import AddonManager

from .browser_will_show_context_menu_hook import BrowserWillShowContextMenuHook
from .browser_will_show_hook import BrowserWillShowHook
from ...config.config import Config
from ...config.settings import Settings
from ...config.url_manager import UrlManager
from ...ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from ...ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
from ...ui.menu.dialog_params_factory import DialogParamsFactory
from ...ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserHooks:

    def __init__(self, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController, dialog_params_factory: DialogParamsFactory,
                 addon_manager: AddonManager, dialog_manager: DialogManager, url_manager: UrlManager,
                 desktop_services: QDesktopServices, config: Config, settings: Settings) -> None:
        self.__hook_browser_will_show: BrowserWillShowHook = BrowserWillShowHook(
            op_factory, adhoc_highlight_dialog_controller, adhoc_erase_dialog_controller, dialog_params_factory, config)
        self.__hook_browser_will_show_context_menu: BrowserWillShowContextMenuHook = BrowserWillShowContextMenuHook(
            op_factory, adhoc_highlight_dialog_controller, adhoc_erase_dialog_controller, dialog_params_factory,
            addon_manager, dialog_manager, url_manager, desktop_services, config, settings)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def setup_hooks(self) -> None:
        self.remove_hooks()
        gui_hooks.browser_will_show.append(self.__hook_browser_will_show)
        gui_hooks.browser_will_show_context_menu.append(self.__hook_browser_will_show_context_menu)
        log.info(f"{self.__class__.__name__} are set")

    def remove_hooks(self) -> None:
        gui_hooks.browser_will_show.remove(self.__hook_browser_will_show)
        gui_hooks.browser_will_show_context_menu.remove(self.__hook_browser_will_show_context_menu)
        log.info(f"{self.__class__.__name__} are removed")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
