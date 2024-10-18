from aqt import QLabel
from PyQtPath.path_chain_pyqt6 import path

from cross_field_highlighter.ui.dialog.adhoc.highlight.adhoc_highlight_dialog_view import AdhocHighlightDialogView
from cross_field_highlighter.ui.widgets import TitledComboBoxLayout


def test_dialog(adhoc_highlight_dialog_view: AdhocHighlightDialogView):
    assert path(adhoc_highlight_dialog_view) is not None
    # noinspection PyUnresolvedReferences
    assert adhoc_highlight_dialog_view.windowTitle() == "Highlight"

    source_combo_box: TitledComboBoxLayout = path(adhoc_highlight_dialog_view).group().child(
        TitledComboBoxLayout).get()
    assert source_combo_box is not None
    note_type_label: QLabel = path(source_combo_box).label().get()
    assert note_type_label.text() == "Note Type"
