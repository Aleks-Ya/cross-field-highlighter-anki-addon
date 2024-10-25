from anki.models import NoteType, NotetypeId

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, FieldName, NoteTypeName
from tests.data import DefaultFields


def test_str(basic_note_type_details: NoteTypeDetails, basic_note_type_id: NotetypeId):
    assert str(basic_note_type_details) == f"NoteTypeDetails({basic_note_type_id}, Basic, [Front, Back])"


def test_repr(basic_note_type_details: NoteTypeDetails, basic_note_type_id: NotetypeId):
    note_type_details: list[NoteTypeDetails] = [basic_note_type_details]
    assert str(note_type_details) == f"[NoteTypeDetails({basic_note_type_id}, Basic, [Front, Back])]"


def test_eq(basic_note_type_details: NoteTypeDetails, cloze_note_type_details: NoteTypeDetails,
            basic_note_type: NoteType, basic_note_type_id: NotetypeId, basic_note_type_name: NoteTypeName):
    assert basic_note_type_details != cloze_note_type_details
    assert basic_note_type_details == NoteTypeDetails(
        basic_note_type_id, basic_note_type_name,
        FieldNames([FieldName(DefaultFields.basic_front_field), FieldName(DefaultFields.basic_back_field)]))
    assert basic_note_type_details != "abc"
