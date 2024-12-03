from pytestqt.qtbot import QtBot
from aqt import Qt, QWidget


class VisualQtBot:
    def __init__(self, qtbot: QtBot, wait_ms: int):
        self.__qtbot: QtBot = qtbot
        self.__wait_ms: int = wait_ms

    def add_widget(self, widget: QWidget):
        self.__qtbot.addWidget(widget)
        if self.__wait_ms > 0:
            # noinspection PyUnresolvedReferences
            widget.show()

    def key_click(self, widget: QWidget, key: Qt.Key):
        self.__qtbot.keyClick(widget, key)
        self.__qtbot.wait(self.__wait_ms)

    def key_clicks(self, widget: QWidget, text: str):
        self.__qtbot.keyClicks(widget, text)
        self.__qtbot.wait(self.__wait_ms)

    def mouse_click(self, widget: QWidget, mouse_button: Qt.MouseButton):
        self.__qtbot.mouseClick(widget, mouse_button)
        self.__qtbot.wait(self.__wait_ms)

    def wait_until(self, callback, timeout):
        self.__qtbot.waitUntil(callback, timeout=timeout)

    def wait_exposed(self, widget: QWidget):
        self.__qtbot.waitExposed(widget)
