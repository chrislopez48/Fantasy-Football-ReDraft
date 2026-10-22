import pytest

from backend.lambda_ranker.scoring import compute_fantasy_points

def test_qb_scoring():
    player= {
        "pass_yd": 100, "pass_td": 2, "interceptions": 1
    }

    rules = {
        "pass_yd": .04, "pass_td": 4, "interception": -2
    }

    total, breakdown = compute_fantasy_points(player, rules)

    assert total == pytest.approx(10.0)   
    assert breakdown["pass_td"] == 8.0
    assert breakdown["interceptions"] == -2.0