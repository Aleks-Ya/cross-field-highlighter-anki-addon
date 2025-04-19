from typing import Any

from aqt import ProfileManager

from cross_field_highlighter.config.user_files_storage import UserFilesStorage
from cross_field_highlighter.highlighter.note_type_details import NoteTypeDetails
from cross_field_highlighter.highlighter.types import Profile
from tests.data import DefaultFields


def test_write_read(user_files_storage: UserFilesStorage, note_type_details_basic: NoteTypeDetails):
    key: str = "state"
    # Write new key
    exp_value_1: dict[str, Any] = {"item": "about",
                                   "nested": {"note_type": note_type_details_basic.name,
                                              "field": DefaultFields.basic_front}}
    user_files_storage.write(key, exp_value_1)
    act_value_1: dict[str, Any] = user_files_storage.read(key)
    assert act_value_1 == exp_value_1
    assert user_files_storage.read_all() == {
        key: {'item': 'about', 'nested': {'note_type': note_type_details_basic.name,
                                          'field': DefaultFields.basic_front}}}
    # Update existing key
    exp_value_2: dict[str, Any] = {"status": "done", "nested": {"field": DefaultFields.basic_back}}
    user_files_storage.write(key, exp_value_2)
    act_value_2: dict[str, Any] = user_files_storage.read(key)
    assert act_value_2 == exp_value_2
    assert user_files_storage.read_all() == {key: {'nested': {'field': DefaultFields.basic_back},
                                                   'status': 'done'}}


def test_write_read_several_keys(user_files_storage: UserFilesStorage, note_type_details_basic: NoteTypeDetails):
    key_1: str = "state"
    key_2: str = "data"
    exp_value_1: dict[str, Any] = {"item": "about",
                                   "nested": {"note_type": note_type_details_basic.name,
                                              "field": DefaultFields.basic_front}}
    exp_value_2: dict[str, Any] = {"status": "done", "nested": {"field": DefaultFields.basic_back}}
    user_files_storage.write(key_1, exp_value_1)
    user_files_storage.write(key_2, exp_value_2)
    act_value_1: dict[str, Any] = user_files_storage.read(key_1)
    act_value_2: dict[str, Any] = user_files_storage.read(key_2)
    assert act_value_1 == exp_value_1
    assert act_value_2 == exp_value_2
    assert user_files_storage.read_all() == {
        key_2: {'nested': {'field': DefaultFields.basic_back}, 'status': 'done'},
        key_1: {'item': 'about', 'nested': {'note_type': note_type_details_basic.name,
                                            'field': DefaultFields.basic_front}}}


def test_write_read_different_profiles(user_files_storage: UserFilesStorage,
                                       note_type_details_basic: NoteTypeDetails, profile_manager: ProfileManager):
    key: str = "state"
    profile_1: Profile = Profile("User 1")
    profile_2: Profile = Profile("User 2")
    profile_manager.create(profile_1)
    profile_manager.create(profile_2)
    profile_manager.save()

    # Write 1st profile
    profile_manager.openProfile(profile_1)
    exp_value_1: dict[str, Any] = {"item": "About 1"}
    user_files_storage.write(key, exp_value_1)
    assert user_files_storage.read_all() == {key: exp_value_1}

    # Write 2nd profile
    profile_manager.openProfile(profile_2)
    exp_value_2: dict[str, Any] = {"item": "About 2"}
    user_files_storage.write(key, exp_value_2)
    assert user_files_storage.read_all() == {key: exp_value_2}

    # Read 1st profile
    profile_manager.openProfile(profile_1)
    assert user_files_storage.read_all() == {key: exp_value_1}

    # Read 2st profile
    profile_manager.openProfile(profile_2)
    assert user_files_storage.read_all() == {key: exp_value_2}


def test_read_absent_key(user_files_storage: UserFilesStorage):
    value: dict[str, Any] = user_files_storage.read("not-exists")
    assert value == {}
    assert user_files_storage.read_all() == {}


def test_write_empty_value(user_files_storage: UserFilesStorage):
    key: str = "empty"
    user_files_storage.write(key, {})
    value: dict[str, Any] = user_files_storage.read(key)
    assert value == {}
    assert user_files_storage.read_all() == {'empty': {}}


def test_read_all_empty(user_files_storage: UserFilesStorage):
    assert user_files_storage.read_all() == {}
