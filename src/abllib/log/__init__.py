"""A module containing the logger creation"""

from abllib.log._ablapi_handler import add_ablapi_handler as add_ablapi_handler
from abllib.log._default_handlers import add_console_handler as add_console_handler
from abllib.log._default_handlers import add_file_handler as add_file_handler
from abllib.log._helpers import DEFAULT_LOG_LEVEL as DEFAULT_LOG_LEVEL
from abllib.log._helpers import get_loglevel as get_loglevel
from abllib.log._helpers import get_loglevel_fast as get_loglevel_fast
from abllib.log._helpers import get_logger as get_logger
from abllib.log._helpers import initialize as initialize
from abllib.log._log_level import LogLevel as LogLevel

__exports__ = [
    LogLevel,
    initialize,
    add_ablapi_handler,
    add_console_handler,
    add_file_handler,
    get_logger,
    get_loglevel,
    get_loglevel_fast,
    DEFAULT_LOG_LEVEL,
]
