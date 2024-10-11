from cross_field_highlighter.highlighter.formatter.tag_formatter import TagFormatter


class ItalicFormatter(TagFormatter):
    def __init__(self):
        super().__init__("<i>", "</i>")
