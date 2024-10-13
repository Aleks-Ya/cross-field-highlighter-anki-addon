import logging
from abc import abstractmethod
from logging import Logger

log: Logger = logging.getLogger(__name__)


class ConfigListener:
    @abstractmethod
    def on_config_changed(self):
        pass
