from pathlib import Path

import pytest
from anki.collection import Collection, AddNoteRequest
from anki.decks import DeckId
from anki.models import NoteType
from anki.notes import Note
from aqt import ProfileManager

from tests.data import Data


@pytest.mark.skip(reason="For manual running")
class TestProfilesForManualTesting:

    def test_generate_cfh_1(self, td: Data):
        col: Collection = self.__recreate_profile("CFH Manual Test 1")
        deck_id: DeckId = col.decks.get_current_id()
        for case in td.cases():
            col.add_note(self.__add_basic_note(col, case.collocation, case.original_text), deck_id)
        col.add_note(self.__add_cloze_note(col, "study", "I {{c1:study}} every day."), deck_id)
        col.close()

    def test_generate_cfh_2(self, td: Data):
        col: Collection = self.__recreate_profile("CFH Manual Test 2")
        deck_id: DeckId = col.decks.get_current_id()
        col.add_note(self.__add_basic_note(col, "nice", "What a nice day!"), deck_id)
        col.add_note(self.__add_basic_note(col, "素晴らしい", "素晴らしい一日でした！"), deck_id)
        col.add_note(self.__add_cloze_note(col, "blow", "Wind {{c1:blows}} from the North."), deck_id)
        col.close()

    @pytest.mark.skip(reason="For manual running")
    def test_generate_cfh_3_big(self, td: Data):
        col: Collection = self.__recreate_profile("CFH Manual Test 3 Big")
        deck_id: DeckId = col.decks.get_current_id()
        note_count: int = 50000
        requests: list[AddNoteRequest] = []
        for i in range(note_count):
            requests.append(AddNoteRequest(
                self.__add_basic_note(col, f"Front field {i}", f"Back field {i}"),
                deck_id))
            requests.append(AddNoteRequest(
                self.__add_cloze_note(col, f"Text field {i}", f"Back Extra field {i}"),
                deck_id))
        col.add_notes(requests)
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
    def __add_basic_note(col: Collection, front: str, back: str) -> Note:
        note_type: NoteType = col.models.by_name('Basic')
        note: Note = col.new_note(note_type)
        note["Front"] = front
        note["Back"] = back
        return note

    @staticmethod
    def __add_cloze_note(col: Collection, text: str, back_extra: str) -> Note:
        note_type: NoteType = col.models.by_name('Cloze')
        note: Note = col.new_note(note_type)
        note["Text"] = text
        note["Back Extra"] = back_extra
        return note
