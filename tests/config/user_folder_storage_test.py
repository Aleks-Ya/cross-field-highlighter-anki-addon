from cross_field_highlighter.config.user_folder_storage import UserFolderStorage


def test_write_read(user_folder_storage: UserFolderStorage):
    key: str = "state"
    # Write new key
    exp_value_1: dict[str, any] = {"item": "about", "nested": {"note_type": "Basic", "field": "Front"}}
    user_folder_storage.write(key, exp_value_1)
    act_value_1: dict[str, any] = user_folder_storage.read(key)
    assert act_value_1 == exp_value_1
    assert user_folder_storage.read_all() == {
        'state': {'item': 'about', 'nested': {'field': 'Front', 'note_type': 'Basic'}}}
    # Update existing key
    exp_value_2: dict[str, any] = {"status": "done", "nested": {"field": "Back"}}
    user_folder_storage.write(key, exp_value_2)
    act_value_2: dict[str, any] = user_folder_storage.read(key)
    assert act_value_2 == exp_value_2
    assert user_folder_storage.read_all() == {'state': {'nested': {'field': 'Back'}, 'status': 'done'}}


def test_write_read_several_keys(user_folder_storage: UserFolderStorage):
    key_1: str = "state"
    key_2: str = "data"
    exp_value_1: dict[str, any] = {"item": "about", "nested": {"note_type": "Basic", "field": "Front"}}
    exp_value_2: dict[str, any] = {"status": "done", "nested": {"field": "Back"}}
    user_folder_storage.write(key_1, exp_value_1)
    user_folder_storage.write(key_2, exp_value_2)
    act_value_1: dict[str, any] = user_folder_storage.read(key_1)
    act_value_2: dict[str, any] = user_folder_storage.read(key_2)
    assert act_value_1 == exp_value_1
    assert act_value_2 == exp_value_2
    assert user_folder_storage.read_all() == {
        'data': {'nested': {'field': 'Back'}, 'status': 'done'},
        'state': {'item': 'about', 'nested': {'field': 'Front', 'note_type': 'Basic'}}}


def test_read_absent_key(user_folder_storage: UserFolderStorage):
    value: dict[str, any] = user_folder_storage.read("not-exists")
    assert value == {}
    assert user_folder_storage.read_all() == {}


def test_write_empty_value(user_folder_storage: UserFolderStorage):
    key: str = "empty"
    user_folder_storage.write(key, {})
    value: dict[str, any] = user_folder_storage.read(key)
    assert value == {}
    assert user_folder_storage.read_all() == {'empty': {}}


def test_read_all_empty(user_folder_storage: UserFolderStorage):
    assert user_folder_storage.read_all() == {}
