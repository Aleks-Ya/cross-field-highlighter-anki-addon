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
            index: Optional[int] = None
            items: list[NoteTypeDetails] = []
            for i in range(self.__combo_box.count()):
                item_data: NoteTypeDetails = self.__combo_box.itemData(i)
                items.append(item_data)
                if item_data == note_type_details:
                    index: int = i
                    break
            if index is None:
                raise RuntimeError(f"Note type details '{note_type_details}' not found in combo box: {items}")
            log.debug(f"Found current note type index: {note_type_details_name}={index}")
            self.__combo_box.setCurrentIndex(index)
        self.__combo_box.blockSignals(False)

    def set_note_types(self, note_types: list[NoteTypeDetails]) -> None:
        log.debug(f"Set note types: {NoteTypeDetails.names(note_types)}")
        self.__combo_box.blockSignals(True)
        self.__combo_box.clear()
        for note_type_details in note_types:
            self.__combo_box.addItem(note_type_details.name, note_type_details)
        self.__combo_box.blockSignals(False)

    def __on_current_index_changed(self, _: int) -> None:
        if self.__callback and self.__combo_box.currentData():
            self.__callback(self.__combo_box.currentData())

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
