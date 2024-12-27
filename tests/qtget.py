from aqt import QComboBox


def get_item_texts(combo_box: QComboBox) -> list[str]:
    return [combo_box.itemText(i) for i in range(combo_box.count())]


def get_item_datas(combo_box: QComboBox) -> list[any]:
    return [combo_box.itemData(i) for i in range(combo_box.count())]
