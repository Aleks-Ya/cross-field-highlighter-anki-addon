from cross_field_highlighter.highlighter.formatter.formatter_facade import FormatterFacade
from cross_field_highlighter.highlighter.types import Text


def test_erase(formatter_facade: FormatterFacade):
    highlighted_text: Text = Text("I <b>see</b> an <i>ocean</i> on <b>the</b> <i>horizon</i>.")
    clean_text: Text = formatter_facade.erase(highlighted_text)
    assert clean_text == "I see an ocean on the horizon."
