from re import Pattern, split, compile, escape
import string

from .tokenizer import TokenType
from ...highlighter.tokenizer.tokenizer import Tokenizer, Tokens, Token
from ...highlighter.types import Text, Word, Words


class RegExTokenizer(Tokenizer):
    def __init__(self):
        self.__punctuation_pattern: Pattern[str] = self.__create_punctuation_pattern()

    def tokenize(self, text: Text) -> Tokens:
        super().tokenize(text)
        tokens: Tokens = Tokens([Token(Word(text), TokenType.UNDEFINED)])
        by_tags: Tokens = self.__split_by_tags(tokens)
        by_space: Tokens = self.__split_by_spaces(by_tags)
        by_punctuation: Tokens = self.__split_by_punctuation(by_space)
        non_empty: Tokens = self.__remove_empty_tokens(by_punctuation)
        return non_empty

    @staticmethod
    def __create_punctuation_pattern() -> Pattern[str]:
        punctuation: str = string.punctuation.replace("<", "").replace(">", "")
        punctuation_escaped: str = escape(punctuation)
        punctuation_pattern: Pattern[str] = compile(f"([{punctuation_escaped}])")
        return punctuation_pattern

    @staticmethod
    def __remove_empty_tokens(tokens: Tokens) -> Tokens:
        return Tokens([token for token in tokens if token.word != ''])

    def __split_by_tags(self, tokens: Tokens) -> Tokens:
        pattern: Pattern[str] = compile("(<[^>]+>)")
        tokens_list: list[Tokens] = []
        for token in tokens:
            word_tokens: Tokens = Tokens([])
            words: Words = Words(split(pattern, token.word))
            for word in words:
                if pattern.match(word):
                    word_tokens.append(Token(Word(word), TokenType.TAG))
                else:
                    word_tokens.append(Token(Word(word), TokenType.UNDEFINED))
            tokens_list.append(word_tokens)
        return self.__flatten(tokens_list)

    def __split_by_spaces(self, tokens: Tokens) -> Tokens:
        tokens_list: list[Tokens] = []
        for token in tokens:
            if token.token_type == TokenType.UNDEFINED:
                words: Words = Words(split(r'(\s)', token.word))
                word_tokens: Tokens = Tokens([Token(word, TokenType.UNDEFINED) for word in words])
                tokens_list.append(word_tokens)
            else:
                tokens_list.append(Tokens([token]))
        return self.__flatten(tokens_list)

    def __split_by_punctuation(self, tokens: Tokens) -> Tokens:
        tokens_list: list[Tokens] = []
        for token in tokens:
            if token.token_type == TokenType.UNDEFINED:
                words: Words = Words(split(self.__punctuation_pattern, token.word))
                word_tokens: Tokens = Tokens([Token(word, TokenType.WORD) for word in words])
                tokens_list.append(word_tokens)
            else:
                tokens_list.append(Tokens([token]))
        return self.__flatten(tokens_list)

    @staticmethod
    def __flatten(tokens_list: list[Tokens]) -> Tokens:
        return Tokens([item for sublist in tokens_list for item in sublist])
