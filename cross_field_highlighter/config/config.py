import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any, Optional

from .config_listener import ConfigListener

log: Logger = logging.getLogger(__name__)


class Config:
    __key_1_dialog: str = 'Dialog'
    __key_2_dialog_adhoc: str = 'Adhoc'
    __key_3_dialog_highlight: str = 'Highlight'
    __key_4_dialog_adhoc_default_stop_words: str = 'Default Stop Words'
    __key_1_latest_modified_notes: str = 'Latest Modified Notes'
    __key_2_latest_modified_notes_enabled: str = 'Enabled'
    __key_2_latest_modified_notes_tag: str = 'Tag'

    def __init__(self, config: dict[str, Any]):
        self.__config: dict[str, Any] = config
        self.__listeners: set[ConfigListener] = set()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __str__(self):
        return str(self.__config)

    @classmethod
    def from_path(cls, path: Path) -> 'Config':
        return cls.from_path_updated(path, {})

    @classmethod
    def from_path_updated(cls, path: Path, overwrites: dict[str, Any]) -> 'Config':
        with Path(path).open() as config_file:
            config_data: dict[str, Any] = json.load(config_file)
        return cls(Config.join(config_data, overwrites))

    @staticmethod
    def join(base: Optional[dict[str, Any]], actual: Optional[dict[str, Any]]) \
            -> dict[str, Any]:
        base: dict[str, Any] = dict(base if base else {})
        actual: dict[str, Any] = actual if actual else {}
        for k, v in actual.items():
            if isinstance(v, dict):
                if k in base:
                    base[k] = Config.join(base.get(k, {}), v)
            else:
                base[k] = v
        return base

    def get_dialog_adhoc_highlight_default_stop_words(self) -> Optional[str]:
        return self.__get(self.__key_1_dialog, self.__key_2_dialog_adhoc,
                          self.__key_3_dialog_highlight, self.__key_4_dialog_adhoc_default_stop_words)

    def set_dialog_adhoc_highlight_default_stop_words(self, last_stop_words: Optional[str]) -> None:
        self.__set(last_stop_words, self.__key_1_dialog, self.__key_2_dialog_adhoc,
                   self.__key_3_dialog_highlight, self.__key_4_dialog_adhoc_default_stop_words)

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

    def get_as_dict(self) -> dict[str, Any]:
        return self.__config

    def add_listener(self, listener: ConfigListener) -> None:
        log.debug(f"Add config listener: {listener}")
        self.__listeners.add(listener)

    def fire_config_changed(self) -> None:
        log.debug("Fire config changed")
        for listener in self.__listeners:
            listener.on_config_changed()

    def __set(self, value: Any, *keys: str) -> None:
        sub_dict: dict[str, Any] = self.__config
        for index, key in enumerate(keys):
            is_last: bool = index == len(keys) - 1
            if is_last:
                sub_dict[key] = value
            else:
                if key not in sub_dict:
                    sub_dict[key] = {}
                sub_dict = sub_dict[key]

    def __get(self, *keys: str) -> Optional[Any]:
        sub_dict: dict[str, Any] = self.__config
        for index, key in enumerate(keys):
            is_last: bool = index == len(keys) - 1
            if is_last:
                return sub_dict[key] if key in sub_dict else None
            else:
                if key in sub_dict:
                    sub_dict = sub_dict[key]
                else:
                    return None
