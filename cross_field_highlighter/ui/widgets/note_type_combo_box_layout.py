import logging
from logging import Logger
from typing import Callable, Optional

from aqt.qt import QHBoxLayout, QLabel, Qt, QComboBox

from ...highlighter.note_type_details import NoteTypeDetails

log: Logger = logging.getLogger(__name__)


class NoteTypeComboBoxLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        label: QLabel = QLabel("Note type:")
        self.__combo_box: QComboBox = QComboBox(None)
        self.__combo_box.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.__callback: Optional[Callable[[NoteTypeDetails], None]] = None
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentIndexChanged.connect(self.__on_current_index_changed)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addWidget(label)
        self.addWidget(self.__combo_box, stretch=1)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def set_note_type_changed_callback(self, callback: Callable[[NoteTypeDetails], None]) -> None:
        self.__callback = callback

    def set_current_note_type(self, note_type_details: NoteTypeDetails) -> None:
        note_type_details_name: str = NoteTypeDetails.name(note_type_details)
        log.debug(f"Set current note type: {note_type_details_name}")
        self.__combo_box.blockSignals(True)
        current_item: NoteTypeDetails = self.__combo_box.currentData()
        if current_item != note_type_details:
            act_items: list[str] = []
            for i in range(self.__combo_box.count()):
                act_items.append(self.__combo_box.itemText(i))
            log.debug(f"Current combobox items: {act_items}")
            index: int = self.__combo_box.findData(note_type_details)
            log.debug(f"Found current note type index: {note_type_details_name}={index}")
            self.__combo_box.setCurrentIndex(index)
        self.__combo_box.blockSignals(False)

    def set_note_types(self, note_types: list[NoteTypeDetails]) -> None:
        log.debug(f"Set note types: {NoteTypeDetails.names(note_types)}")
        self.__combo_box.blockSignals(True)
        current_item: NoteTypeDetails = self.__combo_box.currentData()
        self.__combo_box.clear()
        for note_type_details in note_types:
            self.__combo_box.addItem(note_type_details.name, note_type_details)
        if current_item in note_types:
            index: int = self.__combo_box.findData(current_item)
            log.debug(f"Found current note type index: {NoteTypeDetails.name(current_item)}={index}")
            self.__combo_box.setCurrentIndex(index)
        self.__combo_box.blockSignals(False)

    def __on_current_index_changed(self, _: int) -> None:
        if self.__callback and self.__combo_box.currentData():
            self.__callback(self.__combo_box.currentData())

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
