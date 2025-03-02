import json
import os
from pathlib import Path
from typing import Optional

from aqt.addons import AddonManager

from cross_field_highlighter.config.config_loader import ConfigLoader, ConfigData
from cross_field_highlighter.highlighter.types import NoteTypeName
from tests.data import DefaultConfig, DefaultTags


def test_empty_addon_dir(config_loader: ConfigLoader, module_dir: Path) -> None:
    os.remove(module_dir.joinpath("config.json"))
    config_data: ConfigData = config_loader.load_config()
    assert config_data == {}


def test_default_values(config_loader: ConfigLoader, module_dir: Path):
    config_data: ConfigData = config_loader.load_config()
    assert config_data == DefaultConfig.loader


def test_read_modified_config_all(config_loader: ConfigLoader, module_dir: Path):
    meta_json_data: ConfigData = ConfigData({
        "Dialog": {"Adhoc": {
            "Highlight": {"Default Stop Words": "the", "Editor Shortcut": "Alt+H"},
            "Erase": {"Editor Shortcut": "Alt-E"}}},
        "Latest Modified Notes": {"Enabled": False, "Tag": "modified"}})
    __write_meta_json(meta_json_data, module_dir)
    act_config_data: ConfigData = config_loader.load_config()
    assert meta_json_data == act_config_data


def test_read_modified_config_partial(module_dir: Path, config_loader: ConfigLoader):
    updated_editor_shortcut: str = "Alt+H"
    updated_latest_modified_notes_enabled: bool = False
    __write_meta_json(ConfigData({
        "Dialog": {"Adhoc": {
            "Highlight": {"Editor Shortcut": updated_editor_shortcut},
            "Erase": {}}},
        "Latest Modified Notes": {"Enabled": updated_latest_modified_notes_enabled}}), module_dir)
    config_data: ConfigData = config_loader.load_config()
    assert config_data == {
        'Dialog': {'Adhoc': {
            'Highlight': {'Default Stop Words': DefaultConfig.default_stop_words, "Editor Shortcut": updated_editor_shortcut},
            "Erase": {**DefaultConfig.erase}}},
        "Latest Modified Notes": {"Enabled": updated_latest_modified_notes_enabled, "Tag": DefaultTags.latest_modified}}


def test_delete_unused_properties(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json(ConfigData({
        "Dialog": {"Adhoc": {
            "Highlight": {**DefaultConfig.highlight},
            "Erase": {**DefaultConfig.erase}}},
        'Unused Top': {'Property 1': 'Value 1'}}  # Will be deleted
    ), module_dir)
    config_data: ConfigData = config_loader.load_config()
    assert config_data == DefaultConfig.loader


def test_read_config_by_addon_manager(addon_manager: AddonManager, config_loader: ConfigLoader, module_name: str,
                                      module_dir: Path):
    exp_config: ConfigData = ConfigData({
        "Dialog": {"Adhoc": {
            "Highlight": {"Default Stop Words": "the", "Editor Shortcut": "Alt+H"},
            "Erase": {"Editor Shortcut": "Alt-E"}}},
        "Latest Modified Notes": {"Enabled": False, "Tag": "modified"}})
    __write_meta_json(exp_config, module_dir)
    config_origin: Optional[ConfigData] = addon_manager.getConfig(module_name)
    assert config_origin == exp_config
    config_data: ConfigData = config_loader.load_config()
    assert config_data == exp_config
    config_saved: Optional[ConfigData] = addon_manager.getConfig(module_name)
    assert config_saved == exp_config


def test_write_config(config_loader: ConfigLoader, module_dir: Path, note_type_name_basic: NoteTypeName) -> None:
    exp_config: ConfigData = ConfigData({
        "Dialog": {"Adhoc": {
            "Highlight": {"Default Stop Words": "the", "Editor Shortcut": "Alt+H"},
            "Erase": {"Editor Shortcut": "Alt-E"}}},
        "Latest Modified Notes": {"Enabled": False, "Tag": "modified"}})
    config_loader.write_config(exp_config)
    act_config_data: ConfigData = config_loader.load_config()
    assert act_config_data == exp_config


def __write_meta_json(meta_json_config_data: ConfigData, module_dir: Path) -> None:
    module_dir.mkdir(exist_ok=True)
    meta_json: Path = module_dir.joinpath("meta.json")
    meta_json_content: dict[str, ConfigData] = {
        "config": meta_json_config_data
    }
    with open(meta_json, 'w') as fp:
        # noinspection PyTypeChecker
        json.dump(meta_json_content, fp, indent=2)
