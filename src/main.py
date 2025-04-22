"""The main module, used for dev testing"""

# TODO:
# UP NEXT

# IMPORTANT BUT ANNOYING
# add tests for threaded storage access
# document and understand levenshtein_distance
# document fuzzy score calculation

# TAKES A LOT OF TIME / NEEDED IN THE FUTURE
# add abllib.type module with verify function, which compares a value to a given type hint
# add a enforce_types wrapper for ensuring function parameter types, which internally uses abllib.type
# go throught all TODO comments and add type validation if necessary
# add async module with function to run async func in sync context

if __name__ == "__main__":
    import traceback
    traces = traceback.format_list(traceback.extract_stack())
    traces.reverse()
    for line in traces:
        print(line)
