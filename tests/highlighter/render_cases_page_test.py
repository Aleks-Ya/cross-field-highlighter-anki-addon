from pathlib import Path

from mdutils import MdUtils

from tests.data import Data, Case


def test_create_cases_markdown(td: Data):
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
    text: list[str] = ["#", "Title", "Collocation", "Original text", "Expected text (space-delimited language)",
                       "Expected text (non-space-delimited language)"]
    cases: list[Case] = td.cases()
    for i, case in enumerate(cases):
        number: str = str(i + 1)
        title: str = case.name
        collocation: str = f"`{case.collocation}`" if case.collocation is not None and case.collocation != "" else ""
        original: str = f"`{case.original_text}`"
        expected_space: str = f"`{case.highlighted_text_space_delimited}`"
        expected_non_space: str = f"`{case.highlighted_text_non_space_delimited}`"
        text.extend([number, title, collocation, original, expected_space, expected_non_space])
    col_number: int = 6
    row_number: int = len(cases) + 1
    md.new_table(col_number, row_number, text=text)
    md.create_md_file()
