from typing import Any

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_listener import ConfigListener
from cross_field_highlighter.highlighter.types import NoteTypeName
from tests.data import Data, DefaultStopWords


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
                **DefaultStopWords.config,
                'States': {}},
            "Erase": {'States': {}}}}}

    assert config.get_dialog_adhoc_highlight_states() == {}
    assert config.get_dialog_adhoc_highlight_default_stop_words() == DefaultStopWords.in_config
    assert config.get_dialog_adhoc_erase_states() == {}

    assert config.get_dialog_adhoc_highlight_states() == {}
    config.set_dialog_adhoc_highlight_default_stop_words("the")
    config.set_dialog_adhoc_erase_states(
        {'current_state': 'Basic', 'states': [{'fields': ['Back'], 'note_type': 'Basic'}]})

    assert config.get_dialog_adhoc_highlight_states() == {}
    assert config.get_dialog_adhoc_highlight_default_stop_words() == "the"
    assert config.get_dialog_adhoc_erase_states() == {'current_state': 'Basic',
                                                      'states': [{'fields': ['Back'], 'note_type': 'Basic'}]}

    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": "the",
                'States': {}},
            "Erase": {'States': {'current_state': 'Basic', 'states': [{'fields': ['Back'], 'note_type': 'Basic'}]}}}}}


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
                **DefaultStopWords.config,
                'States': {}},
            "Erase": {'States': {}}}}}

    actual: dict[str, Any] = {
        "Dialog": {"Adhoc": {
            "Highlight": {
                **DefaultStopWords.config,
                'States': {}}},
            'Unused Top': {'Property 1': 'Value 1'}}}  # Unused property will be deleted

    joined: dict[str, Any] = Config.join(base, actual)
    assert joined == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                **DefaultStopWords.config,
                'States': {}},
            "Erase": {  # Get dict from base
                'States': {}}}}}
