from cross_field_highlighter.highlighter.text.start_with_text_highlighter import StartWithTextHighlighter


def __tests(highlighter: StartWithTextHighlighter, collocation: str, original: str, highlighted: str):
    stop_words: set[str] = {"to", "a", "an"}
    assert highlighted == highlighter.highlight(collocation, original, stop_words)
    assert highlighted == highlighter.highlight(collocation, highlighted, stop_words)
    assert original == highlighter.erase(highlighted)


def test_normal(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'beautiful',
            'Hello, beautiful world!',
            'Hello, <b>beautiful</b> world!')


def test_highlight_several_words(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'beautiful',
            'Hello, beautiful world and beautiful day!',
            'Hello, <b>beautiful</b> world and <b>beautiful</b> day!')


def test_sub_word(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'hip',
            'Her children is at her hip.',
            'Her children is at her <b>hip</b>.')


def test_case_insensitive(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'beautiful',
            'Hello, Beautiful world!',
            'Hello, <b>Beautiful</b> world!')


def test_ing_base(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'abstain',
            'Abstaining from chocolate',
            '<b>Abstaining</b> from chocolate')


def test_ing_banging(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'overtake',
            'A driver was overtaking a slower vehicle.',
            'A driver was <b>overtaking</b> a slower vehicle.')


def test_ing_changing_short(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'lie',
            'A cat was lying on the floor.',
            'A cat was lying on the floor.')


def test_prefix_to(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'to overtake',
            'Driver was overtaking a slower vehicle.',
            'Driver was <b>overtaking</b> a slower vehicle.')


def test_prefix_a(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'a driver',
            'Driver was overtaking a slower vehicle.',
            '<b>Driver</b> was overtaking a slower vehicle.')


def test_prefix_an(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'an automobile',
            'Automobile was overtaking a slower vehicle.',
            '<b>Automobile</b> was overtaking a slower vehicle.')


def test_collocation(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'take forever',
            'Downloading a movie takes forever.',
            'Downloading a movie <b>takes forever</b>.')


def test_tag_li(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'lid',
            '<li>I opened the lid of the jar to get some jam.</li>',
            '<li>I opened the <b>lid</b> of the jar to get some jam.</li>')


def test_tag_div(start_with_text_highlighter: StartWithTextHighlighter):
    __tests(start_with_text_highlighter, 'ivy',
            '<li><div>There is ivy trailing all over the wall.</div></li>',
            '<li><div>There is <b>ivy</b> trailing all over the wall.</div></li>')
