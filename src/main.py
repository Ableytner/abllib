"""The main module, used for dev testing"""

# TODO:
# UP NEXT

# IMPORTANT BUT ANNOYING
# add tests for threaded storage access
# document levenshtein_distance
# document fuzzy score calculation
# optimize _lock_wrapper._log_callstack (takes half of the runtime when assigning storage item)
# better implement functools.update_wrapper for Deprecated class

# TAKES A LOT OF TIME / NEEDED IN THE FUTURE
# construct target type-specific function at runtime in types.enforce

# pylint: skip-file

if __name__ == "__main__":
    from time import perf_counter_ns

    from abllib import VolatileStorage, log

    VolatileStorage.initialize()

    start = perf_counter_ns()
    for c in range(100000):
        VolatileStorage[str(c)] = "test"
    end = perf_counter_ns() - start
    print(end)
