# Import
from omnitools import dot_convolve
from numpy import array, ndarray
from numpy.random import normal


# Variables


# Test classes and functions
def test_dot_convolve() -> None:
    loc: float = 0.0
    scale: float = 1.0
    size: int = 100
    data: ndarray = normal(loc, scale, size)
    window_functions: ndarray = array([0, 1, 2, 1, 0])
    data_smoothed = dot_convolve(data, window_functions)

    assert abs((sum(data) - sum(data_smoothed)) / sum(data)) < 0.05, "dot_convolve does not conserve area!"


def main() -> None:
    pass


if __name__ == "__main__":
    main()