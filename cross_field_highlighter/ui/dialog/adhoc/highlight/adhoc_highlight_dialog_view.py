import logging
from logging import Logger

from aqt.qt import QDialog, QGridLayout, QDialogButtonBox, QPushButton, Qt

from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.note_type_details_factory import NoteTypeDetailsFactory
from cross_field_highlighter.highlighter.types import FieldNames
from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_model import \
    AdhocHighlightDialogModel
from cross_field_highlighter.ui.dialog.adhoc.highlight.destination_group_box import DestinationGroupBox
from cross_field_highlighter.ui.dialog.adhoc.highlight.format_group_box import FormatGroupBox
from cross_field_highlighter.ui.dialog.adhoc.highlight.source_group_box import SourceGroupBox

log: Logger = logging.getLogger(__name__)


class AdhocHighlightDialogView(QDialog):

    def __init__(self, model: AdhocHighlightDialogModel, note_type_details_factory: NoteTypeDetailsFactory):
        super().__init__(parent=None)
        self.__model: AdhocHighlightDialogModel = model
        self.__note_type_details_factory: NoteTypeDetailsFactory = note_type_details_factory
        self.setVisible(False)
        # noinspection PyUnresolvedReferences
        self.setWindowTitle('Highlight')

        source_group_box: SourceGroupBox = SourceGroupBox(model)
        self.__format_group_box: FormatGroupBox = FormatGroupBox(model)

        button_box: QDialogButtonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                                        QDialogButtonBox.StandardButton.Cancel |
                                                        QDialogButtonBox.StandardButton.RestoreDefaults)
        start_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.Ok)
        start_button.setText("Start")
        self.__destination_group_box: DestinationGroupBox = DestinationGroupBox(model)
        # noinspection PyUnresolvedReferences
        button_box.accepted.connect(self.__accept)
        # noinspection PyUnresolvedReferences
        button_box.rejected.connect(self.__reject)
        restore_defaults_button: QPushButton = button_box.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        # noinspection PyUnresolvedReferences
        restore_defaults_button.setToolTip('Reset settings in this dialog to defaults')
        # noinspection PyUnresolvedReferences
        restore_defaults_button.clicked.connect(self.__restore_defaults)

        layout: QGridLayout = QGridLayout(self)
        layout.addWidget(source_group_box, 0, 0, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.__format_group_box, 0, 1, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.__destination_group_box, 0, 2, Qt.AlignmentFlag.AlignTop)
        layout.addWidget(button_box, 3, 0, Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)
        self.resize(300, 200)
        log.debug(f"{self.__class__.__name__} was instantiated")

    def show_view(self) -> None:
        log.debug(f"Show view")
        if not self.__model.current_state or not self.__model.current_state.selected_note_type:
            if len(self.__model.note_types) > 0:
                selected_note_type_details: NoteTypeDetails = self.__model.note_types[0]
                self.__model.switch_state(selected_note_type_details)
        self.__model.fire_model_changed(self)
        # noinspection PyUnresolvedReferences
        self.show()
        self.adjustSize()

    def __accept(self) -> None:
        log.info("Starting")
        self.hide()
        if self.__model.accept_callback:
            self.__model.accept_callback()

    def __reject(self) -> None:
        log.info("Cancelled")
        self.hide()
        if self.__model.reject_callback:
            self.__model.reject_callback()

    def __restore_defaults(self) -> None:
        log.info("Restore defaults")
        self.__model.current_state.selected_note_type = None
        self.__model.current_state.selected_source_field = None
        self.__model.current_state.selected_format = None
        self.__model.current_state.selected_stop_words = self.__model.default_stop_words
        self.__model.current_state.selected_destination_fields = FieldNames([])
        self.__model.fire_model_changed(None)

    def __repr__(self):
        return self.__class__.__name__

    def __del__(self):
        log.debug(f"{self.__class__.__name__} was deleted")
