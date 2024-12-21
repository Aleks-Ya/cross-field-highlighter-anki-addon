import logging
from logging import Logger

from .adhoc_highlight_dialog_model import AdhocHighlightDialogModel
from .....highlighter.formatter.highlight_format import HighlightFormatCode, HighlightFormat
from .....highlighter.note_type_details import NoteTypeDetails
from .....highlighter.types import NoteTypeName, FieldNames, Text, FieldName

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogModelSerDe:
    __source_field: str = "source_field"
    __space_delimited_language: str = "space_delimited_language"
    __format: str = "format"
    __stop_words: str = "stop_words"
    __destination_fields: str = "destination_fields"
    __current_state: str = "current_state"
    __states: str = "states"
    __note_type: str = "note_type"

    def __init__(self):
        log.debug(f"{self.__class__.__name__} was instantiated")

    def serialize_states(self, model: AdhocHighlightDialogModel) -> dict[str, any]:
        states: list[dict[str, any]] = [{
            "note_type": state.get_selected_note_type().name,
            self.__source_field: state.get_selected_source_field(),
            self.__space_delimited_language: state.get_space_delimited_language(),
            self.__format: state.get_selected_format().code.value,
            self.__stop_words: state.get_selected_stop_words(),
            self.__destination_fields: state.get_selected_destination_fields()
        } for state in model.get_states()]
        result: dict[str, any] = {
            "current_state": model.get_current_state().get_selected_note_type().name,
            "states": states}
        return result

    def deserialize_states(self, model: AdhocHighlightDialogModel, json: dict[str, any]) -> None:
        note_type_dict: [NoteTypeName, NoteTypeDetails] = {note_type.name: note_type for note_type in
                                                           model.get_note_types()}
        self.__read_states(json, model, note_type_dict)
        self.__read_current_state(json, model, note_type_dict)

    def __read_current_state(self, json, model, note_type_dict):
        if json and self.__current_state in json:
            current_state_name: NoteTypeName = json[self.__current_state]
            if current_state_name in note_type_dict:
                current_note_type_details: NoteTypeDetails = note_type_dict[current_state_name]
                model.switch_state(current_note_type_details)

    def __read_states(self, json, model, note_type_dict):
        highlight_formats: [HighlightFormatCode, HighlightFormat] = {highlight_format.code: highlight_format for
                                                                     highlight_format in model.get_formats()}
        if json and self.__states in json:
            for state_obj in json[self.__states]:
                saved_note_type_name: NoteTypeName = state_obj[self.__note_type]
                if saved_note_type_name in note_type_dict:
                    saved_note_type_details: NoteTypeDetails = note_type_dict[saved_note_type_name]
                    model.switch_state(saved_note_type_details)
                    self.__read_source_field(model, state_obj)
                    self.__read_space_delimited_language(model, state_obj)
                    self.__read_format(model, state_obj, highlight_formats)
                    self.__read_stop_words(model, state_obj)
                    self.__read_destination_fields(model, state_obj)

    def __read_source_field(self, model: AdhocHighlightDialogModel, state_obj: dict):
        if self.__source_field in state_obj:
            saved_source_field: FieldName = FieldName(state_obj[self.__source_field])
            model.get_current_state().select_source_field(saved_source_field)

    def __read_stop_words(self, model: AdhocHighlightDialogModel, state_obj: dict):
        if self.__stop_words in state_obj:
            saved_stop_words: Text = Text(state_obj[self.__stop_words])
            model.get_current_state().set_stop_words(saved_stop_words)

    def __read_space_delimited_language(self, model: AdhocHighlightDialogModel, state_obj: dict):
        if self.__space_delimited_language in state_obj:
            space_delimited_language: bool = state_obj[self.__space_delimited_language]
            model.get_current_state().set_space_delimited_language(space_delimited_language)

    def __read_format(self, model: AdhocHighlightDialogModel, state_obj: dict,
                      highlight_formats: [HighlightFormatCode, HighlightFormat]):
        if self.__format in state_obj:
            saved_highlight_format_code: HighlightFormatCode = HighlightFormatCode(state_obj[self.__format])
            saved_highlight_format: HighlightFormat = highlight_formats[saved_highlight_format_code]
            model.get_current_state().select_format(saved_highlight_format)

    def __read_destination_fields(self, model: AdhocHighlightDialogModel, state_obj: dict):
        if self.__destination_fields in state_obj:
            saved_destination_fields: FieldNames = FieldNames(state_obj[self.__destination_fields])
            model.get_current_state().select_destination_fields(saved_destination_fields)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
