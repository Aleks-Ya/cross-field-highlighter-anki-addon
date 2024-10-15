import logging
from logging import Logger
from typing import Sequence

from anki.cards import CardId
from anki.collection import Collection
from anki.models import NotetypeId, NoteType
from anki.notes import NoteId

from cross_field_highlighter.highlighter.types import NoteTypeDetails
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams

log: Logger = logging.getLogger(__name__)


class DialogParamsFactory:

    def __init__(self, col: Collection) -> None:
        self.__col: Collection = col
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_from_note_ids(self, note_ids: Sequence[NoteId]) -> DialogParams:
        note_type_ids: set[NotetypeId] = {self.__col.get_note(note_id).mid for note_id in note_ids}
        note_types: list[NoteTypeDetails] = []
        for note_type_id in note_type_ids:
            note_type: NoteType = self.__col.models.get(note_type_id)
            note_type_details: NoteTypeDetails = NoteTypeDetails(
                note_type_id, note_type["name"], self.__col.models.field_names(note_type))
            note_types.append(note_type_details)
        sorted_notes_type: list[NoteTypeDetails] = sorted(note_types, key=lambda n_type: n_type.name)
        params: DialogParams = DialogParams(sorted_notes_type, note_ids)
        log.debug(f"Created DialogParams: {params}")
        return params

    def create_from_card_ids(self, card_ids: Sequence[CardId]) -> DialogParams:
        selected_note_ids: Sequence[NoteId] = [self.__col.get_card(card_id).nid for card_id in card_ids]
        return self.create_from_note_ids(selected_note_ids)
