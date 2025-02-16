from PyQtPath.path_chain_pyqt6 import path
from aqt import QCheckBox, QPushButton

from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout


def assert_fields_layout(fields_layout: FieldsLayout, exp_names: list[str], exp_marked_names: list[str],
                         exp_disabled_names: list[str]) -> None:
    assert_field_check_box_names(fields_layout, exp_names)
    assert_marked_destination_field_names(fields_layout, exp_marked_names)
    assert_disabled_destination_field_names(fields_layout, exp_disabled_names)


def assert_field_check_box_names(fields_layout: FieldsLayout, exp_names: list[str]) -> None:
    field_check_box_names: list[str] = [check_box.text() for check_box in get_field_checkboxes(fields_layout)]
    assert field_check_box_names == exp_names, f"field_check_box_names: '{field_check_box_names}' != '{exp_names}'"


def assert_marked_destination_field_names(fields_layout: FieldsLayout, exp_marked_names: list[str]) -> None:
    checked_destination_field_names: list[str] = [check_box.text() for check_box in get_field_checkboxes(fields_layout)
                                                  if check_box.isChecked()]
    assert checked_destination_field_names == exp_marked_names, \
        f"checked_destination_field_names: '{checked_destination_field_names}' != '{exp_marked_names}'"


def assert_disabled_destination_field_names(fields_layout: FieldsLayout, exp_disabled_names: list[str]) -> None:
    disabled_field_check_box_names: list[str] = [check_box.text() for check_box in get_field_checkboxes(fields_layout)
                                                 if not check_box.isEnabled()]
    assert disabled_field_check_box_names == exp_disabled_names, f"'{disabled_field_check_box_names}' != '{exp_disabled_names}'"


def get_field_checkboxes(fields_layout: FieldsLayout) -> list[QCheckBox]:
    return path(fields_layout).children(QCheckBox)


def get_select_all_button(fields_layout: FieldsLayout) -> QPushButton:
    return path(fields_layout).layout().button(0).get()


def get_select_none_button(fields_layout: FieldsLayout) -> QPushButton:
    return path(fields_layout).layout().button(1).get()
