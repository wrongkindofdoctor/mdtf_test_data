import numpy as np

from mdtf_test_data.random import generate_random_array


def test_generate_random_array():
    result = generate_random_array((20, 20), 5, [(5.0, 10.0), (50.0, 100.0)])
    assert result.shape == (5, 2, 20, 20)
    assert np.allclose(result.sum(), 104847.61)
    assert np.allclose(
        (result[:, 0, :, :].mean(), result[:, 0, :, :].std()), (5.2270184, 10.07385)
    )
    assert np.allclose(
        (result[:, 1, :, :].mean(), result[:, 1, :, :].std()), (47.196785, 98.86136)
    )
