from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_listener import ConfigListener
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormatCode
from cross_field_highlighter.highlighter.types import FieldName, FieldNames
from tests.data import Data


class CountConfigListener(ConfigListener):
    def __init__(self):
        self.counter: int = 0

    def on_config_changed(self):
        super().on_config_changed()
        self.counter += 1


def test_setters(td: Data):
    config: Config = td.read_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": None,
                "Last Source Field Name": None,
                "Last Format": None,
                "Last Destination Field Names": []},
            "Erase": {
                "Last Note Type": None,
                "Last Field Names": []}}}}

    assert config.get_dialog_adhoc_highlight_last_note_type() is None
    assert config.get_dialog_adhoc_highlight_last_source_field_name() is None
    assert config.get_dialog_adhoc_highlight_last_format() is None
    assert config.get_dialog_adhoc_highlight_last_destination_field_names() == []
    assert config.get_dialog_adhoc_erase_last_note_type() is None
    assert config.get_dialog_adhoc_erase_last_field_names() == []

    config.set_dialog_adhoc_highlight_last_note_type("Basic")
    config.set_dialog_adhoc_highlight_last_source_field_name(FieldName("English"))
    config.set_dialog_adhoc_highlight_last_format(HighlightFormatCode.BOLD)
    config.set_dialog_adhoc_highlight_last_destination_field_names(FieldNames([FieldName("Examples")]))
    config.set_dialog_adhoc_erase_last_note_type("Cloze")
    config.set_dialog_adhoc_erase_last_field_names(FieldNames([FieldName("Sentences")]))

    assert config.get_dialog_adhoc_highlight_last_note_type() == "Basic"
    assert config.get_dialog_adhoc_highlight_last_source_field_name() == "English"
    assert config.get_dialog_adhoc_highlight_last_format() == HighlightFormatCode.BOLD
    assert config.get_dialog_adhoc_highlight_last_destination_field_names() == ["Examples"]
    assert config.get_dialog_adhoc_erase_last_note_type() == "Cloze"
    assert config.get_dialog_adhoc_erase_last_field_names() == ["Sentences"]

    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": "English",
                "Last Format": "BOLD",
                "Last Destination Field Names": ["Examples"]},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Names": ["Sentences"]}}}}


def test_set_absent_field():
    config: Config = Config({})
    assert config.get_dialog_adhoc_highlight_last_note_type() is None
    config.set_dialog_adhoc_highlight_last_note_type("Basic")
    assert config.get_dialog_adhoc_highlight_last_note_type() == "Basic"


def test_fire_config_changed(td: Data):
    config: Config = td.read_config()
    listener: CountConfigListener = CountConfigListener()
    config.add_listener(listener)
    assert listener.counter == 0
    config.fire_config_changed()
    assert listener.counter == 1
    config.fire_config_changed()
    assert listener.counter == 2
