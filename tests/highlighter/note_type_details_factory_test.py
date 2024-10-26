from anki.models import NotetypeId
from anki.notes import Note, NoteId

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import NoteTypeName
from tests.data import Data


def test_by_note_type_id(note_type_details_factory: NoteTypeDetailsFactory, basic_note_type_id: NotetypeId,
                         basic_note_type_details: NoteTypeDetails):
    assert note_type_details_factory.by_note_type_id(basic_note_type_id) == basic_note_type_details


def test_by_note_type_name(note_type_details_factory: NoteTypeDetailsFactory, basic_note_type_name: NoteTypeName,
                           basic_note_type_details: NoteTypeDetails):
    assert note_type_details_factory.by_note_type_name(basic_note_type_name) == basic_note_type_details


def test_by_note_ids(note_type_details_factory: NoteTypeDetailsFactory, td: Data,
                     basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails):
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    note_3: Note = td.create_cloze_note()
    note_ids: list[NoteId] = [note_1.id, note_2.id, note_3.id]
    assert note_type_details_factory.by_note_ids(note_ids) == [basic_note_type_details, cloze_note_type_details]
