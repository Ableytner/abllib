"""Module containing tests for the abllib.fuzzy module"""

# pylint: disable=protected-access

from abllib import fuzzy

def test_all():
    """Ensure that fuzzy.match_all works at all"""

    target = "fox"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    results = fuzzy.match_all(target, inputs)
    assert len(results) == 1
    assert results[0].value == "the quick brown fox"
    assert results[0].index == 1
    assert results[0].inner_index is None

    target = "the"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    results = fuzzy.match_all(target, inputs)
    assert len(results) == 2
    assert results[0].value == "the slow white rat"
    assert results[0].index == 0
    assert results[0].inner_index is None
    assert results[1].value == "the quick brown fox"
    assert results[1].index == 1
    assert results[1].inner_index is None

def test_all_fuzzy():
    """Ensure that fuzzy.match_all applies fuzzy logic"""

    target = "diferent"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert len(fuzzy.match_all(target, inputs, 0)) == 0
    assert len(fuzzy.match_all(target, inputs, 1)) == 1
    assert len(fuzzy.match_all(target, inputs, 8)) == 1

def test_all_tuple():
    """Ensure that fuzzy.match_all handles tuple candidates correctly"""

    target = "diferent"
    inputs = [
        ("the slow white rat", "this sentence is diferent"),
        ("the quick brown fox", "something else"),
        "different saying with many words"
    ]

    m = fuzzy.match_all(target, inputs)

    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert len(m) == 2
    assert m[0].value == ("the slow white rat", "this sentence is diferent")
    assert m[1].value == "different saying with many words"

def test_all_matchresult():
    """Ensure that fuzzy.match_all asigns correct values to MatchResult"""

    target = "diferent"
    inputs = [
        ("the slow white rat", "this sentence is diferent"),
        ("the quick brown fox", "something else"),
        "different saying with many words"
    ]

    m = fuzzy.match_all(target, inputs)

    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert len(m) == 2
    assert m[0].index == 0
    assert m[0].value == ("the slow white rat", "this sentence is diferent")
    assert m[0].inner_index == 1

def test_closest():
    """Ensure that fuzzy.match_closest works at all"""

    target = "fox"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    result = fuzzy.match_closest(target, inputs, 0)
    assert result.value == "the quick brown fox"
    assert result.index == 1
    assert result.inner_index is None

    target = "the"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    result = fuzzy.match_closest(target, inputs, 0)
    assert result.value == "the slow white rat"
    assert result.index == 0
    assert result.inner_index is None

def test_closest_fuzzy():
    """Ensure that fuzzy.match_closest applies fuzzy logic"""

    target = "diferent"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match_closest(target, inputs, 0).value is None
    assert fuzzy.match_closest(target, inputs, 1).value == "different saying with many words"
    assert fuzzy.match_closest(target, inputs, 8).value == "different saying with many words"

    target = "diferent wth wors"
    inputs = ["the slow white rat", "the quick brown fox", "different saying with many words"]

    assert fuzzy.match_closest(target, inputs, 0).value is None
    assert fuzzy.match_closest(target, inputs, 1).value == "different saying with many words"
    assert fuzzy.match_closest(target, inputs, 8).value == "different saying with many words"

def test_closest_tuple():
    """Ensure that fuzzy.match_closest handles candidate tuples correctly"""

    target = "diferent"
    inputs = [
        ("the slow white rat", "this sentence is diferent"),
        ("the quick brown fox", "something else"),
        "different saying with many words"
    ]

    m = fuzzy.match_closest(target, inputs)

    assert m.value == ("the slow white rat", "this sentence is diferent")
    assert m.score == 0.25

def test_closest_matchresult():
    """Ensure that fuzzy.match_closest asigns correct values to MatchResult"""

    target = "diferent"
    inputs = [
        ("the slow white rat", "this sentence is diferent"),
        ("the quick brown fox", "something else"),
        "different saying with many words"
    ]

    m = fuzzy.match_closest(target, inputs)

    # pylint: disable-next=use-implicit-booleaness-not-comparison
    assert m.index == 0
    assert m.value == ("the slow white rat", "this sentence is diferent")
    assert m.inner_index == 1

def test_similarity():
    """Ensure that the similarity calculation works as expected"""

    similarity = fuzzy._similarity.similarity_v2
    assert callable(similarity)

    assert similarity("fox", "the quick fox", 5) == 0.33
    assert similarity("foy", "the quick fox", 5) == 0.22

    # only allow for an edit_distance of up to len(word) // 3
    assert similarity("hay", "the quick fox", 5) == 0.0
