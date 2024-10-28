from cross_field_highlighter.highlighter.tokenizer.stop_words_tokenizer import StopWordsTokenizer
from cross_field_highlighter.highlighter.types import Words, Word, Text


def test_str_to_stop_words(stop_words_tokenizer: StopWordsTokenizer):
    assert stop_words_tokenizer.tokenize(Text("a an the to a an")) == Words(
        [Word("a"), Word("an"), Word("the"), Word("to")])
    assert stop_words_tokenizer.tokenize(Text("")) == Words([])
