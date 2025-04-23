"""Module containing tests for the different types of Storage"""

# pylint: disable=protected-access, missing-class-docstring, pointless-statement, expression-not-assigned

import json
import os

import pytest

from abllib import error, storage, _storage

def test_volatilestorage_inheritance():
    """Ensure the VolatileStorage inherits from _BaseStorage"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}

    assert isinstance(VolatileStorage, _storage._base_storage._BaseStorage)
    assert not isinstance(VolatileStorage, storage._persistent_storage._PersistentStorage)

def test_volatilestorage_instantiation():
    """Ensure that VolatileStorage behaves like a singleton"""

    with pytest.raises(error.SingletonInstantiationError):
        storage._volatile_storage._VolatileStorage().initialize()

    with pytest.raises(error.SingletonInstantiationError):
        storage._volatile_storage._VolatileStorage().initialize()

def test_volatilestorage_valuetype():
    """Test the VolatileStorages' support for different value types"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}

    VolatileStorage["key1"] = ["1", 2, None]
    assert VolatileStorage["key1"] == ["1", 2, None]

    class CustomType():
        pass
    custom_item = CustomType()
    VolatileStorage["key1"] = custom_item
    assert VolatileStorage["key1"] == custom_item

def test_volatilestorage_noinit_error():
    """Ensure the VolatileStorage methods don't work before initialization is complete"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = None

    with pytest.raises(error.NotInitializedError):
        VolatileStorage["testkey"]
    with pytest.raises(error.NotInitializedError):
        VolatileStorage["testkey"] = "testvalue"
    with pytest.raises(error.NotInitializedError):
        del VolatileStorage["testkey"]
    with pytest.raises(error.NotInitializedError):
        VolatileStorage.contains("testkey")
    with pytest.raises(error.NotInitializedError):
        VolatileStorage.contains_item("testkey", "testvalue")

    try:
        VolatileStorage["testkey"]
    except error.NotInitializedError as exc:
        assert "VolatileStorage is not yet initialized" in str(exc)
    else:
        pytest.fail("expected exception")

def test_volatilestorage_del_autoremovedict():
    """Test that AutoremoveDicts are correctly deleted on del"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}

    VolatileStorage["key1.key2.key3.key4.key5.key6"] = "values"
    del VolatileStorage["key1.key2.key3.key4.key5.key6"]
    assert "key1.key2.key3.key4.key5" not in VolatileStorage
    assert "key1.key2.key3.key4" not in VolatileStorage
    assert "key1.key2.key3" not in VolatileStorage
    assert "key1.key2" not in VolatileStorage
    assert "key1" not in VolatileStorage

def test_persistentstorage_inheritance():
    """Ensure the PersistentStorage inherits from _BaseStorage"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    assert isinstance(PersistentStorage, _storage._base_storage._BaseStorage)
    assert not isinstance(PersistentStorage, storage._volatile_storage._VolatileStorage)

def test_persistentstorage_instantiation():
    """Ensure that PersistentStorage behaves like a singleton"""

    with pytest.raises(error.SingletonInstantiationError):
        storage._persistent_storage._PersistentStorage().initialize("test.json")

    with pytest.raises(error.SingletonInstantiationError):
        storage._persistent_storage._PersistentStorage().initialize("test.json")

def test_persistentstorage_valuetype():
    """Test the PersistentStorages' support for different value types"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    PersistentStorage["key1"] = True
    assert PersistentStorage["key1"] is True
    PersistentStorage["key1"] = 10
    assert PersistentStorage["key1"] == 10
    PersistentStorage["key1"] = 10.1
    assert PersistentStorage["key1"] == 10.1
    PersistentStorage["key1"] = "value"
    assert PersistentStorage["key1"] == "value"
    PersistentStorage["key1"] = ["1", "2"]
    assert PersistentStorage["key1"] == ["1", "2"]
    PersistentStorage["key1"] = {"key": "item"}
    assert PersistentStorage["key1"] == {"key": "item"}
    PersistentStorage["key1"] = ("1", "2")
    assert PersistentStorage["key1"] == ("1", "2")
    PersistentStorage["key1"] = None
    assert PersistentStorage["key1"] is None

    class CustomType():
        pass

    with pytest.raises(TypeError):
        PersistentStorage["key1"] = CustomType()

def test_persistentstorage_load_file():
    """Test the PersistentStorage._load_from_disk() method"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    filepath = _storage.InternalStorage["_storage_file"]

    with open(filepath, "w", encoding="utf8") as f:
        json.dump({
            "key1": "value",
            "key2": [
                "value21",
                "value22",
                "value23"
            ],
            "key3": 10
        }, f)

    PersistentStorage.load_from_disk()

    assert PersistentStorage["key1"] == "value"
    assert PersistentStorage["key2"] == ["value21", "value22", "value23"]
    assert PersistentStorage["key3"] == 10

    os.remove(filepath)

def test_persistentstorage_save_file():
    """Test the PersistentStorage._save_to_disk() method"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    filepath = _storage.InternalStorage["_storage_file"]

    PersistentStorage["key1"] = "value"
    PersistentStorage["key2"] = ["value21", "value22", "value23"]
    PersistentStorage["key4"] = 10

    PersistentStorage.save_to_disk()

    assert os.path.isfile(filepath)
    with open(filepath, "r", encoding="utf8") as f:
        data = json.load(f)
    assert data["key1"] == "value"
    assert data["key2"] == ["value21", "value22", "value23"]
    assert data["key4"] == 10

    os.remove(filepath)

