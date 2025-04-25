import sys

import pytest
from anki.collection import Collection
from anki.models import NoteType, NotetypeId
from anki.notes import Note, NoteId

from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from tests.data import Data
from tests.visual_qtbot import VisualQtBot


@pytest.mark.skip("For manual running")
def test_show_erase_dialog(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                           adhoc_erase_dialog_view: AdhocEraseDialogView,
                           dialog_params_factory: DialogParamsFactory,
                           td: Data, visual_qtbot: VisualQtBot):
    __show_dialog(adhoc_erase_dialog_controller, adhoc_erase_dialog_view, dialog_params_factory, visual_qtbot, td)


@pytest.mark.skip("For manual running")
def test_show_erase_dialog_many_wide_fields(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                                            adhoc_erase_dialog_view: AdhocEraseDialogView,
                                            dialog_params_factory: DialogParamsFactory,
                                            note_type_basic: NoteType, td: Data, visual_qtbot: VisualQtBot):
    td.add_fields_to_note_type(note_type_basic, 30, 50)
    __show_dialog(adhoc_erase_dialog_controller, adhoc_erase_dialog_view, dialog_params_factory, visual_qtbot, td)


@pytest.mark.skip("For manual running")
def test_show_erase_dialog_wide_note_type(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                                          adhoc_erase_dialog_view: AdhocEraseDialogView,
                                          dialog_params_factory: DialogParamsFactory, note_type_id_cloze: NotetypeId,
                                          col: Collection, td: Data, visual_qtbot: VisualQtBot):
    note_type_cloze: NoteType = col.models.get(note_type_id_cloze)
    note_type_cloze['name'] = "A really wide wide wide wide wide wide name"
    col.models.save(note_type_cloze)
    __show_dialog(adhoc_erase_dialog_controller, adhoc_erase_dialog_view, dialog_params_factory, visual_qtbot, td)


@pytest.mark.skip("For manual running")
def test_show_highlight_dialog_narrow_and_wide_fields(adhoc_erase_dialog_controller: AdhocEraseDialogController,
                                                      adhoc_erase_dialog_view: AdhocEraseDialogView,
                                                      dialog_params_factory: DialogParamsFactory,
                                                      note_type_id_cloze: NotetypeId,
                                                      note_type_basic: NoteType, note_type_cloze: NoteType,
                                                      col: Collection, td: Data, visual_qtbot: VisualQtBot):
    td.add_fields_to_note_type(note_type_basic, 5, 10)
    td.add_fields_to_note_type(note_type_cloze, 20, 50)
    __show_dialog(adhoc_erase_dialog_controller, adhoc_erase_dialog_view, dialog_params_factory, visual_qtbot, td)


def __show_dialog(controller: AdhocEraseDialogController, view: AdhocEraseDialogView,
                  dialog_params_factory: DialogParamsFactory, visual_qtbot: VisualQtBot, td: Data):
    note_1: Note = td.create_basic_note_1()
    note_2: Note = td.create_basic_note_2()
    note_3: Note = td.create_cloze_note()
    note_ids: list[NoteId] = [note_1.id, note_2.id, note_3.id]
    params: DialogParams = dialog_params_factory.create_from_note_ids(note_ids)
    controller.show_dialog(params, lambda erase_op_params: None)
    visual_qtbot.wait_until(lambda: view.isHidden(), timeout=sys.maxsize)
