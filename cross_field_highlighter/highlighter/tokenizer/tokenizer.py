from abc import ABC, abstractmethod
from enum import Enum

from ...highlighter.types import Text, Word


class TokenType(Enum):
    WORD = "WORD"
    PUNCTUATION = "PUNCTUATION"
    SPACE = "SPACE"
    TAG = "TAG"
    UNDEFINED = "UNDEFINED"


class Token:
    def __init__(self, word: Word, token_type: TokenType):
        self.word = word
        self.token_type = token_type

    def __eq__(self, other):
        return self.word == other.word and self.token_type == other.token_type

    def __repr__(self):
        return f"Token(word={self.word}, token_type={self.token_type})"

    def __hash__(self):
        return hash((self.word, self.token_type))


class Tokens(list):
    def delete_word(self, word: Word) -> None:
        self[:] = [token for token in self if token.word != word]

    def delete_by_token_type(self, token_type: TokenType) -> None:
        self[:] = [token for token in self if token.token_type != token_type]


class Tokenizer(ABC):

    @abstractmethod
    def tokenize(self, text: Text) -> Tokens:
        ...

    def tokenize_distinct(self, text: Text) -> Tokens:
        return Tokens(list(dict.fromkeys(self.tokenize(text))))
