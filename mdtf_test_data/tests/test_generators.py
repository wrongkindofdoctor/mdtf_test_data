import numpy as np

from mdtf_test_data.generators import generate_random_array
from mdtf_test_data.generators.normal import normal


def test_generate_random_array_normal():
    stats = [(5.0, 10.0), (50.0, 100.0)]
    generator_kwargs = {"stats": stats}
    result = generate_random_array(
        (20, 20), 5, generator=normal, generator_kwargs=generator_kwargs
    )
    assert result.shape == (5, 2, 20, 20)
    assert np.allclose(result.sum(), 104847.61)
    assert np.allclose(
        (result[:, 0, :, :].mean(), result[:, 0, :, :].std()), (5.2270184, 10.07385)
    )
    assert np.allclose(
        (result[:, 1, :, :].mean(), result[:, 1, :, :].std()), (47.196785, 98.86136)
    )
