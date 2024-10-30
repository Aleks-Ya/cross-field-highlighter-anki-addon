import pytest
from anki.models import NotetypeId
from anki.notes import NoteId
from pytestqt.qtbot import QtBot
from aqt import QWidget

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldNames, Text
from cross_field_highlighter.ui.operation.highlight_op_params import HighlightOpParams
from tests.data import DefaultFields, Data


@pytest.fixture
def note_ids(td: Data) -> set[NoteId]:
    return {td.create_basic_note_1().id, td.create_basic_note_2().id}


@pytest.fixture
def parent(qtbot: QtBot) -> QWidget:
    parent: QWidget = QWidget()
    qtbot.addWidget(parent)
    return parent


@pytest.fixture
def params(basic_note_type_id: NotetypeId, note_ids: set[NoteId], bold_format: HighlightFormat,
           parent: QWidget) -> HighlightOpParams:
    stop_words: Text = Text("a an")
    return HighlightOpParams(basic_note_type_id, note_ids, parent, DefaultFields.basic_front,
                             FieldNames([DefaultFields.basic_back]), stop_words,
                             bold_format)


def test_str(params: HighlightOpParams, note_ids: set[NoteId], basic_note_type_id: NotetypeId):
    exp: str = (f"HighlightOpParams(note_type_id={basic_note_type_id}, "
                f"note_ids={sorted(note_ids)}, source_field=Front, destination_fields=Back, "
                "stop_words='a an', highlight_format=HighlightFormat(Bold, BOLD))")
    assert str(params) == exp
    assert str([params]) == f"[{exp}]"


def test_eq(params: HighlightOpParams, basic_note_type_id: NotetypeId, parent: QWidget, note_ids: set[NoteId],
            bold_format: HighlightFormat):
    stop_words: Text = Text("a an")
    params2: HighlightOpParams = HighlightOpParams(basic_note_type_id, note_ids, parent,
                                                   DefaultFields.basic_front,
                                                   FieldNames([DefaultFields.basic_back]), stop_words,
                                                   bold_format)
    assert params == params2
