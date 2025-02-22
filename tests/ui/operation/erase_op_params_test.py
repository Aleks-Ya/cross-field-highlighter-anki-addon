import pytest
from anki.models import NoteType, NotetypeId

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from tests.data import DefaultFields


@pytest.fixture
def params(note_type_basic: NoteType, bold_format: HighlightFormat) -> EraseOpParams:
    return EraseOpParams(note_type_basic["id"], FieldNames([DefaultFields.basic_back]))


def test_str(params: EraseOpParams, note_type_id_basic: NotetypeId):
    exp: str = f"EraseOpParams(note_type_id={note_type_id_basic}, fields=Back)"
    assert str(params) == exp
    assert str([params]) == f"[{exp}]"


def test_eq(params: EraseOpParams, note_type_basic: NoteType):
    params2: EraseOpParams = EraseOpParams(note_type_basic["id"], FieldNames([DefaultFields.basic_back]))
    assert params == params2
