from services.screening import rank_candidates


def test_rank_candidates():
    assert rank_candidates("Python and SQL") == 20
