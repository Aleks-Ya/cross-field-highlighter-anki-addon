import logging
from logging import Logger
from typing import Sequence

from anki.collection import Collection
from anki.models import NotetypeId, NoteType
from anki.notes import NoteId

from ..highlighter.note_type_details import NoteTypeDetails
from ..highlighter.types import NoteTypeName

log: Logger = logging.getLogger(__name__)


class NoteTypeDetailsFactory:
    def __init__(self, col: Collection):
        self.__col: Collection = col
        self.__cache_id: dict[NotetypeId, NoteTypeDetails] = {}
        self.__cache_name: dict[NoteTypeName, NoteTypeDetails] = {}
        log.debug(f"{self.__class__.__name__} was instantiated")

    def by_note_type_id(self, note_type_id: NotetypeId) -> NoteTypeDetails:
        if note_type_id not in self.__cache_id:
            note_type: NoteType = self.__col.models.get(note_type_id)
            self.__cache_id[note_type_id] = NoteTypeDetails(note_type_id, note_type["name"],
                                                            self.__col.models.field_names(note_type))
        return self.__cache_id[note_type_id]

    def by_note_type_name(self, note_type_name: NoteTypeName) -> NoteTypeDetails:
        if note_type_name not in self.__cache_name:
            note_type: NoteType = self.__col.models.by_name(note_type_name)
            self.__cache_name[note_type_name] = NoteTypeDetails(note_type["id"], note_type_name,
                                                                self.__col.models.field_names(note_type))
        return self.__cache_name[note_type_name]

    def by_note_ids(self, note_ids: Sequence[NoteId]) -> list[NoteTypeDetails]:
        note_type_ids: set[NotetypeId] = {self.__col.get_note(note_id).mid for note_id in note_ids}
        note_types: list[NoteTypeDetails] = []
        for note_type_id in note_type_ids:
            note_type_details: NoteTypeDetails = self.by_note_type_id(note_type_id)
            note_types.append(note_type_details)
        sorted_notes_type: list[NoteTypeDetails] = sorted(note_types, key=lambda n_type: n_type.name)
        return sorted_notes_type
