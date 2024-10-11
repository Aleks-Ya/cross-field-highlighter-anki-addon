from typing import Callable

import pytest

from cross_field_highlighter.highlighter.tokenizer.regex_tokenizer import RegExTokenizer
from cross_field_highlighter.highlighter.types import Text, Word


@pytest.fixture
def tokenize(regex_tokenizer: RegExTokenizer) -> Callable[[str], list[Word]]:
    return lambda s: regex_tokenizer.tokenize(Text(s))


def test_tokenize_by_space(tokenize: Callable[[str], list[Word]]):
    assert tokenize('Hello, beautiful world!') == ['Hello,', 'beautiful', 'world!']


def test_tokenize_by_line_break(tokenize: Callable[[str], list[Word]]):
    assert tokenize('Hello, beautiful\nworld!') == ['Hello,', 'beautiful', 'world!']


def test_tokenize_tag(tokenize: Callable[[str], list[Word]]):
    assert tokenize('Hello, <b>beautiful</b>\nworld!') == ['Hello,', '<b>beautiful</b>', 'world!']
