import logging
from logging import Logger
from typing import Callable, Optional

from aqt.qt import QHBoxLayout, QLabel, Qt, QComboBox

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails

log: Logger = logging.getLogger(__name__)


class NoteTypeComboBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        label: QLabel = QLabel("Note Type")
        self.__combo_box: QComboBox = QComboBox(None)
        self.__callback: Optional[Callable[[NoteTypeDetails], None]] = None
        self.__combo_box.currentIndexChanged.connect(self.__on_current_index_changed)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(label)
        self.addWidget(self.__combo_box)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def add_note_type_changed_callback(self, callback: Callable[[int], None]) -> None:
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentIndexChanged.connect(callback)

    def set_note_type_changed_callback(self, callback: Callable[[NoteTypeDetails], None]) -> None:
        self.__callback = callback

    def set_current_note_type(self, note_type_details: NoteTypeDetails) -> None:
        self.__combo_box.blockSignals(True)
        current_item: NoteTypeDetails = self.__combo_box.currentData()
        if current_item != note_type_details:
            index: int = self.__combo_box.findData(note_type_details)
            self.__combo_box.setCurrentIndex(index)
        self.__combo_box.blockSignals(False)

    def set_note_types(self, note_types: list[NoteTypeDetails]) -> None:
        current_item: NoteTypeDetails = self.__combo_box.currentData()
        self.__combo_box.clear()
        for note_type_details in note_types:
            self.__combo_box.addItem(note_type_details.name, note_type_details)
        if current_item in note_types:
            index: int = self.__combo_box.findData(current_item)
            self.__combo_box.setCurrentIndex(index)

    def __on_current_index_changed(self, _: int) -> None:
        if self.__callback:
            self.__callback(self.__combo_box.currentData())

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")