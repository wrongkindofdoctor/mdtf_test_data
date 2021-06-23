import numpy as np


def generate_random_array(xyshape, ntimes, stats, dtype="float32"):
    """Generates an array of sample data chosen from a normal distribution

    Parameters
    ----------
    stats : tuple or list of tuples
        Array statistics in the format of [(mean,stddev)]
    xyshape : tuple
        Tuple of desired array shape

    Returns
    -------
    np.ndarray
        Array of random data
    """
    stats = [stats] if not isinstance(stats, list) else stats

    data = []
    for time in range(ntimes):
        np.random.seed(time)
        data.append(np.array([np.random.normal(x[0], x[1], xyshape) for x in stats]))

    return np.array(data).astype(dtype)
