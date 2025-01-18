import json
import logging
from logging import Logger
from pathlib import Path

from .settings import Settings

log: Logger = logging.getLogger(__name__)


class UserFolderStorage:
    def __init__(self, settings: Settings):
        self.__settings: Settings = settings
        log.debug(f"{self.__class__.__name__} was instantiated")

    def read(self, key: str) -> dict[str, any]:
        return self.read_all().get(key, {})

    def write(self, key: str, value: dict[str, any]) -> None:
        storage_file: Path = self.__get_storage_file()
        if not storage_file.parent.exists():
            storage_file.parent.mkdir(parents=True)
        current_data: dict[str, any] = self.read_all()
        current_data[key] = value
        with open(storage_file, 'w') as f:
            # noinspection PyTypeChecker
            json.dump(current_data, f, indent=2)

    def read_all(self) -> dict[str, any]:
        storage_file: Path = self.__get_storage_file()
        if storage_file.exists():
            with open(storage_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def __get_storage_file(self) -> Path:
        return self.__settings.user_folder / "storage.json"

    def __str__(self):
        return f"UserFolderStorage({self.__get_storage_file()})"
