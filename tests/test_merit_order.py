import pytest

from market.merit_order import clear_market

CAP = [20, 10, 15, 20, 5]
OFFERS = [0, 10, 50, 80, 150]
CAP_CAP = 250


@pytest.mark.parametrize(
    "demand, price, dispatched, unserved",
    [
        (0,   0,   [0, 0, 0, 0, 0],      0),
        (20,  0,   [20, 0, 0, 0, 0],     0),
        (21,  10,  [20, 1, 0, 0, 0],     0),
        (45,  50,  [20, 10, 15, 0, 0],   0),
        (46,  80,  [20, 10, 15, 1, 0],   0),
        (70,  150, [20, 10, 15, 20, 5],  0),
        (71,  250, [20, 10, 15, 20, 5],  1),
        (100, 250, [20, 10, 15, 20, 5],  30),
    ],
)
def test_clear_market(demand, price, dispatched, unserved):
    result = clear_market(CAP, OFFERS, demand, CAP_CAP)
    assert result["price"] == pytest.approx(price)
    assert list(result["dispatched"]) == pytest.approx(dispatched)
    assert result["unserved"] == pytest.approx(unserved)


def test_dispatched_plus_unserved_equals_demand():
    for demand in range(0, 101):
        result = clear_market(CAP, OFFERS, demand, CAP_CAP)
        assert sum(result["dispatched"]) + result["unserved"] == pytest.approx(demand)


def test_unsorted_input_gives_same_logic():
    cap = [20, 20, 5, 15, 10]
    offers = [80, 0, 150, 50, 10]
    result = clear_market(cap, offers, 46, CAP_CAP)
    assert result["price"] == pytest.approx(80)
    assert list(result["dispatched"]) == pytest.approx([1, 20, 0, 15, 10])
    assert result["marginal_index"] == 0


def test_marginal_index_none_when_shortage():
    result = clear_market(CAP, OFFERS, 80, CAP_CAP)
    assert result["marginal_index"] is None


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        clear_market([10, 20], [5], 10, CAP_CAP)
    with pytest.raises(ValueError):
        clear_market(CAP, OFFERS, -1, CAP_CAP)