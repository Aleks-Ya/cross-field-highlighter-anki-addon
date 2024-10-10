import logging
from logging import Logger

from anki.notes import Note

from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.note.note_highlighter import NoteHighlighter, NoteHighlighterResult
from cross_field_highlighter.highlighter.types import FieldName, Word

log: Logger = logging.getLogger(__name__)


class NotesHighlighter:
    def __init__(self, note_highlighter: NoteHighlighter):
        self.__note_highlighter: NoteHighlighter = note_highlighter

    def highlight(self, notes: list[Note], collocation_field: FieldName, destination_field: FieldName,
                  stop_words: set[Word], highlight_format: HighlightFormat) -> list[Note]:
        results: list[NoteHighlighterResult] = [
            self.__note_highlighter.highlight(note, collocation_field, destination_field, stop_words, highlight_format)
            for note in notes]
        modified_notes: int = len([result for result in results if result.was_modified()])
        log.debug(
            f"Highlight notes: notes={len(notes)}, modified={modified_notes}, collocation_field={collocation_field}, "
            f"destination_field={destination_field}, stop_words={stop_words}, "
            f"highlight_format={highlight_format}")
        highlighted_notes: list[Note] = [result.note for result in results]
        return highlighted_notes

    def erase(self, notes: list[Note], destination_field: FieldName) -> list[Note]:
        return [self.__note_highlighter.erase(note, destination_field) for note in notes]
