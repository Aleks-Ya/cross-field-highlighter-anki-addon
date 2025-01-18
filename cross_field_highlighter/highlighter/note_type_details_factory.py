import logging
from logging import Logger
from typing import Sequence

from anki.models import NotetypeId, NoteType
from anki.notes import NoteId

from ..common.collection_holder import CollectionHolder
from ..highlighter.note_type_details import NoteTypeDetails
from ..highlighter.types import NoteTypeName

log: Logger = logging.getLogger(__name__)


class NoteTypeDetailsFactory:
    def __init__(self, collection_holder: CollectionHolder):
        self.__collection_holder: CollectionHolder = collection_holder
        self.__cache_id: dict[NotetypeId, NoteTypeDetails] = {}
        self.__cache_name: dict[NoteTypeName, NoteTypeDetails] = {}
        log.debug(f"{self.__class__.__name__} was instantiated")

    def by_note_type_id(self, note_type_id: NotetypeId) -> NoteTypeDetails:
        if note_type_id not in self.__cache_id:
            note_type: NoteType = self.__collection_holder.col().models.get(note_type_id)
            self.__cache_id[note_type_id] = NoteTypeDetails(note_type_id, note_type["name"],
                                                            self.__collection_holder.col().models.field_names(
                                                                note_type))
        return self.__cache_id[note_type_id]

    def by_note_type_name(self, note_type_name: NoteTypeName) -> NoteTypeDetails:
        if note_type_name not in self.__cache_name:
            note_type: NoteType = self.__collection_holder.col().models.by_name(note_type_name)
            self.__cache_name[note_type_name] = NoteTypeDetails(note_type["id"], note_type_name,
                                                                self.__collection_holder.col().models.field_names(
                                                                    note_type))
        return self.__cache_name[note_type_name]

    def by_note_ids(self, note_ids: Sequence[NoteId]) -> list[NoteTypeDetails]:
        log.debug(f"Collecting note types for note ids: {len(note_ids)}")
        note_type_ids: set[NotetypeId] = {self.__collection_holder.col().get_note(note_id).mid for note_id in note_ids}
        note_types: list[NoteTypeDetails] = []
        for note_type_id in note_type_ids:
            note_type_details: NoteTypeDetails = self.by_note_type_id(note_type_id)
            note_types.append(note_type_details)
        sorted_notes_type: list[NoteTypeDetails] = sorted(note_types, key=lambda n_type: n_type.name)
        log.debug(f"Collected note types: {NoteTypeDetails.names(sorted_notes_type)}")
        return sorted_notes_type
