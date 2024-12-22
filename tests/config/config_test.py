from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_listener import ConfigListener
from cross_field_highlighter.config.config_loader import ConfigData
from cross_field_highlighter.highlighter.types import NoteTypeName
from tests.data import Data, DefaultConfig, DefaultTags


class CountConfigListener(ConfigListener):
    def __init__(self):
        self.counter: int = 0

    def on_config_changed(self):
        super().on_config_changed()
        self.counter += 1


def test_setters(td: Data, basic_note_type_name: NoteTypeName):
    config: Config = td.read_config()
    original_config: ConfigData = ConfigData({
        "Dialog": {"Adhoc": {
            "Highlight": {**DefaultConfig.highlight},
            "Erase": {**DefaultConfig.erase}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}})
    assert config.get_config_data() == original_config
    assert config.get_dialog_adhoc_highlight_default_stop_words() == DefaultConfig.stop_words
    assert config.get_dialog_adhoc_highlight_editor_shortcut() == DefaultConfig.highlight_shortcut
    assert config.get_dialog_adhoc_erase_editor_shortcut() == (
        None if DefaultConfig.erase_shortcut == "" else DefaultConfig.erase_shortcut)
    assert config.get_latest_modified_notes_enabled() == True
    assert config.get_latest_modified_notes_tag() == DefaultTags.latest_modified

    config.set_dialog_adhoc_highlight_default_stop_words("the")
    config.set_dialog_adhoc_highlight_editor_shortcut("Alt+H")
    config.set_dialog_adhoc_erase_editor_shortcut("Alt+E")
    config.set_latest_modified_notes_enabled(False)
    config.set_latest_modified_notes_tag("latest-notes")

    assert config.get_dialog_adhoc_highlight_default_stop_words() == "the"
    assert config.get_dialog_adhoc_highlight_editor_shortcut() == "Alt+H"
    assert config.get_dialog_adhoc_erase_editor_shortcut() == "Alt+E"
    assert config.get_latest_modified_notes_enabled() == False
    assert config.get_latest_modified_notes_tag() == "latest-notes"
    assert config.get_config_data() == {
        "Dialog": {"Adhoc": {
            "Highlight": {"Default Stop Words": "the", "Editor Shortcut": "Alt+H"},
            "Erase": {"Editor Shortcut": "Alt+E"}}},
        "Latest Modified Notes": {"Enabled": False, "Tag": "latest-notes"}}


def test_fire_config_changed(td: Data):
    config: Config = td.read_config()
    listener: CountConfigListener = CountConfigListener()
    config.add_listener(listener)
    assert listener.counter == 0
    config.fire_config_changed()
    assert listener.counter == 1
    config.fire_config_changed()
    assert listener.counter == 2
