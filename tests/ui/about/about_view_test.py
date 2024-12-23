from aqt import QDialogButtonBox, QPushButton, Qt
from PyQtPath.path_chain_pyqt6 import path

from cross_field_highlighter.ui.about.about_view import AboutView
from tests.visual_qtbot import VisualQtBot


def test_show_view(about_view: AboutView, visual_qtbot: VisualQtBot):
    assert not about_view.isVisible()
    # noinspection PyUnresolvedReferences
    about_view.show_view()
    visual_qtbot.wait_exposed(about_view)
    assert about_view.isVisible()

    # noinspection PyUnresolvedReferences
    assert about_view.windowTitle() == "About"

    button_box: QDialogButtonBox = path(about_view).child(QDialogButtonBox).get()
    ok_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
    visual_qtbot.mouse_click(ok_button, Qt.MouseButton.LeftButton)
    assert not about_view.isVisible()


def test_repr(about_view: AboutView):
    assert repr(about_view) == "AboutView"
