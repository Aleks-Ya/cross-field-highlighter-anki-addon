from typing import Optional

import pytest
from aqt import QPushButton, Qt

from cross_field_highlighter.config.settings import Settings
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from tests.data import DefaultFields
from tests.ui.dialog.adhoc.fields_layout_asserts import assert_fields_layout, get_field_checkboxes, \
    get_select_all_button, get_select_none_button
from tests.visual_qtbot import VisualQtBot


@pytest.fixture
def fields_layout(settings: Settings, visual_qtbot: VisualQtBot) -> FieldsLayout:
    return FieldsLayout(settings)


def test_initial_state(fields_layout: FieldsLayout):
    assert_fields_layout(fields_layout, exp_names=[], exp_marked_names=[], exp_disabled_names=[])


def test_set_items(fields_layout: FieldsLayout):
    assert_fields_layout(fields_layout, exp_names=[], exp_marked_names=[], exp_disabled_names=[])
    fields_layout.set_items(FieldNames(DefaultFields.all_basic))
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[], exp_disabled_names=[])


def test_set_disabled_fields(fields_layout: FieldsLayout):
    # Initial state
    fields_layout.set_items(FieldNames(DefaultFields.all_basic))
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[], exp_disabled_names=[])
    # Disable two fields
    fields_layout.set_disabled_fields(FieldNames([DefaultFields.basic_front, DefaultFields.basic_extra]))
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[],
                         exp_disabled_names=[DefaultFields.basic_front, DefaultFields.basic_extra])
    # Enable one field
    fields_layout.set_disabled_fields(FieldNames([DefaultFields.basic_front]))
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[],
                         exp_disabled_names=[DefaultFields.basic_front])


def test_set_on_field_selected_callback(fields_layout: FieldsLayout, visual_qtbot: VisualQtBot):
    # Set callback
    callback: __FakeCallback = __FakeCallback()
    fields_layout.set_on_field_selected_callback(callback.call)
    assert callback.selected_field_names is None
    assert_fields_layout(fields_layout, exp_names=[], exp_marked_names=[], exp_disabled_names=[])
    # Select one field
    fields_layout.set_items(FieldNames(DefaultFields.all_basic))
    __mark_field_check_box(fields_layout, DefaultFields.basic_front)
    assert callback.selected_field_names == FieldNames([DefaultFields.basic_front])
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[DefaultFields.basic_front],
                         exp_disabled_names=[])
    # Select second field
    __mark_field_check_box(fields_layout, DefaultFields.basic_extra)
    fields_layout.set_disabled_fields(FieldNames([DefaultFields.basic_front]))
    assert callback.selected_field_names == FieldNames([DefaultFields.basic_front, DefaultFields.basic_extra])


def test_select_all_button(fields_layout: FieldsLayout, visual_qtbot: VisualQtBot):
    select_all_button: QPushButton = get_select_all_button(fields_layout)
    assert select_all_button.isEnabled() is True
    fields_layout.set_items(FieldNames(DefaultFields.all_basic))
    __mark_field_check_box(fields_layout, DefaultFields.basic_front)
    assert select_all_button.isEnabled() is True
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[DefaultFields.basic_front],
                         exp_disabled_names=[])
    visual_qtbot.mouse_click(select_all_button, Qt.MouseButton.LeftButton)
    assert select_all_button.isEnabled() is False
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=DefaultFields.all_basic,
                         exp_disabled_names=[])


def test_select_none_button(fields_layout: FieldsLayout, visual_qtbot: VisualQtBot):
    fields_layout.set_items(FieldNames(DefaultFields.all_basic))
    select_none_button: QPushButton = get_select_none_button(fields_layout)
    assert select_none_button.isEnabled() is False
    __mark_field_check_box(fields_layout, DefaultFields.basic_front)
    assert select_none_button.isEnabled() is True
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[DefaultFields.basic_front],
                         exp_disabled_names=[])
    visual_qtbot.mouse_click(select_none_button, Qt.MouseButton.LeftButton)
    assert select_none_button.isEnabled() is False
    assert_fields_layout(fields_layout, exp_names=DefaultFields.all_basic, exp_marked_names=[], exp_disabled_names=[])


class __FakeCallback:
    def __init__(self):
        self.selected_field_names: Optional[FieldNames] = None

    def call(self, selected_field_names: FieldNames):
        self.selected_field_names = selected_field_names


def __mark_field_check_box(fields_layout: FieldsLayout, field_name_to_mark: str) -> None:
    for check_box in get_field_checkboxes(fields_layout):
        if check_box.text() == field_name_to_mark:
            check_box.setChecked(True)
            break
