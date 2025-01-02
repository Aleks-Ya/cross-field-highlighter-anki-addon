from aqt import QWidget
from aqt.utils import MessageBox, show_warning

from cross_field_highlighter.ui.about.about_view import AboutView
from tests.visual_qtbot import VisualQtBot


def test_show_warning(about_view: AboutView, visual_qtbot: VisualQtBot):
    widget: QWidget = QWidget()
    visual_qtbot.add_widget(widget)
    message_box: MessageBox = show_warning("hello", parent=widget)
    assert message_box.text() == "hello"
