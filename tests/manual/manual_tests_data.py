#!/usr/bin/env python3
from pathlib import Path

import yaml
from anki.collection import Collection, AddNoteRequest
from anki.decks import DeckId
from anki.models import NoteType
from anki.notes import Note
from aqt import ProfileManager


def generate_cfh_1():
    col: Collection = _recreate_profile("CFH Manual Test 1")
    deck_id: DeckId = col.decks.get_current_id()
    for case in _load_cases():
        col.add_note(_add_basic_note(col, case["collocation"], case["original_text"]), deck_id)
    col.add_note(_add_cloze_note(col, "study", "I {{c1:study}} every day."), deck_id)
    col.close()


def generate_cfh_2():
    col: Collection = _recreate_profile("CFH Manual Test 2")
    deck_id: DeckId = col.decks.get_current_id()
    col.add_note(_add_basic_note(col, "nice", "What a nice day!"), deck_id)
    col.add_note(_add_basic_note(col, "素晴らしい", "素晴らしい一日でした！"), deck_id)
    col.add_note(_add_cloze_note(col, "blow", "Wind {{c1:blows}} from the North."), deck_id)
    col.close()


def generate_cfh_3_big():
    col: Collection = _recreate_profile("CFH Manual Test 3 Big")
    deck_id: DeckId = col.decks.get_current_id()
    note_count: int = 50000
    requests: list[AddNoteRequest] = []
    for i in range(note_count):
        requests.append(AddNoteRequest(_add_basic_note(col, f"Front field {i}", f"Back field {i}"), deck_id))
        requests.append(AddNoteRequest(_add_cloze_note(col, f"Text field {i}", f"Back Extra field {i}"), deck_id))
    col.add_notes(requests)
    col.close()


def _load_cases() -> list[dict]:
    yaml_file: Path = Path(__file__).parent.parent / "cases.yaml"
    return yaml.safe_load(yaml_file.read_text(encoding="utf-8"))


def _recreate_profile(profile_name: str) -> Collection:
    base_dir: Path = ProfileManager.get_created_base_folder(None)
    pm: ProfileManager = ProfileManager(base=base_dir)
    pm.setupMeta()
    if profile_name in pm.profiles():
        pm.openProfile(profile_name)
        pm.remove(profile_name)
    pm.create(profile_name)
    pm.openProfile(profile_name)
    pm.save()
    return Collection(pm.collectionPath())


def _add_basic_note(col: Collection, front: str, back: str) -> Note:
    note_type: NoteType = col.models.by_name('Basic')
    note: Note = col.new_note(note_type)
    note["Front"] = front
    note["Back"] = back
    return note


def _add_cloze_note(col: Collection, text: str, back_extra: str) -> Note:
    note_type: NoteType = col.models.by_name('Cloze')
    note: Note = col.new_note(note_type)
    note["Text"] = text
    note["Back Extra"] = back_extra
    return note


def main():
    generate_cfh_1()
    generate_cfh_2()
    generate_cfh_3_big()


if __name__ == "__main__":
    main()
