import json
import os
from pathlib import Path
from typing import Any, Optional

from aqt.addons import AddonManager

from cross_field_highlighter.config.config import Config
from cross_field_highlighter.config.config_loader import ConfigLoader
from cross_field_highlighter.highlighter.formatter.highlight_format import HighlightFormatCode
from cross_field_highlighter.highlighter.types import FieldName, FieldNames


def test_empty_addon_dir(config_loader: ConfigLoader, module_dir: Path) -> None:
    os.remove(module_dir.joinpath("config.json"))
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {}


def test_default_values(config_loader: ConfigLoader, module_dir: Path):
    config: Config = config_loader.load_config()
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


def test_actual_values_all(config_loader: ConfigLoader, module_dir: Path):
    meta_json_config: dict[str, Any] = {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": "English",
                "Last Format": "BOLD",
                "Last Destination Field Names": ["Examples"]},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Names": ["Sentences"]}}}}
    __write_meta_json_config(meta_json_config, module_dir)
    config: Config = config_loader.load_config()
    assert meta_json_config == config.get_as_dict()


def test_actual_values_partial(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({'Dialog': {'Adhoc': {'Highlight': {'Last Format': 'ITALIC'}}}}, module_dir)
    config: Config = config_loader.load_config()
    assert config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": None,
                "Last Source Field Name": None,
                "Last Format": "ITALIC",
                "Last Destination Field Names": []},
            "Erase": {
                "Last Note Type": None,
                "Last Field Names": []}}}}


def test_delete_unused_properties(module_dir: Path, config_loader: ConfigLoader):
    __write_meta_json_config({
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": "English",
                "Last Format": "BOLD",
                "Last Destination Field Names": ["Examples"]},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Names": ["Sentences"]}}},
        'Unused Top': {'Property 1': 'Value 1'}}
        , module_dir)
    config: Config = config_loader.load_config()
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


def test_save_loaded_config(addon_manager: AddonManager, config_loader: ConfigLoader, module_name: str,
                            module_dir: Path):
    __write_meta_json_config({
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": "English",
                "Last Format": "BOLD",
                "Last Destination Field Names": ["Examples"]},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Names": ["Sentences"]}}}}, module_dir)
    config_origin: Optional[dict[str, Any]] = addon_manager.getConfig(module_name)
    assert config_origin == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": "English",
                "Last Format": "BOLD",
                "Last Destination Field Names": ["Examples"]},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Names": ["Sentences"]}}}}
    config: Config = config_loader.load_config()
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
    config_saved: Optional[dict[str, Any]] = addon_manager.getConfig(module_name)
    assert config_saved == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": "English",
                "Last Format": "BOLD",
                "Last Destination Field Names": ["Examples"]},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Names": ["Sentences"]}}}}


def test_write_config(config_loader: ConfigLoader, module_dir: Path) -> None:
    config: Config = config_loader.load_config()
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
    config.set_dialog_adhoc_highlight_last_note_type("Basic")
    config.set_dialog_adhoc_highlight_last_source_field_name(FieldName("English"))
    config.set_dialog_adhoc_highlight_last_format(HighlightFormatCode.BOLD)
    config.set_dialog_adhoc_highlight_last_destination_field_names(FieldNames([FieldName("Examples")]))
    config.set_dialog_adhoc_erase_last_note_type("Cloze")
    config.set_dialog_adhoc_erase_last_field_names(FieldNames([FieldName("Sentences")]))
    config_loader.write_config(config)
    act_config: Config = config_loader.load_config()
    assert act_config.get_as_dict() == {
        "Dialog": {"Adhoc": {
            "Highlight": {
                "Last Note Type": "Basic",
                "Last Source Field Name": "English",
                "Last Format": "BOLD",
                "Last Destination Field Names": ["Examples"]},
            "Erase": {
                "Last Note Type": "Cloze",
                "Last Field Names": ["Sentences"]}}}}


def __write_meta_json_config(meta_json_config, module_dir: Path) -> None:
    module_dir.mkdir(exist_ok=True)
    meta_json: Path = module_dir.joinpath("meta.json")
    meta_json_content: dict[str, dict[str, Any]] = {
        "config": meta_json_config
    }
    with open(meta_json, 'w') as fp:
        # noinspection PyTypeChecker
        json.dump(meta_json_content, fp, indent=2)
