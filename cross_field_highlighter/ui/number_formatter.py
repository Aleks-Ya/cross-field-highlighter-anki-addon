from typing import Optional


class NumberFormatter:
    @staticmethod
    def with_thousands_separator(number: Optional[int]) -> str:
        return f"{number:,}".replace(',', ' ') if number is not None else ''
