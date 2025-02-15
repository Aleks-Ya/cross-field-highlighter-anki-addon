import logging
from logging import Logger
from typing import Sequence

from anki.cards import CardId
from anki.notes import NoteId

from ...common.collection_holder import CollectionHolder
from ...highlighter.note_type_details import NoteTypeDetails
from ...highlighter.note_type_details_factory import NoteTypeDetailsFactory
from ...ui.dialog.dialog_params import DialogParams

log: Logger = logging.getLogger(__name__)


class DialogParamsFactory:

    def __init__(self, collection_holder: CollectionHolder, note_type_details_factory: NoteTypeDetailsFactory) -> None:
        self.__collection_holder: CollectionHolder = collection_holder
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_from_note_ids(self, note_ids: Sequence[NoteId]) -> DialogParams:
        selected_note_types: list[NoteTypeDetails] = self.__note_type_details_factory.by_note_ids(note_ids)
        return DialogParams(selected_note_types, len(note_ids))

    def create_from_card_ids(self, card_ids: Sequence[CardId]) -> DialogParams:
        selected_note_ids: Sequence[NoteId] = [self.__collection_holder.col().get_card(card_id).nid for card_id in
                                               card_ids]
        return self.create_from_note_ids(selected_note_ids)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
