import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any, Optional

from .config_listener import ConfigListener
from ..highlighter.formatter.highlight_format import HighlightFormat
from ..highlighter.types import FieldName, FieldNames

log: Logger = logging.getLogger(__name__)


class Config:
    __key_1_dialog: str = 'Dialog'
    __key_2_dialog_adhoc: str = 'Adhoc'
    __key_3_dialog_highlight: str = 'Highlight'
    __key_3_dialog_erase: str = 'Erase'
    __key_4_dialog_adhoc_last_note_type: str = 'Last Note Type'
    __key_4_dialog_adhoc_last_source_field_name: str = 'Last Source Field Name'
    __key_4_dialog_adhoc_last_format: str = 'Last Format'
    __key_4_dialog_adhoc_last_destination_field_name: str = 'Last Destination Field Name'
    __key_4_dialog_erase_last_note_type: str = 'Last Note Type'
    __key_4_dialog_erase_last_field_names: str = 'Last Field Names'

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
            if k in base:
                if isinstance(v, dict):
                    base[k] = Config.join(base.get(k, {}), v)
                else:
                    base[k] = v
        return base

    def get_dialog_adhoc_highlight_last_note_type(self) -> str:
        return self.__config[self.__key_1_dialog][self.__key_2_dialog_adhoc][self.__key_3_dialog_highlight][
            self.__key_4_dialog_adhoc_last_note_type]

    def set_dialog_adhoc_highlight_last_note_type(self, last_note_type: str) -> None:
        self.__set(last_note_type, self.__key_1_dialog, self.__key_2_dialog_adhoc, self.__key_3_dialog_highlight,
                   self.__key_4_dialog_adhoc_last_note_type)

    def get_dialog_adhoc_highlight_last_source_field_name(self) -> Optional[FieldName]:
        field: str = self.__config[self.__key_1_dialog][self.__key_2_dialog_adhoc][self.__key_3_dialog_highlight][
            self.__key_4_dialog_adhoc_last_source_field_name]
        return FieldName(field) if field else None

    def set_dialog_adhoc_highlight_last_source_field_name(self, last_source_field_name: FieldName) -> None:
        self.__set(last_source_field_name, self.__key_1_dialog, self.__key_2_dialog_adhoc,
                   self.__key_3_dialog_highlight, self.__key_4_dialog_adhoc_last_source_field_name)

    def get_dialog_adhoc_highlight_last_format(self) -> Optional[HighlightFormat]:
        highlight_format: str = \
            self.__config[self.__key_1_dialog][self.__key_2_dialog_adhoc][self.__key_3_dialog_highlight][
                self.__key_4_dialog_adhoc_last_format]
        return HighlightFormat(highlight_format) if highlight_format else None

    def set_dialog_adhoc_highlight_last_format(self, last_format: HighlightFormat) -> None:
        self.__set(last_format.name, self.__key_1_dialog, self.__key_2_dialog_adhoc, self.__key_3_dialog_highlight,
                   self.__key_4_dialog_adhoc_last_format)

    def get_dialog_adhoc_highlight_last_destination_field_name(self) -> Optional[FieldName]:
        field: str = self.__config[self.__key_1_dialog][self.__key_2_dialog_adhoc][self.__key_3_dialog_highlight][
            self.__key_4_dialog_adhoc_last_destination_field_name]
        return FieldName(field) if field else None

    def set_dialog_adhoc_highlight_last_destination_field_name(self, last_destination_field_name: FieldName) -> None:
        self.__set(last_destination_field_name, self.__key_1_dialog, self.__key_2_dialog_adhoc,
                   self.__key_3_dialog_highlight, self.__key_4_dialog_adhoc_last_destination_field_name)

    def get_dialog_adhoc_erase_last_note_type(self) -> str:
        return self.__config[self.__key_1_dialog][self.__key_2_dialog_adhoc][self.__key_3_dialog_erase][
            self.__key_4_dialog_erase_last_note_type]

    def set_dialog_adhoc_erase_last_note_type(self, last_note_type: str) -> None:
        self.__set(last_note_type, self.__key_1_dialog, self.__key_2_dialog_adhoc, self.__key_3_dialog_erase,
                   self.__key_4_dialog_erase_last_note_type)

    def get_dialog_adhoc_erase_last_field_names(self) -> FieldNames:
        fields: list[str] = self.__config[self.__key_1_dialog][self.__key_2_dialog_adhoc][self.__key_3_dialog_erase][
            self.__key_4_dialog_erase_last_field_names]
        return FieldNames([FieldName(field) for field in fields])

    def set_dialog_adhoc_erase_last_field_names(self, last_field_names: FieldNames) -> None:
        self.__set(last_field_names, self.__key_1_dialog, self.__key_2_dialog_adhoc, self.__key_3_dialog_erase,
                   self.__key_4_dialog_erase_last_field_names)

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
        d: dict[str, Any] = self.__config
        for index, key in enumerate(keys):
            is_last: bool = index == len(keys) - 1
            if is_last:
                d[key] = value
            else:
                if key not in d:
                    d[key] = {}
                d = d[key]
