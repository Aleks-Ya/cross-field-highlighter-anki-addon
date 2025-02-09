from pathlib import Path

from cross_field_highlighter.config.settings import Settings


def test_to_string(settings: Settings, module_dir: Path, base_dir: Path):
    exp_logs_folder: str = str(base_dir / "logs" / "addons" / "cross_field_highlighter")
    exp_user_folder: str = str(base_dir / "addons21" / "cross_field_highlighter" / "user_folder")
    assert str(settings) == (f"Settings(module_dir={module_dir}, module_name=cross_field_highlighter, "
                             f"logs_folder={exp_logs_folder}, user_folder={exp_user_folder}, version=0.1.0)")
