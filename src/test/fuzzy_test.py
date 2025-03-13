"""Module containing tests for the abllib.fuzzy module"""

# pylint: disable=protected-access, missing-class-docstring, pointless-statement, expression-not-assigned

from abllib import fuzzy

def test_search():
    """Ensure that fuzzy.search works as expected"""

    target = "fox"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    for threshold in range(10):
        assert fuzzy.search(target, inputs, threshold) == [1], f"Error at threshold {threshold}"

    target = "the"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    for threshold in range(10):
        assert fuzzy.search(target, inputs, threshold) == [0, 1], f"Error at threshold {threshold}"

    target = "diferent"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    for threshold in range(3):
        # pylint: disable-next=use-implicit-booleaness-not-comparison
        assert fuzzy.search(target, inputs, threshold) == [], f"Error at threshold {threshold}"
    for threshold in range(3, 10):
        assert fuzzy.search(target, inputs, threshold) == [2], f"Error at threshold {threshold}"

def test_match():
    """Ensure that fuzzy.match works as expected"""

    target = "fox"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match(target, inputs, 0) == (1, 1.0)

    target = "the"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match(target, inputs, 0) == (0, 1.0)

    target = "diferent"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match(target, inputs, 0) == (None, 0.0)
    assert fuzzy.match(target, inputs, 1) == (None, 0.0)
    assert fuzzy.match(target, inputs, 2) == (None, 0.0)
    assert fuzzy.match(target, inputs, 3) == (2, 0.1)

    target = "diferent wth wors"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match(target, inputs, 0) == (None, 0.0)
    assert fuzzy.match(target, inputs, 1) == (None, 0.0)
    assert fuzzy.match(target, inputs, 2) == (None, 0.0)
    assert fuzzy.match(target, inputs, 3) == (2, 0.3)
