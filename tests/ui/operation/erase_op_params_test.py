import pytest
from anki.models import NoteType, NotetypeId
from aqt import QWidget

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from tests.data import DefaultFields
from tests.visual_qtbot import VisualQtBot


@pytest.fixture
def parent(visual_qtbot: VisualQtBot) -> QWidget:
    parent: QWidget = QWidget()
    visual_qtbot.add_widget(parent)
    return parent


@pytest.fixture
def params(basic_note_type: NoteType, bold_format: HighlightFormat, parent: QWidget) -> EraseOpParams:
    return EraseOpParams(basic_note_type["id"], parent, FieldNames([DefaultFields.basic_back]))


def test_str(params: EraseOpParams, basic_note_type_id: NotetypeId):
    exp: str = f"EraseOpParams(note_type_id={basic_note_type_id}, fields=Back)"
    assert str(params) == exp
    assert str([params]) == f"[{exp}]"


def test_eq(params: EraseOpParams, basic_note_type: NoteType, parent: QWidget):
    params2: EraseOpParams = EraseOpParams(basic_note_type["id"], parent, FieldNames([DefaultFields.basic_back]))
    assert params == params2
