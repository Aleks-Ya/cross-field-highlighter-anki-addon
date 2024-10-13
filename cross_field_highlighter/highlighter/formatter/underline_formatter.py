from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter


class UnderlineFormatter(TagFormatter):
    def __init__(self):
        super().__init__(f"""<u class="{TagFormatter._css_class}">""", "</u>")
