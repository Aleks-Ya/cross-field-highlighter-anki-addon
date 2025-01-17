import logging
from logging import Logger
from typing import Callable

from aqt import gui_hooks, QMenu, DialogManager, QDesktopServices
from aqt.addons import AddonManager
from aqt.browser import Browser

from .browser_will_show_hook import BrowserWillShowHook
from ...config.config import Config
from ...config.settings import Settings
from ...config.url_manager import UrlManager
from ...ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from ...ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
from ...ui.menu.browser_menu import BrowserMenu
from ...ui.menu.browser_menu_erase_action import BrowserMenuEraseAction
from ...ui.menu.browser_menu_highlight_action import BrowserMenuHighlightAction
from ...ui.menu.dialog_params_factory import DialogParamsFactory
from ...ui.operation.op_factory import OpFactory

log: Logger = logging.getLogger(__name__)


class BrowserHooks:

    def __init__(self, op_factory: OpFactory,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController, dialog_params_factory: DialogParamsFactory,
                 addon_manager: AddonManager, dialog_manager: DialogManager, url_manager: UrlManager,
                 desktop_services: QDesktopServices, config: Config, settings: Settings) -> None:
        self.__op_factory: OpFactory = op_factory
        self.__adhoc_highlight_dialog_controller: AdhocHighlightDialogController = adhoc_highlight_dialog_controller
        self.__adhoc_erase_dialog_controller: AdhocEraseDialogController = adhoc_erase_dialog_controller
        self.__dialog_params_factory: DialogParamsFactory = dialog_params_factory
        self.__addon_manager: AddonManager = addon_manager
        self.__dialog_manager: DialogManager = dialog_manager
        self.__url_manager: UrlManager = url_manager
        self.__desktop_services: QDesktopServices = desktop_services
        self.__config: Config = config
        self.__settings: Settings = settings
        self.__hook_browser_will_show: BrowserWillShowHook = BrowserWillShowHook(
            op_factory, adhoc_highlight_dialog_controller, adhoc_erase_dialog_controller, dialog_params_factory, config)
        self.__hook_browser_will_show_context_menu: Callable[
            [Browser, QMenu], None] = self.__on_browser_will_show_context_menu
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

    def __on_browser_will_show_context_menu(self, browser: Browser, menu: QMenu) -> None:
        log.debug("On Browser will show context menu")
        highlight_action: BrowserMenuHighlightAction = BrowserMenuHighlightAction(
            browser, self.__op_factory, self.__adhoc_highlight_dialog_controller, self.__dialog_params_factory,
            self.__config)
        erase_action: BrowserMenuEraseAction = BrowserMenuEraseAction(
            browser, self.__op_factory, self.__adhoc_erase_dialog_controller, self.__dialog_params_factory,
            self.__config)
        browser_menu: BrowserMenu = BrowserMenu(
            browser, highlight_action, erase_action, self.__addon_manager, self.__dialog_manager,
            self.__url_manager, self.__desktop_services, self.__config, self.__settings)
        menu.addMenu(browser_menu)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
