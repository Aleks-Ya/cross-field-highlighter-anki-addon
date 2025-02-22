import logging
from logging import Logger
from typing import Callable

from ..common.collection_holder import CollectionHolder


class ProfileDidOpenHook(Callable[[], None]):
    def __init__(self, collection_holder: CollectionHolder):
        self.__collection_holder: CollectionHolder = collection_holder
        self.__initialized: bool = False

    def __call__(self) -> None:
        from pathlib import Path
        from aqt.addons import AddonManager
        from aqt.progress import ProgressManager
        from aqt import ProfileManager
        from aqt.taskman import TaskManager
        from aqt import mw, DialogManager, dialogs
        from ..config.config import Config
        from ..config.config_loader import ConfigLoader
        from ..config.settings import Settings
        from ..config.user_folder_storage import UserFolderStorage
        from ..highlighter.formatter.formatter_facade import FormatterFacade
        from ..highlighter.note.regex_field_highlighter import RegexFieldHighlighter
        from ..highlighter.note_type_details_factory import NoteTypeDetailsFactory
        from ..highlighter.notes.notes_highlighter import NotesHighlighter
        from ..highlighter.tokenizer.regex_tokenizer import RegExTokenizer
        from ..log.logs import Logs
        from ..ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
        from ..ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
        from ..ui.menu.dialog_params_factory import DialogParamsFactory
        from ..ui.operation.op_statistics_formatter import OpStatisticsFormatter
        from ..ui.operation.op_factory import OpFactory

        if self.__initialized:
            log: Logger = logging.getLogger(__name__)
            log.info(f"Switched to profile: '{mw.pm.name}'")
            return
        self.__initialized = True

        module_dir: Path = Path(__file__).parent.parent
        module_name: str = module_dir.stem
        version: str = (module_dir / 'version.txt').read_text()
        addon_manager: AddonManager = mw.addonManager
        dialog_manager: DialogManager = dialogs
        log_dir: Path = addon_manager.logs_folder(module_name)
        logs: Logs = Logs(log_dir)
        logs.set_level("DEBUG")
        task_manager: TaskManager = mw.taskman
        progress_manager: ProgressManager = mw.progress
        profile_manager: ProfileManager = mw.pm
        log: Logger = logging.getLogger(__name__)
        log.info(f"Initialized profile: '{profile_manager.name}'")
        settings: Settings = Settings(module_dir, module_name, addon_manager.logs_folder(module_name), version)
        config_loader: ConfigLoader = ConfigLoader(addon_manager, settings)
        config: Config = Config(config_loader)

        tokenizer: RegExTokenizer = RegExTokenizer()
        formatter_facade: FormatterFacade = FormatterFacade()
        regex_field_highlighter: RegexFieldHighlighter = self.__regex_field_highlighter(formatter_facade, tokenizer)
        notes_highlighter: NotesHighlighter = NotesHighlighter(regex_field_highlighter, config)

        note_type_details_factory: NoteTypeDetailsFactory = NoteTypeDetailsFactory(self.__collection_holder)
        user_folder_storage: UserFolderStorage = UserFolderStorage(profile_manager, settings)
        highlight_dialog_controller: AdhocHighlightDialogController = self.__highlight_dialog_controller(
            config, formatter_facade, note_type_details_factory, settings, user_folder_storage)
        erase_dialog_controller: AdhocEraseDialogController = self.__erase_dialog_controller(
            note_type_details_factory, settings, user_folder_storage)
        op_statistics_formatter: OpStatisticsFormatter = OpStatisticsFormatter(self.__collection_holder)
        op_factory: OpFactory = OpFactory(self.__collection_holder, notes_highlighter, task_manager, progress_manager,
                                          op_statistics_formatter, config)
        dialog_params_factory: DialogParamsFactory = DialogParamsFactory(
            self.__collection_holder, note_type_details_factory)
        self.__set_browser_will_show_hook(config, dialog_params_factory, erase_dialog_controller,
                                          highlight_dialog_controller, op_factory)
        self.__set_browser_will_show_context_menu_hook(addon_manager, config, dialog_manager, dialog_params_factory,
                                                       erase_dialog_controller, highlight_dialog_controller, op_factory,
                                                       settings)
        self.__set_editor_did_init_buttons_hook(config, erase_dialog_controller, highlight_dialog_controller,
                                                note_type_details_factory, regex_field_highlighter, settings)

    @staticmethod
    def __regex_field_highlighter(formatter_facade, tokenizer):
        from ..highlighter.note.regex_field_highlighter import RegexFieldHighlighter
        from ..highlighter.text.regex_text_highlighter import RegexTextHighlighter
        from ..highlighter.text.text_highlighter import TextHighlighter
        from ..highlighter.token.find_and_replace_token_highlighter import FindAndReplaceTokenHighlighter
        from ..highlighter.token.start_with_token_highlighter import StartWithTokenHighlighter
        from ..highlighter.tokenizer.stop_words_tokenizer import StopWordsTokenizer
        from ..highlighter.language.language_detector import LanguageDetector
        from ..highlighter.language.unicode_language_detector import UnicodeLanguageDetector
        stop_words_tokenizer: StopWordsTokenizer = StopWordsTokenizer()
        start_with_token_highlighter: StartWithTokenHighlighter = StartWithTokenHighlighter(formatter_facade)
        find_and_replace_token_highlighter: FindAndReplaceTokenHighlighter = FindAndReplaceTokenHighlighter(
            formatter_facade)
        language_detector: LanguageDetector = UnicodeLanguageDetector()
        text_highlighter: TextHighlighter = RegexTextHighlighter(
            start_with_token_highlighter, find_and_replace_token_highlighter, formatter_facade, tokenizer,
            stop_words_tokenizer, language_detector)
        return RegexFieldHighlighter(text_highlighter)

    @staticmethod
    def __set_editor_did_init_buttons_hook(config, erase_dialog_controller, highlight_dialog_controller,
                                           note_type_details_factory, regex_field_highlighter, settings) -> None:
        from aqt import gui_hooks
        from ..ui.editor.editor_button_creator import EditorButtonCreator
        from .editor.editor_did_init_buttons_hook import EditorDidInitButtonsHook
        editor_button_creator: EditorButtonCreator = EditorButtonCreator(
            highlight_dialog_controller, erase_dialog_controller, note_type_details_factory,
            regex_field_highlighter, config, settings)
        hook: EditorDidInitButtonsHook = EditorDidInitButtonsHook(editor_button_creator)
        log: Logger = logging.getLogger(__name__)
        log.debug(f"Count of editor_did_init_buttons before adding: {gui_hooks.editor_did_init_buttons.count()}")
        gui_hooks.editor_did_init_buttons.append(hook)
        log.debug(f"Count of editor_did_init_buttons after adding: {gui_hooks.editor_did_init_buttons.count()}")

    @staticmethod
    def __set_browser_will_show_context_menu_hook(addon_manager, config, dialog_manager, dialog_params_factory,
                                                  erase_dialog_controller, highlight_dialog_controller, op_factory,
                                                  settings) -> None:
        from aqt import gui_hooks
        from aqt import QDesktopServices
        from ..config.url_manager import UrlManager
        from .browser.browser_will_show_context_menu_hook import BrowserWillShowContextMenuHook
        desktop_services: QDesktopServices = QDesktopServices()
        url_manager: UrlManager = UrlManager()
        hook: BrowserWillShowContextMenuHook = BrowserWillShowContextMenuHook(
            op_factory, highlight_dialog_controller, erase_dialog_controller, dialog_params_factory,
            addon_manager, dialog_manager, url_manager, desktop_services, config, settings)
        log: Logger = logging.getLogger(__name__)
        log.debug(
            f"Count of browser_will_show_context_menu before adding: {gui_hooks.browser_will_show_context_menu.count()}")
        gui_hooks.browser_will_show_context_menu.append(hook)
        log.debug(
            f"Count of browser_will_show_context_menu after adding: {gui_hooks.browser_will_show_context_menu.count()}")

    @staticmethod
    def __set_browser_will_show_hook(config, dialog_params_factory, erase_dialog_controller,
                                     highlight_dialog_controller, op_factory) -> None:
        from aqt import gui_hooks
        from .browser.browser_will_show_hook import BrowserWillShowHook
        hook: BrowserWillShowHook = BrowserWillShowHook(op_factory, highlight_dialog_controller,
                                                        erase_dialog_controller, dialog_params_factory, config)
        log: Logger = logging.getLogger(__name__)
        log.debug(f"Count of browser_will_show before adding: {gui_hooks.browser_will_show.count()}")
        gui_hooks.browser_will_show.append(hook)
        log.debug(f"Count of browser_will_show after adding: {gui_hooks.browser_will_show.count()}")

    @staticmethod
    def __highlight_dialog_controller(config, formatter_facade, note_type_details_factory, settings,
                                      user_folder_storage):
        from ..ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
        from ..ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import AdhocHighlightDialogModel
        from ..ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model_serde import AdhocHighlightDialogModelSerDe
        from ..ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
        model: AdhocHighlightDialogModel = AdhocHighlightDialogModel()
        view: AdhocHighlightDialogView = AdhocHighlightDialogView(model, settings)
        serde: AdhocHighlightDialogModelSerDe = AdhocHighlightDialogModelSerDe()
        return AdhocHighlightDialogController(model, view, note_type_details_factory, formatter_facade,
                                              serde, config, user_folder_storage)

    @staticmethod
    def __erase_dialog_controller(note_type_details_factory, settings, user_folder_storage):
        from ..ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
        from ..ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel
        from ..ui.dialog.adhoc.erase.adhoc_erase_dialog_model_serde import AdhocEraseDialogModelSerDe
        from ..ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
        model: AdhocEraseDialogModel = AdhocEraseDialogModel()
        view: AdhocEraseDialogView = AdhocEraseDialogView(model, settings)
        serde: AdhocEraseDialogModelSerDe = AdhocEraseDialogModelSerDe()
        return AdhocEraseDialogController(model, view, note_type_details_factory, serde, user_folder_storage)
