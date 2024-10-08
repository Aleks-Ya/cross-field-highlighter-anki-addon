import logging
from logging import Logger

from PyQt6.QtWidgets import QGroupBox
from aqt.qt import QDialog, QGridLayout, QVBoxLayout, QGroupBox, QLabel

from cross_field_highlighter.ui.dialog.dialog_params import DialogParams
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout

log: Logger = logging.getLogger(__name__)


class AdhocDialog(QDialog):

    def __init__(self):
        super().__init__(parent=None)
        self.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('Highlight')

        source_group_box: QGroupBox = self.__create_source_widget()
        formate_group_box: QGroupBox = self.__create_format_widget()
        destination_group_box: QGroupBox = self.__create_destination_widget()

        layout: QGridLayout = QGridLayout(None)
        layout.addWidget(source_group_box, 0, 0)
        layout.addWidget(formate_group_box, 1, 0)
        layout.addWidget(destination_group_box, 2, 0)

        self.setLayout(layout)
        self.resize(300, 200)

    def __create_destination_widget(self):
        self.note_type_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Note Type")
        self.field_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Field")
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.note_type_combo_box)
        group_layout.addLayout(self.field_combo_box)
        group_box: QGroupBox = QGroupBox("Destination")
        group_box.setLayout(group_layout)
        return group_box

    def __create_format_widget(self):
        label: QLabel = QLabel("format")
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addWidget(label)
        group_box: QGroupBox = QGroupBox("Format")
        group_box.setLayout(group_layout)
        return group_box

    def __create_source_widget(self):
        label: QLabel = QLabel("field type")
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addWidget(label)
        group_box: QGroupBox = QGroupBox("Source")
        group_box.setLayout(group_layout)
        return group_box

    def show_dialog(self, params: DialogParams) -> None:
        note_type_names: list[str] = [note_type.get("name") for note_type in params.note_types.values()]
        self.note_type_combo_box.set_items(note_type_names)
        # noinspection PyUnresolvedReferences
        self.show()
        self.adjustSize()
