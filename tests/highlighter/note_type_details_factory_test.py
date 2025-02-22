from anki.models import NotetypeId
from anki.notes import Note, NoteId

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from tests.data import Data


def test_by_note_type_id(note_type_details_factory: NoteTypeDetailsFactory, note_type_id_basic: NotetypeId,
                         note_type_details_basic: NoteTypeDetails):
    assert note_type_details_factory.by_note_type_id(note_type_id_basic) == note_type_details_basic
    assert note_type_details_factory.by_note_type_id(note_type_id_basic) == note_type_details_factory.by_note_type_id(
        note_type_id_basic)


def test_by_note_ids(note_type_details_factory: NoteTypeDetailsFactory, td: Data,
                     note_type_details_basic: NoteTypeDetails, note_type_details_cloze: NoteTypeDetails):
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    note_3: Note = td.create_cloze_note()
    note_ids: list[NoteId] = [note_1.id, note_2.id, note_3.id]
    assert note_type_details_factory.by_note_ids(note_ids) == [note_type_details_basic, note_type_details_cloze]


def test_get_all(note_type_details_factory: NoteTypeDetailsFactory, note_type_details_all: list[NoteTypeDetails]):
    assert note_type_details_factory.get_all() == note_type_details_all
    assert note_type_details_factory.get_all() == note_type_details_factory.get_all()
