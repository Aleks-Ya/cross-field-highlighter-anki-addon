from pytestqt.qtbot import QtBot
from aqt import Qt, QWidget


class VisualQtBot:
    def __init__(self, qtbot: QtBot, wait_ms: int):
        self.__qtbot: QtBot = qtbot
        self.__wait_ms: int = wait_ms

    def addWidget(self, widget: QWidget):
        self.__qtbot.addWidget(widget)
        if self.__wait_ms > 0:
            widget.show()

    def keyClick(self, widget: QWidget, key: Qt.Key):
        self.__qtbot.keyClick(widget, key)
        self.__qtbot.wait(self.__wait_ms)

    def mouseClick(self, widget: QWidget, mouse_button: Qt.MouseButton):
        self.__qtbot.mouseClick(widget, mouse_button)
        self.__qtbot.wait(self.__wait_ms)

    def waitUntil(self, callback, timeout):
        self.__qtbot.waitUntil(callback, timeout=timeout)

    def waitExposed(self, widget: QWidget):
        self.__qtbot.waitExposed(widget)