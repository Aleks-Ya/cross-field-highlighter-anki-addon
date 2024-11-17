import pytest
from PyQtPath.path_chain_pyqt6 import path
from aqt import QCheckBox

from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from tests.data import DefaultFields
from tests.visual_qtbot import VisualQtBot


@pytest.fixture
def fields_layout(visual_qtbot: VisualQtBot) -> FieldsLayout:
    return FieldsLayout()


def test_initial_state(fields_layout: FieldsLayout):
    __assert_fields_layout(fields_layout, exp_names=[], exp_marked_names=[], exp_disabled_names=[])


def test_set_items(fields_layout: FieldsLayout):
    __assert_fields_layout(fields_layout, exp_names=[], exp_marked_names=[], exp_disabled_names=[])
    fields_layout.set_items(FieldNames(DefaultFields.all_basic))
    __assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[], exp_disabled_names=[])


def test_set_disabled_fields(fields_layout: FieldsLayout):
    # Initial state
    fields_layout.set_items(FieldNames(DefaultFields.all_basic))
    __assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[], exp_disabled_names=[])
    # Disable two fields
    fields_layout.set_disabled_fields(FieldNames([DefaultFields.basic_front, DefaultFields.basic_extra]))
    __assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[],
                           exp_disabled_names=[DefaultFields.basic_front, DefaultFields.basic_extra])
    # Enable one field
    fields_layout.set_disabled_fields(FieldNames([DefaultFields.basic_front]))
    __assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[],
                           exp_disabled_names=[DefaultFields.basic_front])


def __assert_fields_layout(fields_layout: FieldsLayout, exp_names: list[str], exp_marked_names: list[str],
                           exp_disabled_names: list[str]) -> None:
    __assert_field_check_box_names(fields_layout, exp_names)
    __assert_marked_field_check_box_names(fields_layout, exp_marked_names)
    __assert_disabled_field_check_box_names(fields_layout, exp_disabled_names)


def __assert_field_check_box_names(fields_layout: FieldsLayout, exp_names: list[str]) -> None:
    field_check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    field_check_box_names: list[str] = [check_box.text() for check_box in field_check_boxes]
    assert field_check_box_names == exp_names


def __assert_marked_field_check_box_names(fields_layout: FieldsLayout, exp_marked_names: list[str]) -> None:
    field_check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    checked_field_check_box_names: list[str] = [check_box.text() for check_box in field_check_boxes if
                                                check_box.isChecked()]
    assert checked_field_check_box_names == exp_marked_names


def __assert_disabled_field_check_box_names(fields_layout: FieldsLayout, exp_disabled_names: list[str]) -> None:
    field_check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    disabled_field_check_box_names: list[str] = [check_box.text() for check_box in field_check_boxes if
                                                 not check_box.isEnabled()]
    assert disabled_field_check_box_names == exp_disabled_names
