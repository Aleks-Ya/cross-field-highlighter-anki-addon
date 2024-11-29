import sys

import pytest
from anki.models import NoteType
from anki.notes import Note, NoteId

from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import \
    AdhocHighlightDialogController
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from tests.data import Data
from tests.visual_qtbot import VisualQtBot


@pytest.mark.skip(reason="For manual running")
def test_show_highlight_dialog(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                               adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                               dialog_params_factory: DialogParamsFactory,
                               td: Data, visual_qtbot: VisualQtBot):
    __show_dialog(adhoc_highlight_dialog_controller, adhoc_highlight_dialog_view, dialog_params_factory, visual_qtbot,
                  td)


@pytest.mark.skip(reason="For manual running")
def test_show_highlight_dialog_many_wide_fields(adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                                                adhoc_highlight_dialog_view: AdhocHighlightDialogView,
                                                dialog_params_factory: DialogParamsFactory,
                                                basic_note_type: NoteType, td: Data, visual_qtbot: VisualQtBot):
    td.add_fields_to_note_type(basic_note_type, 30, 50)
    __show_dialog(adhoc_highlight_dialog_controller, adhoc_highlight_dialog_view, dialog_params_factory, visual_qtbot,
                  td)


def __show_dialog(controller: AdhocHighlightDialogController, view: AdhocHighlightDialogView,
                  dialog_params_factory: DialogParamsFactory, visual_qtbot: VisualQtBot, td: Data) -> None:
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    note_3: Note = td.create_cloze_note()
    note_ids: list[NoteId] = [note_1.id, note_2.id, note_3.id]
    params: DialogParams = dialog_params_factory.create_from_note_ids(note_ids)
    controller.show_dialog(params, lambda highlight_op_params: None)
    visual_qtbot.waitUntil(lambda: view.isHidden(), timeout=sys.maxsize)
