"""The main module, used for dev testing"""

from abllib import log

# TODO:
# UP NEXT
# improve CustomException system by introducing a .with static method which does message substitution
# change fuzzy module to return a search object containing all relevant data
# add tests for fuzzy for a tuple of targets or remove tuple as valid target

# IMPORTANT BUT ANNOYING
# add function to _BaseStorage which deletes item and all empty subdicts (VolatileStorage.purge("key1.key2")),
# or make it the default behaviour
# add tests for threaded storage access
# document and understand levenshtein_distance
# make output of pylint test humanly readable

# TAKE A LOT OF TIME / NEEDED IN THE FUTURE
# add abllib.type module with verify function, which compares a value to a given type hint
# add a wrapper function for ensuring function parameter types, which uses abllib.type
# also check content type of lists / dicts on PersistentStorage __setitem__
# add async module with function to run async func in sync context

if __name__ == "__main__":
    log.initialize()
    log.add_console_handler()
#    log.add_file_handler()

    logger = log.get_logger()
    logger.info("this is a test")
    logger.warning("this is a warning!")
