from anki.collection import Collection
from anki.notes import Note, NoteId

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.menu.dialog_params_factory import DialogParamsFactory
from tests.data import Data


def test_create_from_notes(dialog_params_factory: DialogParamsFactory, col: Collection, td: Data,
                           note_type_details_basic: NoteTypeDetails, note_type_details_cloze: NoteTypeDetails):
    basic_note_1: Note = td.create_basic_note_1()
    basic_note_2: Note = td.create_basic_note_2()
    cloze_note: Note = td.create_cloze_note()
    note_ids: list[NoteId] = [basic_note_1.id, basic_note_2.id, cloze_note.id]
    act_dialog_params: DialogParams = dialog_params_factory.create_from_note_ids(note_ids)
    selected_note_types: list[NoteTypeDetails] = [note_type_details_basic, note_type_details_cloze]
    exp_dialog_params: DialogParams = DialogParams(selected_note_types, len(note_ids))
    assert act_dialog_params == exp_dialog_params
