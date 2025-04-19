from pathlib import Path

import pytest
from anki.collection import Collection
from anki.decks import DeckId
from anki.models import NoteType
from anki.notes import Note
from aqt import ProfileManager

from tests.data import Data


@pytest.mark.skip(reason="For manual running")
class TestProfilesForManualTesting:

    def test_generate_cfh_1(self, td: Data):
        col: Collection = self.__recreate_profile("CFH Manual Test 1")
        for case in td.cases():
            self.__add_basic_note(col, case.collocation, case.original_text)
        self.__add_cloze_note(col, "study", "I {{c1:study}} every day.", )
        col.close()

    def test_generate_cfh_2(self, td: Data):
        col: Collection = self.__recreate_profile("CFH Manual Test 2")
        self.__add_basic_note(col, "nice", "What a nice day!")
        self.__add_basic_note(col, "素晴らしい", "素晴らしい一日でした！")
        self.__add_cloze_note(col, "blow", "Wind {{c1:blows}} from the North.", )
        col.close()

    @staticmethod
    def __recreate_profile(profile_name) -> Collection:
        base_dir: Path = ProfileManager.get_created_base_folder(None)
        pm: ProfileManager = ProfileManager(base=base_dir)
        pm.setupMeta()
        profile_list: list[str] = pm.profiles()
        if profile_name in profile_list:
            pm.openProfile(profile_name)
            pm.remove(profile_name)
        pm.create(profile_name)
        pm.openProfile(profile_name)
        pm.save()
        return Collection(pm.collectionPath())

    @staticmethod
    def __add_basic_note(col: Collection, front: str, back: str) -> None:
        deck_id: DeckId = col.decks.get_current_id()
        note_type: NoteType = col.models.by_name('Basic')
        note: Note = col.new_note(note_type)
        note["Front"] = front
        note["Back"] = back
        col.add_note(note, deck_id)

    @staticmethod
    def __add_cloze_note(col: Collection, text: str, back_extra: str) -> None:
        deck_id: DeckId = col.decks.get_current_id()
        note_type: NoteType = col.models.by_name('Cloze')
        note: Note = col.new_note(note_type)
        note["Text"] = text
        note["Back Extra"] = back_extra
        col.add_note(note, deck_id)
