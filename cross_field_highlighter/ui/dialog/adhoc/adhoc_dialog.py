import logging
from logging import Logger
from typing import Sequence

from anki.notes import NoteId
from aqt.qt import QDialog, QGridLayout, QVBoxLayout, QGroupBox, QLabel

log: Logger = logging.getLogger(__name__)


class AdhocDialog(QDialog):

    def __init__(self):
        super().__init__(parent=None)
        self.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('Highlight')

        source_group_layout: QVBoxLayout = QVBoxLayout()
        source_label: QLabel = QLabel("field type")
        source_group_layout.addWidget(source_label)
        source_group_box: QGroupBox = QGroupBox("Source")
        source_group_box.setLayout(source_group_layout)

        format_group_layout: QVBoxLayout = QVBoxLayout()
        format_label: QLabel = QLabel("format")
        format_group_layout.addWidget(format_label)
        formate_group_box: QGroupBox = QGroupBox("Format")
        formate_group_box.setLayout(format_group_layout)

        destination_label: QLabel = QLabel("destination")
        destination_group_layout: QVBoxLayout = QVBoxLayout()
        destination_group_layout.addWidget(destination_label)
        destination_group_box: QGroupBox = QGroupBox("Destination")
        destination_group_box.setLayout(destination_group_layout)

        layout: QGridLayout = QGridLayout(None)
        layout.addWidget(source_group_box, 0, 0)
        layout.addWidget(formate_group_box, 1, 0)
        layout.addWidget(destination_group_box, 2, 0)

        self.setLayout(layout)
        self.resize(300, 200)

    def show_dialog(self, note_ids: Sequence[NoteId]) -> None:
        # noinspection PyUnresolvedReferences
        self.show()
        self.adjustSize()
