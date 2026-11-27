
import numpy as np

from src.knapsack import (
    Instance,
    read_instance,
    total_weight,
    gain,
    is_feasible,
    repair,
    random_solution,
    starting_solutions,
)


def create_instance():
    return Instance(
        name="test",
        n=3,
        c=7,
        p=np.array([10, 8, 4]),
        w=np.array([5, 4, 3]),
    )


def test_read_instance(tmp_path):
    file = tmp_path / "test.kp"
    file.write_text("3\n7\n10 5\n8 4\n4 3\n")

    inst = read_instance(file)

    assert inst.n == 3
    assert inst.c == 7
    assert np.array_equal(inst.p, [10, 8, 4])
    assert np.array_equal(inst.w, [5, 4, 3])


def test_total_weight():
    inst = create_instance()
    x = np.array([1, 0, 1], dtype=np.int8)

    assert total_weight(inst, x) == 8


def test_gain():
    inst = create_instance()
    x = np.array([1, 0, 1], dtype=np.int8)

    assert gain(inst, x) == 14


def test_is_feasible():
    inst = create_instance()

    assert is_feasible(inst, np.array([1, 0, 0], dtype=np.int8))
    assert not is_feasible(inst, np.array([1, 1, 0], dtype=np.int8))


def test_repair():
    inst = create_instance()
    x = np.ones(inst.n, dtype=np.int8)
    original = x.copy()

    repaired = repair(inst, x)

    assert is_feasible(inst, repaired)
    assert np.array_equal(x, original)
    assert repaired.dtype == np.int8


def test_random_solution():
    inst = create_instance()
    rng = np.random.default_rng(42)

    x = random_solution(inst, rng)

    assert x.shape == (inst.n,)
    assert x.dtype == np.int8
    assert is_feasible(inst, x)


def test_starting_solutions():
    inst = create_instance()

    solutions = starting_solutions(inst, 5, 42)

    assert len(solutions) == 5
    assert all(is_feasible(inst, x) for x in solutions)
    assert all(x.dtype == np.int8 for x in solutions)


def test_starting_solutions_reproducibility():
    inst = create_instance()

    solutions1 = starting_solutions(inst, 5, 42)
    solutions2 = starting_solutions(inst, 5, 42)

    for x1, x2 in zip(solutions1, solutions2):
        assert np.array_equal(x1, x2)
