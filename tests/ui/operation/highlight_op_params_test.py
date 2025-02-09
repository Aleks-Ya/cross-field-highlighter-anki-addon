import pytest
from anki.models import NotetypeId

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldNames, Text
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from tests.data import DefaultFields


@pytest.fixture
def params(basic_note_type_id: NotetypeId, bold_format: HighlightFormat) -> HighlightOpParams:
    stop_words: Text = Text("a an")
    return HighlightOpParams(basic_note_type_id, DefaultFields.basic_front, FieldNames([DefaultFields.basic_back]),
                             stop_words, bold_format)


def test_str(params: HighlightOpParams, basic_note_type_id: NotetypeId):
    exp: str = (f"HighlightOpParams(note_type_id={basic_note_type_id}, "
                "source_field=Front, destination_fields=Back, "
                "stop_words='a an', highlight_format=HighlightFormat(Bold, BOLD))")
    assert str(params) == exp
    assert str([params]) == f"[{exp}]"


def test_eq(params: HighlightOpParams, basic_note_type_id: NotetypeId, bold_format: HighlightFormat):
    stop_words: Text = Text("a an")
    params2: HighlightOpParams = HighlightOpParams(basic_note_type_id, DefaultFields.basic_front,
                                                   FieldNames([DefaultFields.basic_back]), stop_words, bold_format)
    assert params == params2
