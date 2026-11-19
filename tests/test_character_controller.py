import pytest

from gameplay import character_controller as mod

CASES = [
    pytest.param('move', ((0, 0, 0), (1, 0, 0), (0, 1, 0), 0.3, 45.0), ((1, 0, 0), True), False, id='01_move_flat'),
    pytest.param('move', ((0, 0, 0), (1, 0.2, 0), (0, 1, 0), 0.3, 45.0), ((1, 0.2, 0), True), True, id='02_move_step'),
    pytest.param('move', ((0, 0, 0), (1, 0.5, 0), (0, 1, 0), 0.3, 45.0), ((1, 0.0, 0), True), True, id='03_move_high_step'),
    pytest.param('move', ((0, 0, 0), (1, 0, 0), (0, 0.707, 0.707), 0.3, 45.0), ((1, 0, 0), False), False, id='04_move_slope_ok'),
    pytest.param('move', ((0, 0, 0), (1, 0, 0), (0, 0.5, 0.866), 0.3, 30.0), ((1, 0, 0), False), False, id='05_move_slope_steep'),
    pytest.param('coyote', (10.0, 10.1, 0.15), True, False, id='06_coyote_inside'),
    pytest.param('coyote', (10.0, 10.15, 0.15), False, False, id='07_coyote_edge'),
    pytest.param('coyote', (10.0, 10.2, 0.15), False, False, id='08_coyote_outside'),
    pytest.param('coyote', (10.0, 10.0, 0.0), True, False, id='09_coyote_zero'),
    pytest.param('coyote', (10.0, 9.9, 0.15), True, False, id='10_coyote_negative'),
    pytest.param('resolve_penetration', ((0, 0, 0), (1, 0, 0), 0.5), (0.5, 0.0, 0.0), True, id='11_penetrate_x'),
    pytest.param('resolve_penetration', ((0, 0, 0), (0, 1, 0), 0.2), (0.0, 0.2, 0.0), True, id='12_penetrate_y'),
    pytest.param('resolve_penetration', ((1, 1, 1), (0.707, 0.707, 0), 0.1), (1.0707, 1.0707, 1.0), True, id='13_penetrate_diag'),
    pytest.param('resolve_penetration', ((1, 2, 3), (0, 1, 0), 0.0), (1.0, 2.0, 3.0), True, id='14_penetrate_zero'),
    pytest.param('resolve_penetration', ((0, 0, 0), (0, 0, 1), -0.5), (0.0, 0.0, -0.5), True, id='15_penetrate_negative'),
]


def assert_close(actual, expected):
    if isinstance(expected, tuple):
        assert isinstance(actual, tuple) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            assert_close(actual[key], expected[key])
    else:
        assert actual == pytest.approx(expected)


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_character_controller_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert_close(result, expected)
    else:
        assert result == expected
