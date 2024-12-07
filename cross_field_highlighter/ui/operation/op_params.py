import logging
from abc import ABC
from logging import Logger

from anki.models import NotetypeId

log: Logger = logging.getLogger(__name__)


class OpParams(ABC):
    def __init__(self, note_type_id: NotetypeId):
        self.note_type_id: NotetypeId = note_type_id

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
