import logging
from logging import Logger

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter, NoteHighlightResult, \
    NoteEraseResult
from cross_field_highlighter.highlighter.types import FieldName, Word, Notes

log: Logger = logging.getLogger(__name__)


class NotesHighlighterResult:
    def __init__(self, notes: Notes, total_notes: int, modified_notes: int) -> None:
        self.notes = notes
        self.total_notes: int == total_notes
        self.modified_notes: int = modified_notes


class NotesHighlighter:
    def __init__(self, note_highlighter: NoteHighlighter):
        self.__note_highlighter: NoteHighlighter = note_highlighter

    def highlight(self, notes: Notes, source_field: FieldName, destination_field: FieldName,
                  stop_words: set[Word], highlight_format: HighlightFormat) -> NotesHighlighterResult:
        results: list[NoteHighlightResult] = [
            self.__note_highlighter.highlight(note, source_field, destination_field, stop_words, highlight_format)
            for note in notes]
        modified_notes: int = len([result for result in results if result.was_modified()])
        log.debug(
            f"Highlight notes: notes={len(notes)}, modified={modified_notes}, collocation_field={source_field}, "
            f"destination_field={destination_field}, stop_words={stop_words}, "
            f"highlight_format={highlight_format}")
        highlighted_notes: Notes = Notes([result.note for result in results])
        total_notes: int = len(highlighted_notes)
        modified_notes: int = len([result for result in results if result.was_modified()])
        return NotesHighlighterResult(highlighted_notes, total_notes, modified_notes)

    def erase(self, notes: Notes, field: FieldName) -> NotesHighlighterResult:
        results: list[NoteEraseResult] = [self.__note_highlighter.erase(note, field) for note in notes]
        erased_notes: Notes = Notes([result.note for result in results])
        total_notes: int = len(erased_notes)
        modified_notes: int = len([result for result in results if result.was_modified()])
        return NotesHighlighterResult(erased_notes, total_notes, modified_notes)
