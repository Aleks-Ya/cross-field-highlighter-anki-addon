import pytest
from PyQt6.QtGui import QDesktopServices
from aqt import gui_hooks, DialogManager
from aqt.addons import AddonManager

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.settings import Settings
from cross_field_highlighter.config.url_manager import UrlManager
from cross_field_highlighter.ui.browser_hooks import BrowserHooks
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from cross_field_highlighter.ui.operation.op_factory import OpFactory


@pytest.fixture
def browser_hooks(op_factory: OpFactory,
                  adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                  adhoc_erase_dialog_controller: AdhocEraseDialogController, dialog_params_factory: DialogParamsFactory,
                  addon_manager: AddonManager, dialog_manager: DialogManager, url_manager: UrlManager,
                  desktop_services: QDesktopServices, config: Config, settings: Settings) -> BrowserHooks:
    browser_hooks: BrowserHooks = BrowserHooks(op_factory, adhoc_highlight_dialog_controller,
                                               adhoc_erase_dialog_controller, dialog_params_factory, addon_manager,
                                               dialog_manager, url_manager, desktop_services, config, settings)
    yield browser_hooks
    browser_hooks.remove_hooks()


def test_setup_hooks_enabled(browser_hooks: BrowserHooks):
    __assert_no_hooks()
    browser_hooks.setup_hooks()
    assert gui_hooks.browser_will_show.count() == 1
    assert gui_hooks.browser_will_show_context_menu.count() == 1
    browser_hooks.setup_hooks()
    assert gui_hooks.browser_will_show.count() == 1
    assert gui_hooks.browser_will_show_context_menu.count() == 1
    browser_hooks.remove_hooks()
    __assert_no_hooks()


def __assert_no_hooks():
    assert gui_hooks.browser_will_show.count() == 0
    assert gui_hooks.browser_will_show_context_menu.count() == 0
