from edgetools import dot_convolve

def test_dot_convolve():
    data = ...
    window_functions = ...
    data_smoothed = dot_convolve(data, window_functions)

    assert sum(data), sum(data_smoothed), "dot_convolve does not conserve area!"