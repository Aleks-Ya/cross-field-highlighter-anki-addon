import json
import os
from pathlib import Path
from typing import Any, Optional

from aqt.addons import AddonManager

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.types import NoteTypeName
from tests.data import DefaultStopWords


def test_empty_addon_dir(config_loader: ConfigLoader, module_dir: Path) -> None:
    os.remove(module_dir.joinpath("config.json"))
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {}


def test_default_values(config_loader: ConfigLoader, module_dir: Path):
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}}}


def test_actual_values_all(config_loader: ConfigLoader, module_dir: Path):
    meta_json_config: dict[str, Any] = {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}}}
    __write_meta_json_config(meta_json_config, module_dir)
    config: Config = config_loader.load_config()
    assert meta_json_config == config.get_as_dict()


def test_actual_values_partial(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({'Dialog': {'Adhoc': {'Highlight': {'Default Stop Words': 'the'}}}}, module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": "the",
                'States': {}},
            "Erase": {'States': {}}}}}


def test_delete_unused_properties(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}},
        'Unused Top': {'Property 1': 'Value 1'}}  # Will be deleted
        , module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}}}


def test_save_loaded_config(addon_manager: AddonManager, config_loader: ConfigLoader, module_name: str,
                            module_dir: Path):
    __write_meta_json_config({
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}}}, module_dir)
    config_origin: Optional[dict[str, Any]] = addon_manager.getConfig(module_name)
    assert config_origin == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}}}
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}}}
    config_saved: Optional[dict[str, Any]] = addon_manager.getConfig(module_name)
    assert config_saved == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}}}


def test_write_config(config_loader: ConfigLoader, module_dir: Path, basic_note_type_name: NoteTypeName) -> None:
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {}},
            "Erase": {'States': {}}}}}
    config.set_dialog_adhoc_highlight_states({'current_state': 'Basic',
                                              'states': [{'destination_fields': ['Back'],
                                                          'format': 'Bold',
                                                          'note_type': 'Basic',
                                                          'source_field': 'Front',
                                                          'stop_words': 'to '
                                                                        'the'}]})
    config.set_dialog_adhoc_erase_states(
        {'current_state': 'Basic', 'states': [{'fields': ['Back'], 'note_type': 'Basic'}]})
    config_loader.write_config(config)
    act_config: Config = config_loader.load_config()
    assert act_config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Default Stop Words": DefaultStopWords.in_config,
                'States': {'current_state': 'Basic',
                           'states': [{'destination_fields': ['Back'],
                                       'format': 'Bold',
                                       'note_type': 'Basic',
                                       'source_field': 'Front',
                                       'stop_words': 'to '
                                                     'the'}]}},
            "Erase": {'States': {'current_state': 'Basic', 'states': [{'fields': ['Back'], 'note_type': 'Basic'}]}}}}}


def __write_meta_json_config(meta_json_config, module_dir: Path) -> None:
    module_dir.mkdir(exist_ok=True)
    meta_json: Path = module_dir.joinpath("meta.json")
    meta_json_content: dict[str, dict[str, Any]] = {
        "config": meta_json_config
    }
    with open(meta_json, 'w') as fp:
        # noinspection PyTypeChecker
        json.dump(meta_json_content, fp, indent=2)
