"""The main module, used for dev testing"""

from abllib import log

# TODO:
# add lock for threaded Storage access
# add Overview section in README
# add tests for fs module
# prefix internal module files with an underscore

if __name__ == "__main__":
    log.initialize()
    log.add_console_handler()
#    log.add_file_handler()

    logger = log.get_logger()
    logger.info("this is a test")
    logger.warning("this is a warning!")
