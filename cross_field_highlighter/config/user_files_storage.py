import json
import logging
from logging import Logger
from pathlib import Path

from aqt import ProfileManager

from .settings import Settings

log: Logger = logging.getLogger(__name__)


class UserFilesStorage:
    def __init__(self, profile_manager: ProfileManager, settings: Settings):
        self.__profile_manager: ProfileManager = profile_manager
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
        log.debug(f"Write storage to file {storage_file}: {current_data}")

    def read_all(self) -> dict[str, any]:
        storage_file: Path = self.__get_storage_file()
        result: dict[str, any] = {}
        if storage_file.exists():
            with open(storage_file, 'r') as f:
                result = json.load(f)
        log.debug(f"Read storage from file '{storage_file}': {result}")
        return result

    def __get_storage_file(self) -> Path:
        return self.__settings.user_files / "storage" / f"{self.__profile_manager.name}.json"

    def __str__(self):
        return f"UserFilesStorage({self.__get_storage_file()})"
