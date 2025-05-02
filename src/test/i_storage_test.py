"""Module containing tests for the different types of Storage"""

# pylint: disable=protected-access, missing-class-docstring, pointless-statement, expression-not-assigned

import pytest

from abllib.error import InternalFunctionUsedError, InvalidKeyError, KeyNotFoundError, SingletonInstantiationError, WrongTypeError
from abllib._storage import _BaseStorage, _InternalStorage

def test_basestorage_instantiation():
    """Ensure that BaseStorage cannot be initialized"""

    with pytest.raises(NotImplementedError):
        _BaseStorage()

def test_basestorage_getitem():
    """Test the Storage.__getitem__() method"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage._store["key1"] = "value"
    assert BaseStorage["key1"] == "value"

    BaseStorage._store["key1"] = {}
    BaseStorage._store["key1"]["key2"] = "value2"
    assert BaseStorage["key1"]["key2"] == "value2"

def test_basestorage_getitem_multi():
    """Test the Storage.__getitem__() method with subdicts specified in the key"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage._store["key1"] = {}
    BaseStorage._store["key1"]["key2"] = "value2"
    assert BaseStorage["key1.key2"] == "value2"

    BaseStorage._store["key1"] = {}
    BaseStorage._store["key1"]["key2"] = {}
    BaseStorage._store["key1"]["key2"]["key3"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]["key6"] = "values"
    assert BaseStorage["key1.key2.key3.key4.key5.key6"] == "values"

def test_basestorage_getitem_keytype():
    """Test the Storage.__getitem__() methods' protection against incorrect key types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(WrongTypeError):
        BaseStorage[None]
    with pytest.raises(WrongTypeError):
        BaseStorage[10]
    with pytest.raises(WrongTypeError):
        BaseStorage[list(("1",))]

    with pytest.raises(InvalidKeyError):
        BaseStorage[".some.key"]
    with pytest.raises(InvalidKeyError):
        BaseStorage["some.key."]
    with pytest.raises(InvalidKeyError):
        BaseStorage["some..key"]

def test_basestorage_getitem_valuetype():
    """Test the Storage.__getitem__() methods' support for different value types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage._store["key1"] = ["1", 2, None]
    assert BaseStorage["key1"] == ["1", 2, None]

def test_basestorage_getitem_wrong_key():
    """Test the Storage.__getitem__() methods' protection against nonexistent keys"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(KeyNotFoundError):
        BaseStorage["key1"]
    with pytest.raises(KeyNotFoundError):
        BaseStorage["key1.key2"]
    with pytest.raises(KeyNotFoundError):
        BaseStorage["key1.key2.key3.key4.key5.key6"]

def test_basestorage_setitem():
    """Test the Storage.__setitem__() method"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage["key1"] = "value"
    assert BaseStorage._store["key1"] == "value"

    BaseStorage["key1"] = {}
    BaseStorage["key1"]["key2"] = "value2"
    assert BaseStorage._store["key1"]["key2"] == "value2"

def test_basestorage_setitem_multi():
    """Test the Storage.__setitem__() method with subdicts specified in the key"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage["key1"] = {}
    BaseStorage["key1.key2"] = "value2"
    assert BaseStorage._store["key1"]["key2"] == "value2"

    BaseStorage["key1"] = {}
    BaseStorage["key1.key2"] = {}
    BaseStorage["key1.key2.key3"] = {}
    BaseStorage["key1.key2.key3.key4"] = {}
    BaseStorage["key1.key2.key3.key4.key5"] = {}
    BaseStorage["key1.key2.key3.key4.key5.key6"] = "values"
    assert BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]["key6"] == "values"

def test_basestorage_setitem_create_subdict():
    """Test the Storage.__setitem__() methods' ability to create missing 'inbetween' dictionaries"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage["key1.key2"] = "value2"
    assert isinstance(BaseStorage._store["key1"], dict)
    assert BaseStorage._store["key1"]["key2"] == "value2"

    BaseStorage["key1.key2"] = {}

    BaseStorage["key1.key2.key3.key4.key5.key6"] = "values"
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"], dict)
    assert BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]["key6"] == "values"

def test_basestorage_setitem_keytype():
    """Test the Storage.__setitem__() methods' protection against incorrect key types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(WrongTypeError):
        BaseStorage[None] = "value"
    with pytest.raises(WrongTypeError):
        BaseStorage[10] = "value"
    with pytest.raises(WrongTypeError):
        BaseStorage[list(("1",))] = "value"

    with pytest.raises(InvalidKeyError):
        BaseStorage[".some.key"] = "value"
    with pytest.raises(InvalidKeyError):
        BaseStorage["some.key."] = "value"
    with pytest.raises(InvalidKeyError):
        BaseStorage["some..key"] = "value"

def test_basestorage_setitem_valuetype():
    """Test the Storage.__setitem__() methods' support for different value types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage["key1"] = ["1", 2, None]
    assert BaseStorage._store["key1"] == ["1", 2, None]

    class CustomType():
        pass
    custom_item = CustomType()
    BaseStorage["key1"] = custom_item
    assert BaseStorage._store["key1"] == custom_item

