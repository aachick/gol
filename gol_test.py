"""Very basic tests."""
import pytest

from gol import Universe


@pytest.fixture
def original_universe():
    """Return a small universe with a set random seed."""
    universe = Universe(5, 5, seed_of_life=1, threshold=0.5)
    return universe


def test_universe_representation(original_universe: Universe):
    """Test that the universe is represented correctly and consistently."""
    universe_str = str(original_universe)
    universe_repr = repr(original_universe)
    universe_display = original_universe.display()

    assert universe_str == " ██  \n ██  \n█ █  \n█ ██ \n ██  \n"
    assert universe_repr == universe_str
    assert "\n".join(universe_display) + "\n" == universe_str


def test_universe_tick(original_universe: Universe):
    """Test that the ticking function works correctly."""
    original_universe.tick()

    # Original cells should be:
    # [
    #   False, True, True, False, False,
    #   False, True, True, False, False,
    #   True, False, True, False, False,
    #   True, False, True, True, False,
    #   False, True, True, False, False,
    # ]

    # fmt: off
    expected_cells = [
        True, False, False, True, False,
        True, False, False, True, False,
        True, False, False, False, True,
        True, False, False, True, True,
        True, False, False, False, False,
    ]
    # fmt: on
    assert original_universe.cells == expected_cells
