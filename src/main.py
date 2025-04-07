"""The main module, used for dev testing"""

from abllib import log

# TODO:
# UP NEXT
# document new fuzzy module changes
# make output of pylint test humanly readable

# IMPORTANT BUT ANNOYING
# convert similarity algorithm to be non-recursive / more performant
# add function to _BaseStorage which deletes item and all empty subdicts (VolatileStorage.purge("key1.key2")),
# or make it the default behaviour
# add tests for threaded storage access
# document and understand levenshtein_distance

# TAKES A LOT OF TIME / NEEDED IN THE FUTURE
# add abllib.type module with verify function, which compares a value to a given type hint
# add a wrapper function for ensuring function parameter types, which uses abllib.type
# also check content type of lists / dicts on PersistentStorage.__setitem__
# add async module with function to run async func in sync context

if __name__ == "__main__":
    log.initialize()
    log.add_console_handler()
    logger = log.get_logger()
