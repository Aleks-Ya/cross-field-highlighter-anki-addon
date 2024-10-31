from typing import Any

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_listener import ConfigListener
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormatCode
from cross_field_highlighter.highlighter.types import FieldName, FieldNames, NoteTypeName
from tests.data import Data


class CountConfigListener(ConfigListener):
    def __init__(self):
        self.counter: int = 0

    def on_config_changed(self):
        super().on_config_changed()
        self.counter += 1


def test_setters(td: Data, basic_note_type_name: NoteTypeName):
    config: Config = td.read_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": None,
                "Last Source Field Name": {},
                "Last Format": None,
                "Last Stop Words": None,
                "Last Destination Field Names": None,
                "Default Stop Words": "a an to"},
            "Erase": {
                "Last Note Type": None,
                "Last Field Names": None}}}}

    assert config.get_dialog_adhoc_highlight_last_note_type_name() is None
    assert config.get_dialog_adhoc_highlight_last_source_field_name(basic_note_type_name) is None
    assert config.get_dialog_adhoc_highlight_last_format() is None
    assert config.get_dialog_adhoc_highlight_last_stop_words() is None
    assert config.get_dialog_adhoc_highlight_last_destination_field_names() is None
    assert config.get_dialog_adhoc_highlight_default_stop_words() == "a an to"
    assert config.get_dialog_adhoc_erase_last_note_type_name() is None
    assert config.get_dialog_adhoc_erase_last_field_names() is None

    config.set_dialog_adhoc_highlight_last_note_type_name(NoteTypeName("Basic"))
    config.set_dialog_adhoc_highlight_last_source_field_name(basic_note_type_name, FieldName("English"))
    config.set_dialog_adhoc_highlight_last_format(HighlightFormatCode.BOLD)
    config.set_dialog_adhoc_highlight_last_stop_words("a an the")
    config.set_dialog_adhoc_highlight_last_destination_field_names(FieldNames([FieldName("Examples")]))
    config.set_dialog_adhoc_highlight_default_stop_words("the")
    config.set_dialog_adhoc_erase_last_note_type_name(NoteTypeName("Cloze"))
    config.set_dialog_adhoc_erase_last_field_names(FieldNames([FieldName("Sentences")]))

    assert config.get_dialog_adhoc_highlight_last_note_type_name() == "Basic"
    assert config.get_dialog_adhoc_highlight_last_source_field_name(basic_note_type_name) == "English"
    assert config.get_dialog_adhoc_highlight_last_format() == HighlightFormatCode.BOLD
    assert config.get_dialog_adhoc_highlight_last_stop_words() == "a an the"
    assert config.get_dialog_adhoc_highlight_last_destination_field_names() == ["Examples"]
    assert config.get_dialog_adhoc_highlight_default_stop_words() == "the"
    assert config.get_dialog_adhoc_erase_last_note_type_name() == "Cloze"
    assert config.get_dialog_adhoc_erase_last_field_names() == ["Sentences"]

    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": {"Basic": "English"},
                "Last Format": "BOLD",
                "Last Stop Words": "a an the",
                "Last Destination Field Names": ["Examples"],
                "Default Stop Words": "the"},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Names": ["Sentences"]}}}}


def test_set_absent_field():
    config: Config = Config({})
    assert config.get_dialog_adhoc_highlight_last_note_type_name() is None
    config.set_dialog_adhoc_highlight_last_note_type_name(NoteTypeName("Basic"))
    assert config.get_dialog_adhoc_highlight_last_note_type_name() == "Basic"


def test_fire_config_changed(td: Data):
    config: Config = td.read_config()
    listener: CountConfigListener = CountConfigListener()
    config.add_listener(listener)
    assert listener.counter == 0
    config.fire_config_changed()
    assert listener.counter == 1
    config.fire_config_changed()
    assert listener.counter == 2


def test_join(td: Data):
    base: dict[str, Any] = {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": {"Basic": "Front"},
                "Last Format": "BOLD",
                "Last Stop Words": None,
                "Last Destination Field Names": None,
                "Default Stop Words": "a an to"},
            "Erase": {
                "Last Note Type": None,
                "Last Field Names": None}}}}

    actual: dict[str, Any] = {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Cloze",
                "Last Source Field Name": {"Cloze": "Text"},
                "Last Stop Words": None,
                "Last Destination Field Names": None,
                "Default Stop Words": "a an to"}},
            'Unused Top': {'Property 1': 'Value 1'}}}  # Unused property will be deleted

    joined: dict[str, Any] = Config.join(base, actual)
    assert joined == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Cloze",  # Overwrite value in base
                "Last Source Field Name": {"Basic": "Front", "Cloze": "Text"},  # Join dict field
                "Last Format": "BOLD",  # Get value from base
                "Last Stop Words": None,  # Same value in base and actual
                "Last Destination Field Names": None,
                "Default Stop Words": "a an to"},
            "Erase": {  # Get dict from base
                "Last Note Type": None,
                "Last Field Names": None}}}}
