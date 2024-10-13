from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_listener import ConfigListener
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormat
from cross_field_highlighter.highlighter.types import FieldName
from tests.data import Data


class CountConfigListener(ConfigListener):
    def __init__(self):
        self.counter: int = 0

    def on_config_changed(self):
        self.counter += 1


def test_setters(td: Data):
    config: Config = td.read_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": None,
                "Last Source Field Name": None,
                "Last Format": None,
                "Last Destination Field Name": None},
            "Erase": {
                "Last Note Type": None,
                "Last Field Name": None}}}}
    config.set_dialog_adhoc_highlight_last_note_type("Basic")
    config.set_dialog_adhoc_highlight_last_source_field_name(FieldName("English"))
    config.set_dialog_adhoc_highlight_last_format(HighlightFormat.BOLD)
    config.set_dialog_adhoc_highlight_last_destination_field_name(FieldName("Examples"))
    config.set_dialog_adhoc_erase_last_note_type("Cloze")
    config.set_dialog_adhoc_erase_last_field_name(FieldName("Sentences"))
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": "English",
                "Last Format": "BOLD",
                "Last Destination Field Name": "Examples"},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Name": "Sentences"}}}}


def test_fire_config_changed(td: Data):
    config: Config = td.read_config()
    listener: CountConfigListener = CountConfigListener()
    config.add_listener(listener)
    assert listener.counter == 0
    config.fire_config_changed()
    assert listener.counter == 1
    config.fire_config_changed()
    assert listener.counter == 2
