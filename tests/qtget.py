from aqt import QComboBox


def get_items(combo_box: QComboBox) -> list[str]:
    return [combo_box.itemText(i) for i in range(combo_box.count())]
