import logging
from logging import Logger
from typing import Callable

from aqt.qt import QHBoxLayout, Qt

from cross_field_highlighter.highlighter.types import NoteTypeDetails
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout

log: Logger = logging.getLogger(__name__)


class FieldSelectorLayout(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.__note_types: list[NoteTypeDetails] = []
        self.__note_type_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Note Type")
        self.__field_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Field")
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.addLayout(self.__note_type_combo_box)
        self.addLayout(self.__field_combo_box)
        self.__note_type_combo_box.add_current_index_changed_callback(self.__on_combobox_changed)

    def add_current_text_changed_callback(self, callback: Callable[[int], None]) -> None:
        # noinspection PyUnresolvedReferences
        self.__combo_box.currentIndexChanged.connect(callback)

    def set_note_types(self, note_types: list[NoteTypeDetails]):
        log.debug(f"Set note types: {note_types}")
        self.__note_types: list[NoteTypeDetails] = note_types
        note_type_names: list[str] = [note_type.name for note_type in note_types]
        self.__note_type_combo_box.set_items(note_type_names)

    def __on_combobox_changed(self, index: int):
        log.debug(f"On combobox changed: {index}")
        field_names: list[str] = self.__note_types[index].fields
        self.__field_combo_box.set_items(field_names)
