from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter


class MarkFormatter(TagFormatter):
    def __init__(self):
        super().__init__(f"""<mark class="{TagFormatter._css_class}">""", "</mark>")