def test_basestorage_delitem():
    """Test the Storage.__delitem__() method"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage._store["key1"] = "value"
    del BaseStorage["key1"]
    assert "key1" not in BaseStorage._store

def test_basestorage_delitem_multi():
    """Test the Storage.__delitem__() method with subdicts specified in the key"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage._store["key1"] = {}
    BaseStorage._store["key1"]["key2"] = "value2"
    del BaseStorage["key1.key2"]
    assert isinstance(BaseStorage._store["key1"], dict)
    assert "key2" not in BaseStorage._store["key1"]

    BaseStorage._store = {}

    BaseStorage._store["key1"] = {}
    BaseStorage._store["key1"]["key2"] = {}
    BaseStorage._store["key1"]["key2"]["key3"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]["key6"] = "values"
    del BaseStorage["key1.key2.key3.key4.key5.key6"]
    assert isinstance(BaseStorage._store["key1"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"]["key4"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"], dict)
    assert "key6" not in BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]

    BaseStorage._store = {}

    BaseStorage["key1.key2.key3.key4.key5.key6"] = "values"
    BaseStorage["key1.key2.key3.key4.key5.another"] = "value2"
    del BaseStorage["key1.key2.key3.key4.key5.key6"]
    assert isinstance(BaseStorage._store["key1"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"]["key4"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"], dict)
    assert "another" in BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]
    assert "key6" not in BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]

    BaseStorage._store = {}

    BaseStorage["key1.key2.key3.key4.key5.key6"] = "values"
    del BaseStorage["key1.key2.key3.key4.key5.key6"]
    assert "key1.key2.key3.key4.key5" not in BaseStorage
    assert "key1.key2.key3.key4" not in BaseStorage
    assert "key1.key2.key3" not in BaseStorage
    assert "key1.key2" not in BaseStorage
    assert "key1" not in BaseStorage

def test_basestorage_delitem_keytype():
    """Test the Storage.__delitem__() methods' protection against incorrect key types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(WrongTypeError):
        del BaseStorage[None]
    with pytest.raises(WrongTypeError):
        del BaseStorage[10]
    with pytest.raises(WrongTypeError):
        del BaseStorage[list(("1",))]

    with pytest.raises(InvalidKeyError):
        del BaseStorage[".some.key"]
    with pytest.raises(InvalidKeyError):
        del BaseStorage["some.key."]
    with pytest.raises(InvalidKeyError):
        del BaseStorage["some..key"]

def test_basestorage_delitem_wrong_key():
    """Test the Storage.__delitem__() methods' protection against nonexistent keys"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(KeyNotFoundError):
        del BaseStorage["key1"]
    with pytest.raises(KeyNotFoundError):
        del BaseStorage["key1.key2"]
    with pytest.raises(KeyNotFoundError):
        del BaseStorage["key1.key2.key3.key4.key5.key6"]

