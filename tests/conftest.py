import pytest

from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter


@pytest.fixture
def start_with_text_highlighter() -> StartWithTextHighlighter:
    return StartWithTextHighlighter()
