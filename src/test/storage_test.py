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
        storage._volatile_storage._VolatileStorage()._init()

    with pytest.raises(error.SingletonInstantiationError):
        storage._volatile_storage._VolatileStorage()._init()

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

def test_persistentstorage_inheritance():
    """Ensure the PersistentStorage inherits from _BaseStorage"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    assert isinstance(PersistentStorage, _storage._base_storage._BaseStorage)
    assert not isinstance(PersistentStorage, storage._volatile_storage._VolatileStorage)

def test_persistentstorage_instantiation():
    """Ensure that PersistentStorage behaves like a singleton"""

    with pytest.raises(error.SingletonInstantiationError):
        storage._persistent_storage._PersistentStorage()._init()

    with pytest.raises(error.SingletonInstantiationError):
        storage._persistent_storage._PersistentStorage()._init()

def test_persistentstorage_valuetype():
    """Test the PersistentStorages' support for different value types"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    PersistentStorage["key1"] = "value"
    assert PersistentStorage["key1"] == "value"
    PersistentStorage["key1"] = 10
    assert PersistentStorage["key1"] == 10
    PersistentStorage["key1"] = ["1", "2"]
    assert PersistentStorage["key1"] == ["1", "2"]
    PersistentStorage["key1"] = {"key": "item"}
    assert PersistentStorage["key1"] == {"key": "item"}

    class CustomType():
        pass

    with pytest.raises(TypeError):
        PersistentStorage["key1"] = CustomType()

def test_persistentstorage_load_file():
    """Test the PersistentStorage._load_from_disk() method"""

    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    filepath = storage.VolatileStorage["storage_file"]

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

    filepath = storage.VolatileStorage["storage_file"]

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

    filepath = storage.VolatileStorage["storage_file"]

    with open(filepath, "w", encoding="utf8") as f:
        json.dump({
            "key1": "newvalue"
        }, f)

    PersistentStorage.save_to_disk()

    with open(filepath, "r", encoding="utf8") as f:
        assert json.load(f)["key1"] == "newvalue"

def test_storageview_instantiation():
    """Ensure that instantiating StorageView only works with valid arguments"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}
    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}

    storage._StorageView()._init([
        PersistentStorage,
        VolatileStorage
    ])

    class FakeStorage():
        pass

    with pytest.raises(error.MissingInheritanceError):
        storage._StorageView()._init([
            FakeStorage
        ])

    with pytest.raises(error.MissingInheritanceError):
        storage._StorageView()._init([
            PersistentStorage,
            VolatileStorage,
            FakeStorage
        ])

def test_storageview_getitem():
    """Test the Storage.__getitem__() method"""

    VolatileStorage = storage._volatile_storage._VolatileStorage()
    VolatileStorage._store = {}
    PersistentStorage = storage._persistent_storage._PersistentStorage()
    PersistentStorage._store = {}
    StorageView = storage._StorageView()
    StorageView._init([
        PersistentStorage,
        VolatileStorage
    ])

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
    StorageView._init([
        PersistentStorage,
        VolatileStorage
    ])

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
    StorageView._init([
        PersistentStorage,
        VolatileStorage
    ])

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
