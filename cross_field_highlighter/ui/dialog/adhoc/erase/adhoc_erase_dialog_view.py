import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout, QDialogButtonBox, QPushButton

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.erase.fields_group_box import FieldsGroupBox
from cross_field_highlighter.ui.dialog.adhoc.erase.adhoc_erase_dialog_model import AdhocEraseDialogModel

log: Logger = logging.getLogger(__name__)


class AdhocEraseDialogView(QDialog):

    def __init__(self, adhoc_erase_dialog_model: AdhocEraseDialogModel,
                 note_type_details_factory: NoteTypeDetailsFactory):
        super().__init__(parent=None)
        self.__model: AdhocEraseDialogModel = adhoc_erase_dialog_model
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('Erase')

        self.__fields_group_layout: FieldsGroupBox = FieldsGroupBox(adhoc_erase_dialog_model)

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                                        QDialogButtonBox.StandardButton.Cancel |
                                                        QDialogButtonBox.StandardButton.RestoreDefaults)
        start_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
        start_button.setText("Start")
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
        layout.addWidget(self.__fields_group_layout, 0, 0)
        layout.addWidget(button_box, 3, 0)

        self.setLayout(layout)
        self.resize(300, 200)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_view(self) -> None:
        log.debug("Show view")
        # noinspection PyUnresolvedReferences
        self.show()
        self.adjustSize()
        self.__select_first_note_type()
        self.__model.fire_model_changed(self)

    def __select_first_note_type(self):
        if not self.__model.current_state or not self.__model.current_state.selected_note_type:
            if len(self.__model.note_types) > 0:
                selected_note_type_details: NoteTypeDetails = self.__model.note_types[0]
                self.__model.switch_state(selected_note_type_details)

    def __accept(self) -> None:
        log.info("Starting")
        self.hide()
        if self.__model.accept_callback:
            self.__model.accept_callback()
        log.debug(f"{self.__class__.__name__} was instantiated")

    def __reject(self) -> None:
        log.info("Cancelled")
        self.reject()
        if self.__model.reject_callback:
            self.__model.reject_callback()

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")
        self.__select_first_note_type()
        self.__model.current_state.selected_fields = FieldNames([])
        self.__model.fire_model_changed(None)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
