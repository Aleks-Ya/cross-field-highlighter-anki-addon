import logging
from logging import Logger
from typing import Optional

from .config_listener import ConfigListener
from .config_loader import ConfigLoader, ConfigData

log: Logger = logging.getLogger(__name__)


class Config:
    __key_1_dialog: str = 'Dialog'
    __key_2_dialog_adhoc: str = 'Adhoc'
    __key_3_dialog_adhoc_highlight: str = 'Highlight'
    __key_4_dialog_adhoc_highlight_default_stop_words: str = 'Default Stop Words'
    __key_4_dialog_adhoc_highlight_editor_shortcut: str = 'Editor Shortcut'
    __key_3_dialog_adhoc_erase: str = 'Erase'
    __key_4_dialog_adhoc_erase_editor_shortcut: str = 'Editor Shortcut'
    __key_1_latest_modified_notes: str = 'Latest Modified Notes'
    __key_2_latest_modified_notes_enabled: str = 'Enabled'
    __key_2_latest_modified_notes_tag: str = 'Tag'

    def __init__(self, config_loader: ConfigLoader):
        self.__config_loader: ConfigLoader = config_loader
        self.__listeners: set[ConfigListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def get_dialog_adhoc_highlight_default_stop_words(self) -> Optional[str]:
        return self.__get(self.__key_1_dialog, self.__key_2_dialog_adhoc,
                          self.__key_3_dialog_adhoc_highlight, self.__key_4_dialog_adhoc_highlight_default_stop_words)

    def set_dialog_adhoc_highlight_default_stop_words(self, last_stop_words: Optional[str]) -> None:
        self.__set(last_stop_words, self.__key_1_dialog, self.__key_2_dialog_adhoc,
                   self.__key_3_dialog_adhoc_highlight, self.__key_4_dialog_adhoc_highlight_default_stop_words)

    def get_dialog_adhoc_highlight_editor_shortcut(self) -> Optional[str]:
        return self.__get_shortcut(self.__key_1_dialog, self.__key_2_dialog_adhoc,
                                   self.__key_3_dialog_adhoc_highlight,
                                   self.__key_4_dialog_adhoc_highlight_editor_shortcut)

    def set_dialog_adhoc_highlight_editor_shortcut(self, editor_shortcut: Optional[str]) -> None:
        self.__set(editor_shortcut, self.__key_1_dialog, self.__key_2_dialog_adhoc,
                   self.__key_3_dialog_adhoc_highlight, self.__key_4_dialog_adhoc_highlight_editor_shortcut)

    def get_dialog_adhoc_erase_editor_shortcut(self) -> Optional[str]:
        return self.__get_shortcut(self.__key_1_dialog, self.__key_2_dialog_adhoc,
                                   self.__key_3_dialog_adhoc_erase, self.__key_4_dialog_adhoc_erase_editor_shortcut)

    def set_dialog_adhoc_erase_editor_shortcut(self, editor_shortcut: Optional[str]) -> None:
        self.__set(editor_shortcut, self.__key_1_dialog, self.__key_2_dialog_adhoc,
                   self.__key_3_dialog_adhoc_erase, self.__key_4_dialog_adhoc_erase_editor_shortcut)

    def get_latest_modified_notes_enabled(self) -> Optional[bool]:
        return self.__get(self.__key_1_latest_modified_notes, self.__key_2_latest_modified_notes_enabled)

    def set_latest_modified_notes_enabled(self, latest_modified_notes_enabled: Optional[bool]) -> None:
        self.__set(latest_modified_notes_enabled, self.__key_1_latest_modified_notes,
                   self.__key_2_latest_modified_notes_enabled)

    def get_latest_modified_notes_tag(self) -> Optional[str]:
        return self.__get(self.__key_1_latest_modified_notes, self.__key_2_latest_modified_notes_tag)

    def set_latest_modified_notes_tag(self, latest_modified_notes_tag: Optional[str]) -> None:
        self.__set(latest_modified_notes_tag, self.__key_1_latest_modified_notes,
                   self.__key_2_latest_modified_notes_tag)

    def get_config_data(self) -> ConfigData:
        return self.__config_loader.load_config()

    def add_listener(self, listener: ConfigListener) -> None:
        log.debug(f"Add config listener: {listener}")
        self.__listeners.add(listener)

    def fire_config_changed(self) -> None:
        log.debug("Fire config changed")
        for listener in self.__listeners:
            listener.on_config_changed()

    def __get_shortcut(self, *keys: str) -> Optional[str]:
        shortcut: Optional[str] = self.__get(*keys)
        return shortcut.replace("-", "+") if shortcut is not None and shortcut.strip() != "" else None

    def __set(self, value: any, *keys: str) -> None:
        log.debug(f"Set config value: {value} for keys: {keys}")
        config_data: ConfigData = self.__config_loader.load_config()
        sub_dict: ConfigData = config_data
        for index, key in enumerate(keys):
            is_last: bool = index == len(keys) - 1
            if is_last:
                sub_dict[key] = value
            else:
                if key not in sub_dict:
                    sub_dict[key] = {}
                sub_dict = sub_dict[key]
        self.__config_loader.write_config(config_data)

    def __get(self, *keys: str) -> Optional[any]:
        log.debug(f"Get config value for keys: {keys}")
        sub_dict: ConfigData = self.__config_loader.load_config()
        for index, key in enumerate(keys):
            is_last: bool = index == len(keys) - 1
            if is_last:
                return sub_dict[key] if key in sub_dict else None
            else:
                if key in sub_dict:
                    sub_dict = sub_dict[key]
                else:
                    return None
