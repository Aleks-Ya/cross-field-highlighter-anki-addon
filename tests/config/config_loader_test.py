import json
import os
from pathlib import Path
from typing import Optional

from aqt.addons import AddonManager

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.types import NoteTypeName
from tests.data import DefaultConfig, DefaultTags


def test_empty_addon_dir(config_loader: ConfigLoader, module_dir: Path) -> None:
    os.remove(module_dir.joinpath("config.json"))
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {}


def test_default_values(config_loader: ConfigLoader, module_dir: Path):
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {**DefaultConfig.highlight},
            "Erase": {**DefaultConfig.erase}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}


def test_actual_values_all(config_loader: ConfigLoader, module_dir: Path):
    exp_meta_json_config: dict[str, any] = {
        "Dialog": {"Adhoc": {
            "Highlight": {**DefaultConfig.highlight},
            "Erase": {**DefaultConfig.erase}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    __write_meta_json_config(exp_meta_json_config, module_dir)
    config: Config = config_loader.load_config()
    assert exp_meta_json_config == config.get_as_dict()


def test_actual_values_partial(module_dir: Path, config_loader: ConfigLoader):
    exp_config: dict[str, any] = {
        'Dialog': {'Adhoc': {
            'Highlight': {'Default Stop Words': 'the', "Editor Shortcut": DefaultConfig.highlight_shortcut},
            "Erase": {**DefaultConfig.erase}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    __write_meta_json_config(exp_config, module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == exp_config


def test_delete_unused_properties(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({
        "Dialog": {"Adhoc": {
            "Highlight": {**DefaultConfig.highlight},
            "Erase": {**DefaultConfig.erase}}},
        'Unused Top': {'Property 1': 'Value 1'}}  # Will be deleted
        , module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {**DefaultConfig.highlight},
            "Erase": {**DefaultConfig.erase}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}


def test_save_loaded_config(addon_manager: AddonManager, config_loader: ConfigLoader, module_name: str,
                            module_dir: Path):
    exp_config: dict[str, any] = {
        "Dialog": {"Adhoc": {
            "Highlight": {**DefaultConfig.highlight},
            "Erase": {**DefaultConfig.erase}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    __write_meta_json_config(exp_config, module_dir)
    config_origin: Optional[dict[str, any]] = addon_manager.getConfig(module_name)
    assert config_origin == exp_config
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == exp_config
    config_saved: Optional[dict[str, any]] = addon_manager.getConfig(module_name)
    assert config_saved == exp_config


def test_write_config(config_loader: ConfigLoader, module_dir: Path, basic_note_type_name: NoteTypeName) -> None:
    config: Config = config_loader.load_config()
    exp_config: dict[str, any] = {
        "Dialog": {"Adhoc": {
            "Highlight": {**DefaultConfig.highlight},
            "Erase": {**DefaultConfig.erase}}},
        "Latest Modified Notes": {"Enabled": True, "Tag": DefaultTags.latest_modified}}
    assert config.get_as_dict() == exp_config
    config_loader.write_config(config)
    act_config: Config = config_loader.load_config()
    assert act_config.get_as_dict() == exp_config


def __write_meta_json_config(meta_json_config, module_dir: Path) -> None:
    module_dir.mkdir(exist_ok=True)
    meta_json: Path = module_dir.joinpath("meta.json")
    meta_json_content: dict[str, dict[str, any]] = {
        "config": meta_json_config
    }
    with open(meta_json, 'w') as fp:
        # noinspection PyTypeChecker
        json.dump(meta_json_content, fp, indent=2)
