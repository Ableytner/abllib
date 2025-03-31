# abllib

Ableytners' general-purpose python library.

Supports Python versions 3.10 - 3.13.

## Overview

This project contains many submodules, which are all optional and not dependent on each other. Feel free to only use the ones you need.

The following submodules are available:
1. Algorithms (`abllib.alg`)
2. Errors (`abllib.error`)
3. File system (`abllib.fs`)
4. Fuzzy matching (`abllib.fuzzy`)
5. Logging (`abllib.log`)
6. Storages (`abllib.storage`)
7. Parallel processing (`abllib.pproc`)
8. Function wrappers (`abllib.wrapper`)

## Submodules

### 1. Algorithms (`abllib.alg`)

This module contains general-purpose algorithms.

#### Levenshtein distance (`abllib.alg.levenshtein_distance`)

Calculate the [edit distance](https://en.wikipedia.org/wiki/Levenshtein_distance) between two words.

Example usage:
```py
>> from abllib.alg import levenshtein_distance
>> levenshtein_distance("house", "houses")
1
>> levenshtein_distance("mice", "mouse")
3
>> levenshtein_distance("thomas", "anna")
5
```

### 2. Errors (`abllib.error`)

This module contains a custom exception system, which supports default messages for different errors.

#### CustomException (`abllib.error.CustomException`)

The base class to all custom exceptions. This class cannot be invoked on its own, but should be subclassed to create your own error classes.

Note that all deriving classes should end with 'Error', not 'Exception', to stay consistent with the python naming scheme.

Example usage:
```py
>> from abllib.error import CustomException
>> class MySpecialError(CustomException):
..     default_message = "This error has a default message!"
>> raise MySpecialError()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MySpecialError: This error has a default message!
```

#### General purpose errors

This module also contains some premade general-purpose error types, which all derive from `CustomException`. The following error classes are provided:
* CalledMultipleTimesError
* DirNotFoundError
* InternalFunctionUsedError
* KeyNotFoundError
* LockAcquisitionTimeoutError
* MissingInheritanceError
* NoneTypeError
* NotInitializedError
* SingletonInstantiationError

### 3. File system (`abllib.fs`)

This module contains various file system-related functionality. All provided functions are tested and work correctly on Linux and Windows systems.

#### Absolute path (`abllib.fs.absolute`)

A function which accepts filenames / paths and makes them absolute, also resolving all symlinks and '..'-calls. If a relative path is provided, the current working directory is prepended. 

Example usage:
```py
>> from abllib.fs import absolute
>> absolute("image.png")
'C:\\MyUser\\Some\\sub\\dir\\image.png'
>> absolute("../../image.png")
'C:\\MyUser\\Some\\image.png'
>> absolute("C:\\MyUser\\Some\\image.png")
'C:\\MyUser\\Some\\image.png'
```

### 4. Fuzzy matching (`abllib.fuzzy`)

This module contains functions to search for strings within a list of strings, while applying [fuzzy searching logic](https://en.wikipedia.org/wiki/Approximate_string_matching).

### 5. Logging (`abllib.log`)

This module contains functions to easily log to the console or specified log files.

### 6. Storages (`abllib.storage`)

This module contains multiple storage types. All data stored in these storages is accessable from anywhere within the program, as each storage is a [singleton](https://en.wikipedia.org/wiki/Singleton_pattern). Multithreaded access is also allowed.

The data is stored as key:value pairs. The key needs to be of type `<class 'str'>`, the allowed value types are storage-specific.

#### Initialize storages

The storage can be initialized (enabled) in two different ways:

Enable all storages:
```py
>> from abllib import storage
>> storage.initialize()
```

Alternatively, only the VolatileStorage can be enabled:
```py
>> from abllib import VolatileStorage
>> VolatileStorage.initialize()
```

#### VolatileStorage (`abllib.VolatileStorage`)

This storage instance can hold any type of value. The stored data is reset after each program restart.

Example usage:

First the storage needs to be imported:
```py
>> from abllib import VolatileStorage
```

Items can be assigned in multiple ways:
```py
>> VolatileStorage["mykey"] = "myvalue"
>> VolatileStorage["toplevelkey.sublevelkey"] = "another value"
>> VolatileStorage["specialvalue"] = threading.Lock()
```

Presence of keys can be checked in multiple ways:
```py
>> "toplevelkey" in VolatileStorage
True
>> "toplevelkey.sublevelkey" in VolatileStorage
True
>> VolatileStorage.contains("toplevelkey")
True
>> in VolatileStorage.contains("toplevelkey.sublevelkey")
True
```

Items can be retrieved in multiple ways:
```py
>> VolatileStorage["mykey"]
'myvalue'
>> VolatileStorage["toplevelkey"]["sublevelkey"]
'another value'
>> VolatileStorage["toplevelkey.sublevelkey"]
'another value'
>> type(VolatileStorage["specialvalue"])
<class '_thread.lock'>
```

There also exists a way to check whether an item at a key matches a certain value:
```py
>> VolatileStorage.contains_item("toplevelkey.sublevelkey", "another value")
True
>> # is equal to:
>> VolatileStorage["toplevelkey.sublevelkey"] == "another value"
True
```

Items can be deleted in multiple ways:
```py
>> del VolatileStorage["mykey"]
>> del VolatileStorage["toplevelkey"]["sublevelkey"]
>> del VolatileStorage["toplevelkey.sublevelkey"] # TODO: implement properly
```
Trying to delete non-existent items raises an KeyNotFoundError.

#### PersistentStorage (`abllib.PersistentStorage`)

This storage instance automatically loads saved data on program start and saves its data on program exit.

It can only hold values of type str, int, list or dict.

Example usage:

First the storage needs to be imported:
```py
>> from abllib import PersistentStorage
```

Items can be assigned in multiple ways:
```py
>> PersistentStorage["mykey"] = "myvalue"
>> PersistentStorage["toplevelkey.sublevelkey"] = "another value"
```

Presence of keys can be checked in multiple ways:
```py
>> "toplevelkey" in PersistentStorage
True
>> "toplevelkey.sublevelkey" in PersistentStorage
True
>> PersistentStorage.contains("toplevelkey")
True
>> in PersistentStorage.contains("toplevelkey.sublevelkey")
True
```

Items can be retrieved in multiple ways:
```py
>> PersistentStorage["mykey"]
'myvalue'
>> PersistentStorage["toplevelkey"]["sublevelkey"]
'another value'
>> PersistentStorage["toplevelkey.sublevelkey"]
'another value'
```

There also exists a way to check whether an item at a key matches a certain value:
```py
>> PersistentStorage.contains_item("toplevelkey.sublevelkey", "another value")
True
>> # is equal to:
>> PersistentStorage["toplevelkey.sublevelkey"] == "another value"
True
```

Items can be deleted in multiple ways:
```py
>> del PersistentStorage["mykey"]
>> del PersistentStorage["toplevelkey"]["sublevelkey"]
>> del PersistentStorage["toplevelkey.sublevelkey"] # TODO: implement properly
```
Trying to delete non-existent items raises an KeyNotFoundError.

All storage data can be loaded and saved manually:
```py
>> PersistentStorage.load_from_disk()
>> PersistentStorage.save_to_disk()
```

#### StorageView (`abllib.StorageView`)

This instance is a read-only view on both VolatileStorage and PersistentStorage. It is useful to check whether a key exists in any of the storages.

The StorageView first checks PersistentStorage, then VolatileStorage.

Example usage:

First the storage needs to be imported:
```py
>> from abllib import StorageView
```

Presence of keys can be checked in multiple ways:
```py
>> "toplevelkey" in StorageView
True
>> "toplevelkey.sublevelkey" in StorageView
True
>> StorageView.contains("toplevelkey")
True
>> in StorageView.contains("toplevelkey.sublevelkey")
True
```

Items can be retrieved in multiple ways:
```py
>> StorageView["mykey"]
'myvalue'
>> StorageView["toplevelkey"]["sublevelkey"]
'another value'
>> StorageView["toplevelkey.sublevelkey"]
'another value'
```

There also exists a way to check whether an item at a key matches a certain value:
```py
>> StorageView.contains_item("toplevelkey.sublevelkey", "another value")
True
>> # is equal to:
>> StorageView["toplevelkey.sublevelkey"] == "another value"
True
```

### 7. Parallel processing (`abllib.pproc`)

This module contains parallel processing-related functionality, both thread-based and process-based.

#### Thread vs Process

The parallel processing module contains both thread-based and process-based methods with overlapping functionality.
To help decide which solution to use, the key differences are outlined below:

You should use thread-based processing if the parallel task:
* is not CPU-intensive
* modifies local variables
* doesn't need to be killable

Alternatively, you should use process-based processing if the parallel task:
* is doing CPU-intensive calculations
* needs to be killable

The reason as to why CPU-intensive tasks in python should run in different processes is due to the [GIL](https://realpython.com/python-gil/) (global interpreter lock), which is further explained in the linked article. This effectively makes multiple threads run as fast as one thread if the bottleneck is the CPU.

Another thing to consider is that thread-based processing is simple and straightforward, whereas process-based functionality can be pretty complex.
Arguments passed to another process, for example, lose the reference to its original object.
This means that passing a list to a different process and adding an element in that process doesn't add anything in the original list.

TLDR: If you are not sure what to use, use thread-based processing.

#### WorkerThread (`abllib.pproc.WorkerThread`)

This class represents a seperate thread that runs a given function until completion.
If .join() is called, the functions return value or any occured exception is returned.
If .join() is called with reraise=True, any caught exception will be reraised.

Example usage:

```py
>> from abllib.pproc import WorkerThread
>> def the_answer():
..     return 42
>> wt = WorkerThread(target=the_answer)
>> wt.start()
>> wt.join()
42
```

Exceptions that occur are caught and returned. The exception object can be reraised manually.

Optionally, if reraise is provided, any caught excpetion will be raised automatically.
```py
>> from abllib.pproc import WorkerThread
>> def not_the_answer():
..     raise ValueError("The answer is not yet calculated!")
>> wt = WorkerThread(target=not_the_answer)
>> wt.start()
>> wt.join()
ValueError('The answer is not yet calculated!')
>> isinstance(wt.join(), BaseException)
True
>> raise wt.join()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: The answer is not yet calculated!
>> wt.join(reraise=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: The answer is not yet calculated!
```

#### WorkerProcess (`abllib.pproc.WorkerProcess`)

This class represents a seperate process that runs a given function until completion.
If .join() is called, the functions return value or any occured exception is returned.
If .join() is called with reraise=True, any caught exception will be reraised.

Example usage:

```py
>> from abllib.pproc import WorkerProcess
>> def the_answer():
..     return 42
>> wp = WorkerProcess(target=the_answer)
>> wp.start()
>> wp.join()
42
```

Exceptions that occur are caught and returned. The exception object can be reraised manually.

Optionally, if reraise is provided, any caught excpetion will be raised automatically.
```py
>> from abllib.pproc import WorkerProcess
>> def not_the_answer():
..     raise ValueError("The answer is not yet calculated!")
>> wp = WorkerProcess(target=not_the_answer)
>> wp.start()
>> wp.join()
ValueError('The answer is not yet calculated!')
>> isinstance(wp.join(), BaseException)
True
>> raise wp.join()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: The answer is not yet calculated!
>> wp.join(reraise=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: The answer is not yet calculated!
```

### 8. Function wrappers (`abllib.wrapper`)

This module contains general-purpose [wrappers](https://www.geeksforgeeks.org/function-wrappers-in-python/) for functions.

#### Locking wrappers

There are two wrappers which help with multi-threading:
* ReadLock
* WriteLock

WriteLock works like a normal [lock](https://en.wikipedia.org/wiki/Lock_(computer_science)), while ReadLock works like a [semaphore](https://en.wikipedia.org/wiki/Semaphore_(programming)).

These wrappers can be given a name, and all wrappers with the same name function as the same instance.
If a wrapper is applied to a function, the lock is acquired before the function executes and is released afterwards.

Example usage:
```py
>> from time import sleep
>> from abllib.wrapper import WriteLock
>> @WriteLock("MyLockName")
.. def do_something(duration):
..     sleep(duration)
>> do_something(10) #this holds the "MyLockName"-lock for ten seconds
```

The default behaviour is to wait until the lock can be acquired. If a timeout parameter is provided, an LockAcquisitionTimeoutError is raised if the acquisition takes too long. The timeout is specified in seconds.
```py
>> from time import sleep
>> from abllib.wrapper import WriteLock
>> @WriteLock("MyLockName", timeout=5)
.. def do_something(duration):
..     sleep(duration)
>> WriteLock("MyLockName").acquire() #this holds the "MyLockName"-lock
>> do_something(10)

```

TODO: usage and global nature of lock names

## Installation

### PyPi

Not yet available

### Github

To install the latest version directly from Github, run the following command:
```bash
pip install git+https://github.com/Ableytner/abllib.git
```

This will automatically install all other dependencies.

### requirements.txt

If you want to include this library as a dependency in your requirements.txt, the syntax is as follows:
```text
abllib @ git+https://github.com/Ableytner/abllib@1.2.0
```
whereas 1.2.0 is the version that you want to install.
