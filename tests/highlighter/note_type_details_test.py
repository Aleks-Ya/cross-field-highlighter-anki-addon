from anki.models import NoteType, NotetypeId

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, FieldName, NoteTypeName
from tests.data import DefaultFields


def test_str(note_type_details_basic: NoteTypeDetails, note_type_id_basic: NotetypeId):
    assert str(note_type_details_basic) == f"NoteTypeDetails({note_type_id_basic}, Basic, [Front, Back, Extra])"


def test_repr(note_type_details_basic: NoteTypeDetails, note_type_id_basic: NotetypeId):
    note_type_details: list[NoteTypeDetails] = [note_type_details_basic]
    assert str(note_type_details) == f"[NoteTypeDetails({note_type_id_basic}, Basic, [Front, Back, Extra])]"


def test_eq(note_type_details_basic: NoteTypeDetails, note_type_details_cloze: NoteTypeDetails,
            note_type_basic: NoteType, note_type_id_basic: NotetypeId, note_type_name_basic: NoteTypeName):
    assert note_type_details_basic != note_type_details_cloze
    assert note_type_details_basic == NoteTypeDetails(note_type_id_basic, note_type_name_basic,
                                                      FieldNames([FieldName(DefaultFields.basic_front),
                                                                  FieldName(DefaultFields.basic_back),
                                                                  FieldName(DefaultFields.basic_extra)]))
    assert note_type_details_basic != "abc"
