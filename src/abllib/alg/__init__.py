"""A module containing general-purpose algorithms"""

from abllib.general import try_import_module

Levenshtein = try_import_module("Levenshtein")

if Levenshtein is None:
    from ._levenshtein import levenshtein_distance
else:
    # use C implementation
    levenshtein_distance = Levenshtein.distance

__exports__ = [
    levenshtein_distance
]
