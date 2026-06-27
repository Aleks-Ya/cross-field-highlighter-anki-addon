#!/usr/bin/env python3
from pathlib import Path

import yaml
from mdutils import MdUtils


def main():
    yaml_file: Path = Path(__file__).parent.parent / "cases.yaml"
    cases: list[dict] = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))

    file: Path = Path(__file__).parent.parent.parent / "docs" / "cases.md"
    md: MdUtils = MdUtils(file_name=str(file), title='Test cases for Cross-Field Highlighter (CFH)')
    md.new_line('CFH has highlighting and erasing algorithms which are verified by auto-tests.')
    md.new_line('Test cases listed in the table below are used to verify these algorithms.')
    md.new_paragraph('Auto-tests perform for each test case:')
    md.new_list(['Highlight "Collocation" in "Original text" using Bold format',
                 'Verify that the highlighted text is the same as in "Expected text"',
                 'Erase the highlighted text',
                 'Verify that the erased text is the same as "Original text"'], marked_with="1")
    md.new_line()
    text: list[str] = ["#", "Title", "Collocation", "Original text", "Highlighted text"]
    for i, case in enumerate(cases):
        case_number: int = i + 1
        number: str = f"[{case_number}](#case-{case_number})"
        title: str = case["name"]
        collocation: str = f"`{case['collocation']}`" if case["collocation"] else ""
        original: str = f"`{case['original_text']}`"
        expected: str = f"`{case['highlighted_text']}`"
        text.extend([number, title, collocation, original, expected])
    col_number: int = 5
    row_number: int = len(cases) + 1
    md.new_table(col_number, row_number, text=text)
    md.create_md_file()


if __name__ == "__main__":
    main()
