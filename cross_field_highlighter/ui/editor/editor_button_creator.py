import logging
from logging import Logger
from typing import Optional

from anki.models import NotetypeDict, NotetypeId
from anki.notes import Note
from aqt.editor import Editor

from ...config.settings import Settings
from ...highlighter.note.note_field_highlighter import NoteFieldHighlighter, NoteFieldHighlightResult, \
    NoteFieldEraseResult
from ...highlighter.note_type_details import NoteTypeDetails
from ...highlighter.note_type_details_factory import NoteTypeDetailsFactory
from ...ui.dialog.adhoc.erase.adhoc_erase_dialog_controller import AdhocEraseDialogController
from ...ui.dialog.adhoc.highlight.adhoc_highlight_dialog_controller import AdhocHighlightDialogController
from ...ui.dialog.dialog_params import DialogParams
from ...ui.operation.erase_op_params import EraseOpParams
from ...ui.operation.highlight_op_params import HighlightOpParams

log: Logger = logging.getLogger(__name__)


class EditorButtonCreator:
    def __init__(self,
                 adhoc_highlight_dialog_controller: AdhocHighlightDialogController,
                 adhoc_erase_dialog_controller: AdhocEraseDialogController,
                 note_type_details_factory: NoteTypeDetailsFactory,
                 note_field_highlighter: NoteFieldHighlighter,
                 settings: Settings) -> None:
        self.__highlight_controller: AdhocHighlightDialogController = adhoc_highlight_dialog_controller
        self.__erase_controller: AdhocEraseDialogController = adhoc_erase_dialog_controller
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.__note_field_highlighter: NoteFieldHighlighter = note_field_highlighter
        self.__settings: Settings = settings
        self.__editor: Optional[Editor] = None
        log.debug(f"{self.__class__.__name__} was instantiated")

    def create_highlight_button(self, editor: Editor) -> str:
        icon_path: str = self.__get_icon_path("highlight")
        log.debug(f"Highlight icon path: {icon_path}")
        button: str = editor.addButton(
            tip="Open Highlight dialog for current note...\n(Cross-Field Highlighter)",
            icon=icon_path,
            cmd="highlight_button_cmd",
            func=self.__on_highlight_button_click)
        return button

    def create_erase_button(self, editor: Editor) -> str:
        icon_path: str = self.__get_icon_path("rubber")
        log.debug(f"Erase icon path: {icon_path}")
        button: str = editor.addButton(
            tip="Open Erase dialog for current note...\n(Cross-Field Highlighter)",
            icon=icon_path,
            cmd="erase_button_cmd",
            func=self.__on_erase_button_click)
        return button

    def __on_highlight_button_click(self, editor: Editor) -> None:
        log.debug("On highlight click")
        note: Note = editor.note
        if note:
            self.__editor = editor
            dialog_params: DialogParams = self.__create_dialog_params(note)
            self.__highlight_controller.show_dialog(dialog_params, self.__on_highlight_op)

    def __on_erase_button_click(self, editor: Editor) -> None:
        log.debug("On erase click")
        note: Note = editor.note
        if note:
            self.__editor = editor
            dialog_params: DialogParams = self.__create_dialog_params(note)
            self.__erase_controller.show_dialog(dialog_params, self.__on_erase_op)

    def __create_dialog_params(self, note: Note):
        note_type_dict: NotetypeDict = note.note_type()
        note_type_id: NotetypeId = note_type_dict['id']
        note_type: NoteTypeDetails = self.__note_type_details_factory.by_note_type_id(note_type_id)
        return DialogParams([note_type])

    def __on_highlight_op(self, highlight_op_params: HighlightOpParams) -> None:
        for destination_field in highlight_op_params.destination_fields:
            result: NoteFieldHighlightResult = self.__note_field_highlighter.highlight(
                self.__editor.note, highlight_op_params.source_field, destination_field, highlight_op_params.stop_words,
                highlight_op_params.space_delimited_language, highlight_op_params.highlight_format)
            self.__editor.note[destination_field] = result.highlighted_text
            self.__editor.loadNoteKeepingFocus()

    def __on_erase_op(self, erase_op_params: EraseOpParams) -> None:
        for field in erase_op_params.fields:
            result: NoteFieldEraseResult = self.__note_field_highlighter.erase(self.__editor.note, field)
            self.__editor.note[field] = result.erased_text
            self.__editor.loadNoteKeepingFocus()

    def __get_icon_path(self, icon_name: str) -> str:
        return str(self.__settings.module_dir / "ui" / "editor" / f"{icon_name}.png")

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
