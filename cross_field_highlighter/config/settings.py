import logging
from logging import Logger
from pathlib import Path

log: Logger = logging.getLogger(__name__)


class Settings:

    def __init__(self, module_dir: Path, module_name: str, logs_folder: Path, version: str) -> None:
        self.module_dir: Path = module_dir
        self.module_name: str = module_name
        self.logs_folder: Path = logs_folder
        self.user_files: Path = self.module_dir / "user_files"
        self.version: str = version
        log.debug(f"{self.__class__.__name__} was instantiated: {self}")

    def __str__(self) -> str:
        return (f"{self.__class__.__name__}(module_dir={self.module_dir}, module_name={self.module_name}, "
                f"logs_folder={self.logs_folder}, user_files={self.user_files}, version={self.version})")
