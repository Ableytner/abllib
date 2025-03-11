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

os.environ["DEBUG"] = "True"

# pylint: disable-next=unused-import
from .fixtures import setup, clean_after_function