def test_persistentstorage_save_file_empty():
    """
    Ensure the PersistentStorage._save_to_disk() method doesn't overwrite an existing file
    if the PersistentStorage is empty
    """

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    filepath = _storage.InternalStorage["_storage_file"]

    with open(filepath, "w", encoding="utf8") as f:
        json.dump({
            "key1": "newvalue"
        }, f)

    PersistentStorage.save_to_disk()

    with open(filepath, "r", encoding="utf8") as f:
        assert json.load(f)["key1"] == "newvalue"

def test_persistentstorage_noinit_error():
    """Ensure the PersistentStorage methods don't work before initialization is complete"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = None

    with pytest.raises(error.NotInitializedError):
        PersistentStorage["testkey"]
    with pytest.raises(error.NotInitializedError):
        PersistentStorage["testkey"] = "testvalue"
    with pytest.raises(error.NotInitializedError):
        del PersistentStorage["testkey"]
    with pytest.raises(error.NotInitializedError):
        PersistentStorage.contains("testkey")
    with pytest.raises(error.NotInitializedError):
        PersistentStorage.contains_item("testkey", "testvalue")

    try:
        PersistentStorage["testkey"]
    except error.NotInitializedError as exc:
        assert "PersistentStorage is not yet initialized" in str(exc)
    else:
        pytest.fail("expected exception")

def test_persistentstorage_del_autoremovedict():
    """Test that AutoremoveDicts are correctly deleted on del"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    PersistentStorage["key1.key2.key3.key4.key5.key6"] = "values"
    del PersistentStorage["key1.key2.key3.key4.key5.key6"]
    assert "key1.key2.key3.key4.key5" not in PersistentStorage
    assert "key1.key2.key3.key4" not in PersistentStorage
    assert "key1.key2.key3" not in PersistentStorage
    assert "key1.key2" not in PersistentStorage
    assert "key1" not in PersistentStorage

def test_storageview_instantiation():
    """Ensure that instantiating StorageView only works with valid arguments"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}
    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}
    StorageView = storage._StorageView()
    StorageView._storages = []
    StorageView.add_storage(VolatileStorage)
    StorageView.add_storage(PersistentStorage)

    class FakeStorage():
        pass

    with pytest.raises(error.MissingInheritanceError):
        StorageView.add_storage(FakeStorage)

def test_storageview_getitem():
    """Test the Storage.__getitem__() method"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}
    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}
    StorageView = storage._StorageView()
    StorageView._storages = []
    StorageView.add_storage(VolatileStorage)
    StorageView.add_storage(PersistentStorage)

    VolatileStorage["key1"] = "value"
    PersistentStorage["key2"] = "value2"
    assert StorageView["key1"] == "value"
    assert StorageView["key2"] == "value2"

    del VolatileStorage["key1"]
    del PersistentStorage["key2"]

    VolatileStorage["key1.key2.key3"] = "value"
    PersistentStorage["key2.key3.key4.key5.key6.key7"] = "value2"
    assert StorageView["key1.key2.key3"] == "value"
    assert StorageView["key2.key3.key4.key5.key6.key7"] == "value2"

def test_storageview_contains():
    """Test the Storage.contains() method"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}
    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}
    StorageView = storage._StorageView()
    StorageView._storages = []
    StorageView.add_storage(VolatileStorage)
    StorageView.add_storage(PersistentStorage)

    VolatileStorage["key1"] = "value"
    PersistentStorage["key2"] = "value2"
    assert StorageView.contains("key1")
    assert "key1" in StorageView
    assert StorageView.contains("key2")
    assert "key2" in StorageView

    del VolatileStorage["key1"]
    del PersistentStorage["key2"]

    VolatileStorage["key1.key2.key3"] = "value"
    PersistentStorage["key2.key3.key4.key5.key6.key7"] = "value2"
    assert StorageView.contains("key1.key2.key3")
    assert "key1.key2.key3" in StorageView
    assert StorageView.contains("key2.key3.key4.key5.key6.key7")
    assert "key2.key3.key4.key5.key6.key7" in StorageView

def test_storageview_contains_item():
    """Test the Storage.contains_item() method"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}
    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}
    StorageView = storage._StorageView()
    StorageView._storages = []
    StorageView.add_storage(VolatileStorage)
    StorageView.add_storage(PersistentStorage)

    VolatileStorage["key1"] = "value"
    PersistentStorage["key2"] = "value2"
    assert StorageView.contains_item("key1", "value")
    assert StorageView.contains_item("key2", "value2")

    del VolatileStorage["key1"]
    del PersistentStorage["key2"]

    VolatileStorage["key1.key2.key3"] = "value"
    PersistentStorage["key2.key3.key4.key5.key6.key7"] = "value2"
    assert StorageView.contains_item("key1.key2.key3", "value")
    assert StorageView.contains_item("key2.key3.key4.key5.key6.key7", "value2")

def test_storageview_noinit_error():
    """Ensure the StorageView methods don't work before initialization is complete"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = None
    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = None
    StorageView = storage._StorageView()
    StorageView._storages = []
    StorageView.add_storage(VolatileStorage)
    StorageView.add_storage(PersistentStorage)

    with pytest.raises(error.NotInitializedError):
        StorageView["testkey"]
    with pytest.raises(error.NotInitializedError):
        StorageView.contains("testkey")
    with pytest.raises(error.NotInitializedError):
        StorageView.contains_item("testkey", "testvalue")

    try:
        StorageView["testkey"]
    except error.NotInitializedError as exc:
        # the first storage should raise an error
        assert "VolatileStorage is not yet initialized" in str(exc)
    else:
        pytest.fail("expected exception")

    VolatileStorage._store = {}

    try:
        StorageView["testkey"]
    except error.NotInitializedError as exc:
        # the second storage should raise an error
        assert "PersistentStorage is not yet initialized" in str(exc)
    else:
        pytest.fail("expected exception")

    PersistentStorage._store = {"testkey": "testval"}

    assert StorageView.contains_item("testkey", "testval")
