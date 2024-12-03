import pytest
from anki.models import NotetypeId
from anki.notes import NoteId
from aqt import QWidget

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldNames, Text
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from tests.data import DefaultFields, Data
from tests.visual_qtbot import VisualQtBot


@pytest.fixture
def note_ids(td: Data) -> set[NoteId]:
    return {td.create_basic_note_1().id, td.create_basic_note_2().id}


@pytest.fixture
def parent(visual_qtbot: VisualQtBot) -> QWidget:
    parent: QWidget = QWidget()
    visual_qtbot.addWidget(parent)
    return parent


@pytest.fixture
def params(basic_note_type_id: NotetypeId, note_ids: set[NoteId], bold_format: HighlightFormat,
           parent: QWidget) -> HighlightOpParams:
    stop_words: Text = Text("a an")
    space_delimited_language: bool = True
    return HighlightOpParams(basic_note_type_id, list(note_ids), parent, DefaultFields.basic_front,
                             space_delimited_language, FieldNames([DefaultFields.basic_back]), stop_words, bold_format)


def test_str(params: HighlightOpParams, note_ids: set[NoteId], basic_note_type_id: NotetypeId):
    exp: str = (f"HighlightOpParams(note_type_id={basic_note_type_id}, note_ids={sorted(note_ids)}, "
                "source_field=Front, space_delimited_language=True, destination_fields=Back, "
                "stop_words='a an', highlight_format=HighlightFormat(Bold, BOLD))")
    assert str(params) == exp
    assert str([params]) == f"[{exp}]"


def test_eq(params: HighlightOpParams, basic_note_type_id: NotetypeId, parent: QWidget, note_ids: set[NoteId],
            bold_format: HighlightFormat):
    stop_words: Text = Text("a an")
    space_delimited_language: bool = True
    params2: HighlightOpParams = HighlightOpParams(basic_note_type_id, list(note_ids), parent,
                                                   DefaultFields.basic_front, space_delimited_language,
                                                   FieldNames([DefaultFields.basic_back]), stop_words,
                                                   bold_format)
    assert params == params2
