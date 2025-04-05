"""The main module, used for dev testing"""

from time import perf_counter_ns

from abllib import log
from abllib.fuzzy._similarity import similarity

# TODO:
# UP NEXT
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

# old:
# 2x2   ->     0.94 ms
# 3x3   ->     1.18 ms
# 10x10 -> 41563.12 ms

# new v1:
# 2x2   ->     1.16 ms
# 3x3   ->     1.45 ms
# 10x10 -> 27174.57 ms

if __name__ == "__main__":
    log.initialize()
    log.add_console_handler()
    logger = log.get_logger()

    start = perf_counter_ns()
    sim = similarity("sentence sentence", "sentence candidate", 5)
    logger.info(f"result {sim} completed in {(perf_counter_ns() - start) // 1000 / 1000} ms") # score should be 0.5

    start = perf_counter_ns()
    sim = similarity("sentence sentence sentence", "sentence candidate candidate", 5)
    logger.info(f"result {sim} completed in {(perf_counter_ns() - start) // 1000 / 1000} ms") # score should be 0.33

    start = perf_counter_ns()
    sim = similarity("fox", "the quick fox", 5)
    logger.info(f"result {sim} completed in {(perf_counter_ns() - start) // 1000 / 1000} ms") # score should be 0.33

    start = perf_counter_ns()
    sim = similarity("sentence sen ntence", "sentence sentence candidate", 5)
    logger.info(f"result {sim} completed in {(perf_counter_ns() - start) // 1000 / 1000} ms") # score should be 0.58

    start = perf_counter_ns()
    sim = similarity("this is a pretty pretty long target", "a long pretty sentence is given as", 5)
    logger.info(f"result {sim} completed in {(perf_counter_ns() - start) // 1000 / 1000} ms") # score should be 0.57

    start = perf_counter_ns()
    sim = similarity("this is a pretty pretty long target sentence sentence sentence",
                     "a long pretty sentence is given as a candidate candidate",
                     5)
    logger.info(f"result {sim} completed in {(perf_counter_ns() - start) // 1000 / 1000} ms") # score should be 0.5
