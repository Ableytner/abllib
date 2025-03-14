"""Module containing tests for the abllib.fuzzy module"""

# pylint: disable=protected-access, missing-class-docstring, pointless-statement, expression-not-assigned

from abllib import fuzzy

def test_search():
    """Ensure that fuzzy.search works as expected"""

    target = "fox"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.search(target, inputs) == [1]

    target = "the"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.search(target, inputs) == [0, 1]

    target = "diferent"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert fuzzy.search(target, inputs, 0) == []
    assert fuzzy.search(target, inputs, 1) == [2]
    assert fuzzy.search(target, inputs) == [2]

def test_match():
    """Ensure that fuzzy.match works as expected"""

    target = "fox"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match(target, inputs, 0) == (1, 0.25)

    target = "the"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match(target, inputs, 0) == (0, 0.25)

    target = "diferent"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match(target, inputs, 0) == (None, 0.0)
    assert fuzzy.match(target, inputs, 1) == (2, 0.19)
    assert fuzzy.match(target, inputs, 2) == (2, 0.19)

    target = "diferent wth wors"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match(target, inputs, 0) == (None, 0.0)
    assert fuzzy.match(target, inputs, 1) == (2, 0.57)
    assert fuzzy.match(target, inputs, 2) == (2, 0.57)

def test_similarity():
    """Ensure that the similarity calculation works as expected"""

    similarity = fuzzy._similarity.similarity
    assert callable(similarity)

    assert similarity("fox", "the quick fox", 5) == 0.33
    assert similarity("foy", "the quick fox", 5) == 0.32

    # only allow for an edit_distance up to len(word) // 3
    assert similarity("fay", "the quick fox", 5) == 0.0
