"""The main module, used for dev testing"""

from abllib import log

# TODO:
# add abllib.type module with verify function, which compares a value to a given type hint
# add Overview section in README
# add tests for fs module
# add tests for threaded storage access
# add async module
# improve CustomException system by introducing a Msg() class and enabling message substitution
# change fuzzy module to return a search object containing all relevant data
# document and understand levenshtein_distance
# add pop() function to storages
# fix del VolatileStorage["key1.key2"] only deleting key2 (also check that key1 is empty before deleting)
# add NotInitializedError and use it in storages
# also check content type of lists / dicts on PersistentStorage __setitem__
# add tests for fuzzy for a tuple of targets
# rename ThreadWithReturnValue to WorkerThread and add documentation / tests

if __name__ == "__main__":
    log.initialize()
    log.add_console_handler()
#    log.add_file_handler()

    logger = log.get_logger()
    logger.info("this is a test")
    logger.warning("this is a warning!")
