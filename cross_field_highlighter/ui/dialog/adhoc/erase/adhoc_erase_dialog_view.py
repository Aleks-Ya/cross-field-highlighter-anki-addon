import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout, QVBoxLayout, QDialogButtonBox, QPushButton

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import FieldNames, NoteTypeName
from cross_field_highlighter.ui.dialog.adhoc.fields_layout import FieldsLayout
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel, \
    AdhocEraseDialogModelListener
from cross_field_highlighter.ui.operation.erase_op_params import EraseOpParams
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogView(QDialog, AdhocEraseDialogModelListener):

    def __init__(self, adhoc_erase_dialog_model: AdhocEraseDialogModel):
        super().__init__(parent=None)
        self.__model: AdhocEraseDialogModel = adhoc_erase_dialog_model
        self.__model.add_listener(self)
        self.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('Erase')

        group_layout: QVBoxLayout = self.__field_widget()

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                                        QDialogButtonBox.StandardButton.Cancel |
                                                        QDialogButtonBox.StandardButton.RestoreDefaults)
        ok_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setText("Start")
        # noinspection PyUnresolvedReferences
        button_box.accepted.connect(self.__accept)
        # noinspection PyUnresolvedReferences
        button_box.rejected.connect(self.__reject)
        restore_defaults_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        # noinspection PyUnresolvedReferences
        restore_defaults_button.setToolTip('Reset settings in this dialog to defaults')
        # noinspection PyUnresolvedReferences
        restore_defaults_button.clicked.connect(self.__restore_defaults)

        layout: QGridLayout = QGridLayout(None)
        layout.addLayout(group_layout, 0, 0)
        layout.addWidget(button_box, 3, 0)

        self.setLayout(layout)
        self.resize(300, 200)

    def model_changed(self, source: object) -> None:
        if source != self:
            log.debug("Show dialog")
            note_type_names: list[str] = [note_type.name for note_type in self.__model.note_types]
            self.__note_type_combo_box.set_items(note_type_names)
            if self.__model.selected_note_type:
                self.__note_type_combo_box.set_current_text(self.__model.selected_note_type.name)
            if self.__model.selected_fields:
                self.__fields_vbox.select_fields(self.__model.selected_fields)
            # noinspection PyUnresolvedReferences
            self.show()
            self.adjustSize()

    def __on_combobox_changed(self, index: int):
        log.debug(f"On combobox changed: {index}")
        field_names: FieldNames = FieldNames(self.__model.note_types[index].fields)
        self.__fields_vbox.set_items(field_names)

    def __field_widget(self) -> QVBoxLayout:
        self.__note_type_combo_box: TitledComboBoxLayout = TitledComboBoxLayout("Note Type")
        self.__note_type_combo_box.add_current_index_changed_callback(self.__on_combobox_changed)
        self.__fields_vbox: FieldsLayout = FieldsLayout()
        group_layout: QVBoxLayout = QVBoxLayout()
        group_layout.addLayout(self.__note_type_combo_box)
        group_layout.addLayout(self.__fields_vbox)
        return group_layout

    def __accept(self) -> None:
        log.info("Starting")
        fields: FieldNames = self.__fields_vbox.get_selected_field_names()
        log.debug(f"Selected fields: {fields}")
        note_type_names: dict[NoteTypeName, NoteTypeDetails] = {note_type.name: note_type for note_type in
                                                                self.__model.note_types}
        note_type: NoteTypeDetails = note_type_names[NoteTypeName(self.__note_type_combo_box.get_current_text())]
        self.__model.selected_note_type = note_type
        self.__model.selected_fields = fields
        self.__model.fire_model_changed(self)
        self.hide()
        erase_op_params: EraseOpParams = EraseOpParams(note_type.note_type_id, self.parent(), fields)
        self.__model.run_op_callback(erase_op_params)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __reject(self) -> None:
        log.info("Cancelled")
        self.reject()

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")

    def __repr__(self):
        return self.__class__.__name__
