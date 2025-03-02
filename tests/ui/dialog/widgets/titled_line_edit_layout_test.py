from PyQtPath.path_chain_pyqt6 import path
from aqt import QLabel, QLineEdit

from cross_field_highlighter.ui.widgets.titled_line_edit_layout import TitledLineEditLayout
from tests.data import DefaultConfig
from tests.visual_qtbot import VisualQtBot

exp_title: str = "Exclude words:"


def test_initial_state(visual_qtbot: VisualQtBot):
    exp_text: str = DefaultConfig.default_stop_words
    layout: TitledLineEditLayout = TitledLineEditLayout(exp_title, text=exp_text, clear_button_enabled=True)
    label: QLabel = path(layout).label().get()
    line_edit: QLineEdit = path(layout).child(QLineEdit).get()
    assert label.text() == exp_title
    assert line_edit.text() == exp_text


def test_set_text(visual_qtbot: VisualQtBot):
    callback: __FakeCallback = __FakeCallback()
    original_text: str = DefaultConfig.default_stop_words
    layout: TitledLineEditLayout = TitledLineEditLayout(exp_title, text=original_text, clear_button_enabled=True)
    layout.set_on_text_changed_callback(callback.call)
    line_edit: QLineEdit = path(layout).child(QLineEdit).get()
    assert line_edit.text() == original_text
    assert callback.text_changed_history == []
    exp_test: str = "the of"
    layout.set_text(exp_test)
    assert line_edit.text() == exp_test
    assert callback.text_changed_history == []


def test_set_on_text_changed_callback(visual_qtbot: VisualQtBot):
    callback: __FakeCallback = __FakeCallback()
    original_text: str = "a an "
    layout: TitledLineEditLayout = TitledLineEditLayout(exp_title, text=original_text, clear_button_enabled=True)
    layout.set_on_text_changed_callback(callback.call)
    line_edit: QLineEdit = path(layout).child(QLineEdit).get()
    assert line_edit.text() == original_text
    assert callback.text_changed_history == []
    exp_test: str = "the of"
    visual_qtbot.key_clicks(line_edit, exp_test)
    assert line_edit.text() == original_text + exp_test
    assert callback.text_changed_history == ['a an t', 'a an th', 'a an the', 'a an the ', 'a an the o', 'a an the of']


class __FakeCallback:
    def __init__(self):
        self.text_changed_history: list[str] = []

    def call(self, text: str):
        self.text_changed_history.append(text)
