from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter


class BoldFormatter(TagFormatter):
    def __init__(self):
        super().__init__(f"""<b class="{TagFormatter._css_class}">""", "</b>")
