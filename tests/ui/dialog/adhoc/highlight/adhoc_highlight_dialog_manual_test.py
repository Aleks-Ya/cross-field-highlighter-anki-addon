import sys

import pytest
from anki.notes import Note, NoteId
from pytestqt.qtbot import QtBot

from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from tests.data import Data


@pytest.mark.skip(reason="For manual running")
def test_show_highlight_dialog(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                               adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                               dialog_params_factory: DialogParamsFactory,
                               td: Data, qtbot: QtBot):
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    note_3: Note = td.create_cloze_note()
    note_ids: list[NoteId] = [note_1.id, note_2.id, note_3.id]
    params: DialogParams = dialog_params_factory.create_from_note_ids(note_ids)
    adhoc_highlight_dialog_controller.show_dialog(params, lambda highlight_op_params: None)
    adhoc_highlight_dialog_view.show()
    qtbot.waitUntil(lambda: adhoc_highlight_dialog_view.isHidden(), timeout=sys.maxsize)
