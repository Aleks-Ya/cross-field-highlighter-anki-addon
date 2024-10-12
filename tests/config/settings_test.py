from pathlib import Path

from cross_field_highlighter.config.settings import Settings


def test_to_string(settings: Settings, module_dir: Path):
    assert str(settings) == f"""Settings(module_dir={module_dir}, module_name=cross_field_highlighter)"""
