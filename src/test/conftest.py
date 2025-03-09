"""
    Pytest configuration
"""

# pylint: disable=unused-wildcard-import, wildcard-import, wrong-import-position, wrong-import-order, protected-access

# Adding source path to sys path
import pathlib
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../'))
sys.path.append(f"{pathlib.Path(__file__).parent.parent}")
sys.path.append(f"{pathlib.Path(__file__).parent}")

# pylint: enable=wrong-import-position, wrong-import-order

import shutil

from abllib import log, fs

os.environ["DEBUG"] = "True"

#  setup logging
log.initialize(log.LogLevel.DEBUG)
log.add_console_handler()
log.add_file_handler("test.log")

STORAGE_DIR = fs.absolute(os.path.dirname(__file__), "..", "..", "test_run")

# setup testing dirs
shutil.rmtree(STORAGE_DIR, ignore_errors=True)
os.makedirs(STORAGE_DIR, exist_ok=True)

# pylint: disable-next=unused-import
from .fixtures import setup_storages
