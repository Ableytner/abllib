"""The main module, used for dev testing"""

# TODO:
# UP NEXT
# supply package number manually to release workflow
# add Storage.get(key, default) function

# IMPORTANT BUT ANNOYING
# add tests for threaded storage access
# document and understand levenshtein_distance
# document fuzzy score calculation
# optimize _lock_wrapper._log_callstack (takes half of the runtime when assigning storage item)

# TAKES A LOT OF TIME / NEEDED IN THE FUTURE
# add abllib.type module with verify function, which compares a value to a given type hint
# add an enforce_types wrapper for ensuring function parameter types, which internally uses abllib.type
# go throught all TODO comments and add type validation if necessary
# add async module with function to run async func in sync context

# pylint: skip-file

if __name__ == "__main__":
    pass
