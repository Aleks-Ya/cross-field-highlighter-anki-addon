from pathlib import Path

from anki.collection import Collection
from aqt import mw, gui_hooks

from cross_field_highlighter.ui.browser_hooks import BrowserHooks
from cross_field_highlighter.log.logs import Logs


def __initialize(col: Collection):
    module_dir: Path = Path(__file__).parent
    module_name: str = module_dir.stem
    log_dir: Path = mw.addonManager.logs_folder(module_name)
    logs: Logs = Logs(log_dir)
    logs.set_level("DEBUG")
    browser_hooks: BrowserHooks = BrowserHooks()
    browser_hooks.setup_hooks()

gui_hooks.collection_did_load.append(__initialize)
