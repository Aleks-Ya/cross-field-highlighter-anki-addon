from PyQtPath.path_chain_pyqt6 import path
from aqt import QCheckBox, QDialogButtonBox, QPushButton

from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModelListener
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_view import AdhocEraseDialogView
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams


class FakeCallback:
    def __init__(self):
        self.counter: int = 0

    def call(self):
        self.counter += 1


class FakeModelListener(AdhocEraseDialogModelListener):
    def __init__(self):
        self.history: list[object] = []

    def model_changed(self, source: object):
        self.history.append(source)


class FakeEraseControllerCallback:
    def __init__(self):
        self.history: list[EraseOpParams] = []

    def call(self, params: EraseOpParams):
        self.history.append(params)


def assert_view(view: AdhocEraseDialogView, window_title: str, check_box_texts: list[str], selected_fields: list[str]):
    # noinspection PyUnresolvedReferences
    assert view.windowTitle() == window_title, f"'{view.windowTitle()}' != '{window_title}'"
    assert_buttons(view)
    assert_destination_group_box(view, check_box_texts, selected_fields)


def assert_destination_group_box(view: AdhocEraseDialogView, check_box_texts: list[str], selected_fields: list[str]):
    fields_layout: FieldsLayout = path(view).child(FieldsLayout).get()
    assert path(fields_layout).label().get().text() == "Fields:"
    check_boxes: list[QCheckBox] = path(fields_layout).children(QCheckBox)
    texts: list[str] = [check_box.text() for check_box in check_boxes]
    assert texts == check_box_texts, f"check_box_texts: '{texts}' != '{check_box_texts}'"
    act_selected_fields: list[str] = [check_box.text() for check_box in check_boxes if check_box.isChecked()]
    assert act_selected_fields == selected_fields, f"selected_fields: '{act_selected_fields}' != '{selected_fields}'"


def assert_buttons(view: AdhocEraseDialogView):
    start_button: QPushButton = path(view).child(QDialogButtonBox).button(0).get()
    assert start_button.text() == "&Start"
    cancel_button: QPushButton = path(view).child(QDialogButtonBox).button(1).get()
    act_cancel_button_text: str = cancel_button.text()
    exp_cancel_button_text: str = "&Cancel"
    assert act_cancel_button_text == exp_cancel_button_text, f"'{act_cancel_button_text}' != '{exp_cancel_button_text}'"
    restore_defaults_button: QPushButton = path(view).child(QDialogButtonBox).button(2).get()
    assert restore_defaults_button.text() == "Restore Defaults"
