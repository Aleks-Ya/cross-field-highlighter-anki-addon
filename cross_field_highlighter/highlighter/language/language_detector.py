from abc import ABC, abstractmethod

from .language import Language
from ...highlighter.types import Text


class LanguageDetector(ABC):
    @abstractmethod
    def detect_language(self, text: Text) -> Language:
        ...