def test_basestorage_pop():
    """Test the Storage.pop() method"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage._store["key1"] = "value"
    val = BaseStorage.pop("key1")
    assert val == "value"
    assert "key1" not in BaseStorage._store

def test_basestorage_pop_multi():
    """Test the Storage.pop() method with subdicts specified in the key"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    BaseStorage._store["key1"] = {}
    BaseStorage._store["key1"]["key2"] = "value2"
    val = BaseStorage.pop("key1.key2")
    assert val == "value2"
    assert isinstance(BaseStorage._store["key1"], dict)
    assert "key2" not in BaseStorage._store["key1"]

    BaseStorage._store["key1"] = {}
    BaseStorage._store["key1"]["key2"] = {}
    BaseStorage._store["key1"]["key2"]["key3"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"] = {}
    BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]["key6"] = "values"
    val = BaseStorage.pop("key1.key2.key3.key4.key5.key6")
    assert val == "values"
    assert isinstance(BaseStorage._store["key1"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"]["key4"], dict)
    assert isinstance(BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"], dict)
    assert "key2" not in BaseStorage._store["key1"]["key2"]["key3"]["key4"]["key5"]

def test_basestorage_pop_keytype():
    """Test the Storage.pop() methods' protection against incorrect key types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(WrongTypeError):
        BaseStorage.pop(None)
    with pytest.raises(WrongTypeError):
        BaseStorage.pop(10)
    with pytest.raises(WrongTypeError):
        BaseStorage.pop(list(("1",)))

    with pytest.raises(InvalidKeyError):
        BaseStorage.pop(".some.key")
    with pytest.raises(InvalidKeyError):
        BaseStorage.pop("some.key.")
    with pytest.raises(InvalidKeyError):
        BaseStorage.pop("some..key")

def test_basestorage_pop_wrong_key():
    """Test the Storage.pop() methods' protection against nonexistent keys"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(KeyNotFoundError):
        BaseStorage.pop("key1")
    with pytest.raises(KeyNotFoundError):
        BaseStorage.pop("key1.key2")
    with pytest.raises(KeyNotFoundError):
        BaseStorage.pop("key1.key2.key3.key4.key5.key6")

def test_basestorage_contains():
    """Test the Storage.contains() method"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    assert not BaseStorage.contains("key1")
    assert "key1" not in BaseStorage

    BaseStorage["key1"] = "value"
    assert BaseStorage.contains("key1")
    assert "key1" in BaseStorage

def test_basestorage_contains_multi():
    """Test the Storage.contains() method with subdicts specified in the key"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    assert not BaseStorage.contains("key1.key2")
    assert "key1.key2" not in BaseStorage

    BaseStorage["key1.key2"] = "value2"
    assert BaseStorage.contains("key1.key2")
    assert "key1.key2" in BaseStorage

    del BaseStorage["key1"]

    assert not BaseStorage.contains("key1.key2.key3.key4.key5.key6")
    assert "key1.key2.key3.key4.key5.key6" not in BaseStorage

    BaseStorage["key1.key2.key3.key4.key5.key6"] = "values"
    assert BaseStorage.contains("key1.key2.key3.key4.key5.key6")
    assert "key1.key2.key3.key4.key5.key6" in BaseStorage

def test_basestorage_contains_keytype():
    """Test the Storage.contains() methods' protection against incorrect key types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(WrongTypeError):
        None in BaseStorage
    with pytest.raises(WrongTypeError):
        10 in BaseStorage
    with pytest.raises(WrongTypeError):
        list(("1",)) in BaseStorage

    with pytest.raises(InvalidKeyError):
        ".some.key" in BaseStorage
    with pytest.raises(InvalidKeyError):
        "some.key." in BaseStorage
    with pytest.raises(InvalidKeyError):
        "some..key" in BaseStorage

def test_basestorage_contains_item():
    """Test the Storage.contains_item() method"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    assert not BaseStorage.contains_item("key1", "value")

    BaseStorage["key1"] = "value"
    assert BaseStorage.contains_item("key1", "value")

def test_basestorage_contains_item_multi():
    """Test the Storage.contains_item() method with subdicts specified in the key"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    assert not BaseStorage.contains_item("key1.key2", "value")

    BaseStorage["key1.key2"] = "value2"
    assert BaseStorage.contains_item("key1.key2", "value2")

    del BaseStorage["key1"]

    assert not BaseStorage.contains_item("key1.key2.key3.key4.key5.key6", "values")

    BaseStorage["key1.key2.key3.key4.key5.key6"] = "values"
    assert BaseStorage.contains_item("key1.key2.key3.key4.key5.key6", "values")

def test_basestorage_contains_item_keytype():
    """Test the Storage.contains_item() methods' protection against incorrect key types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    with pytest.raises(WrongTypeError):
        BaseStorage.contains_item(None, "value")
    with pytest.raises(WrongTypeError):
        BaseStorage.contains_item(10, "value")
    with pytest.raises(WrongTypeError):
        BaseStorage.contains_item(list(("1",)), "value")

    with pytest.raises(InvalidKeyError):
        BaseStorage.contains_item(".some.key", "value")
    with pytest.raises(InvalidKeyError):
        BaseStorage.contains_item("some.key.", "value")
    with pytest.raises(InvalidKeyError):
        BaseStorage.contains_item("some..key", "value")

def test_basestorage_contains_item_valuetype():
    """Test the Storage.contains_item() methods' support for different value types"""

    BaseStorage = _BaseStorage.__new__(_BaseStorage)
    BaseStorage._store = {}

    assert not BaseStorage.contains_item("key1", ["1", 2, None])

    BaseStorage["key1"] = ["1", 2, None]
    assert BaseStorage.contains_item("key1", ["1", 2, None])

def test_internalstorage_inheritance():
    """Ensure the InternalStorage inherits from _BaseStorage"""

    InternalStorage = _InternalStorage.__new__(_InternalStorage)
    InternalStorage._store = {}

    assert isinstance(InternalStorage, _BaseStorage)

def test_internalstorage_instantiation():
    """Ensure that InternalStorage behaves like a singleton"""

    with pytest.raises(SingletonInstantiationError):
        _InternalStorage()._init()

    with pytest.raises(SingletonInstantiationError):
        _InternalStorage()._init()

def test_internalstorage_setitem():
    """Ensure that InternalStorage only accepts keys prefixed with '__'"""

    InternalStorage = _InternalStorage.__new__(_InternalStorage)
    InternalStorage._store = {}

    with pytest.raises(InternalFunctionUsedError):
        InternalStorage["key1"] = "value"
    with pytest.raises(InternalFunctionUsedError):
        InternalStorage["key1_"] = "value"
    with pytest.raises(InternalFunctionUsedError):
        InternalStorage["key__1"] = "value"

    InternalStorage["_key0"] = "value1"
    assert InternalStorage._store["_key0"] == "value1"

    InternalStorage["_key1._key2"] = "value2"
    assert InternalStorage._store["_key1"]["_key2"] == "value2"

    InternalStorage["_key2.key2"] = "value3"
    assert InternalStorage._store["_key2"]["key2"] == "value3"
