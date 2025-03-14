import logging
from logging import Logger

from anki.notes import Note

from ...config.config import Config
from ...highlighter.formatter.highlight_format import HighlightFormat
from ...highlighter.note.field_highlighter import FieldHighlighter, FieldHighlightResult, \
    NoteFieldEraseResult
from ...highlighter.types import FieldName, Notes, Text, FieldNames

log: Logger = logging.getLogger(__name__)


class NotesHighlighterResult:
    def __init__(self, notes: Notes, total_notes: int, total_fields: int, modified_notes: int,
                 modified_fields: int) -> None:
        self.notes = notes
        self.total_notes: int = total_notes
        self.total_fields: int = total_fields
        self.modified_notes: int = modified_notes
        self.modified_fields: int = modified_fields


class NotesHighlighter:
    def __init__(self, field_highlighter: FieldHighlighter, config: Config):
        self.__field_highlighter: FieldHighlighter = field_highlighter
        self.__latest_modified_notes_enabled: bool = config.get_latest_modified_notes_enabled()
        self.__latest_modified_notes_tag: str = config.get_latest_modified_notes_tag()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def highlight(self, notes: Notes, source_field: FieldName, destination_fields: FieldNames,
                  stop_words: Text, highlight_format: HighlightFormat) -> NotesHighlighterResult:
        modified_notes: int = 0
        modified_fields: int = 0
        updated_notes: Notes = Notes([])
        for note in notes:
            updated_note: Note = note
            note_was_modified: bool = False
            for destination_field in destination_fields:
                result: FieldHighlightResult = self.__field_highlighter.highlight(
                    updated_note, source_field, destination_field, stop_words, highlight_format)
                if result.was_modified():
                    self.__add_latest_modified_tag(updated_note)
                    note_was_modified = True
                    modified_fields += 1
                updated_note = result.note
            updated_notes.append(updated_note)
            if note_was_modified:
                modified_notes += 1
        total_fields: int = len(destination_fields) * len(notes)
        return NotesHighlighterResult(updated_notes, len(notes), total_fields, modified_notes, modified_fields)

    def erase(self, notes: Notes, fields: FieldNames) -> NotesHighlighterResult:
        modified_notes: int = 0
        modified_fields: int = 0
        updated_notes: Notes = Notes([])
        for note in notes:
            updated_note: Note = note
            note_was_modified: bool = False
            for field in fields:
                result: NoteFieldEraseResult = self.__field_highlighter.erase(updated_note, field)
                if result.was_modified():
                    self.__add_latest_modified_tag(updated_note)
                    note_was_modified = True
                    modified_fields += 1
                updated_note = result.note
            updated_notes.append(updated_note)
            if note_was_modified:
                modified_notes += 1
        total_fields: int = len(fields) * len(notes)
        return NotesHighlighterResult(updated_notes, len(notes), total_fields, modified_notes, modified_fields)

    def __add_latest_modified_tag(self, note: Note) -> None:
        if self.__latest_modified_notes_enabled:
            note.tags.append(self.__latest_modified_notes_tag)

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
