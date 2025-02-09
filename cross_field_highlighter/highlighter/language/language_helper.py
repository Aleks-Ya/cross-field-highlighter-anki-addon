from .language import Language


class LanguageHelper:
    @staticmethod
    def is_space_delimited_language(language: Language) -> bool:
        return language == Language.UNKNOWN
