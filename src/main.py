"""The main module, used for dev testing"""

from abllib import log

# TODO:
# add abllib.type module with verify function, which compares a value to a given type hint
# add wrapper.ReadLock and wrapper.WriteLock classes
# use lock for threaded Storage access
# add Overview section in README
# add tests for fs module
# add async module

if __name__ == "__main__":
    log.initialize()
    log.add_console_handler()
#    log.add_file_handler()

    logger = log.get_logger()
    logger.info("this is a test")
    logger.warning("this is a warning!")
