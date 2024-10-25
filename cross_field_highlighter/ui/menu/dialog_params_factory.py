import logging
from logging import Logger
from typing import Sequence

from anki.cards import CardId
from anki.collection import Collection
from anki.notes import NoteId

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams

log: Logger = logging.getLogger(__name__)


class DialogParamsFactory:

    def __init__(self, col: Collection, note_type_details_factory: NoteTypeDetailsFactory) -> None:
        self.__col: Collection = col
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_from_note_ids(self, note_ids: Sequence[NoteId]) -> DialogParams:
        notes_type_details: list[NoteTypeDetails] = self.__note_type_details_factory.by_note_ids(note_ids)
        params: DialogParams = DialogParams(notes_type_details, note_ids)
        log.debug(f"Created DialogParams: {params}")
        return params

    def create_from_card_ids(self, card_ids: Sequence[CardId]) -> DialogParams:
        selected_note_ids: Sequence[NoteId] = [self.__col.get_card(card_id).nid for card_id in card_ids]
        return self.create_from_note_ids(selected_note_ids)
