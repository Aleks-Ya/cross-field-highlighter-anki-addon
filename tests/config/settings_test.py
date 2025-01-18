from pathlib import Path

from cross_field_highlighter.config.settings import Settings


def test_to_string(settings: Settings, module_dir: Path, base_dir: Path):
    assert str(settings) == (f"Settings(module_dir={module_dir}, module_name=cross_field_highlighter, "
                             f"logs_folder={base_dir}/logs/addons/cross_field_highlighter, "
                             f"user_folder={base_dir}/addons21/cross_field_highlighter/user_folder, "
                             f"version=0.1.0)")
