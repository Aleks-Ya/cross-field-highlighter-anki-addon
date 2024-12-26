import logging
from logging import Logger
from pathlib import Path
import json

from .settings import Settings

log: Logger = logging.getLogger(__name__)


class UserFolderStorage:
    def __init__(self, settings: Settings):
        self.__storage_file: Path = settings.user_folder / "storage.json"
        log.debug(f"{self.__class__.__name__} was instantiated")

    def read(self, key: str) -> dict[str, any]:
        return self.read_all().get(key, {})

    def write(self, key: str, value: dict[str, any]) -> None:
        if not self.__storage_file.parent.exists():
            self.__storage_file.parent.mkdir(parents=True)
        current_data: dict[str, any] = self.read_all()
        current_data[key] = value
        with open(self.__storage_file, 'w') as f:
            # noinspection PyTypeChecker
            json.dump(current_data, f, indent=2)

    def read_all(self) -> dict[str, any]:
        if self.__storage_file.exists():
            with open(self.__storage_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def __str__(self):
        return f"UserFolderStorage({self.__storage_file})"
