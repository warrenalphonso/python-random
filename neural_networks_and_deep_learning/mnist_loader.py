"""
A library to laod the MNIST image data. We usually use `load_data_wrapper`. 
"""
import pickle 
import gzip 
import numpy as np 

def load_data():
    """
    Return the MNIST data as a tuple with training, validiation, and test data. 

    `training_data` is a two-tuple. The first element is an numpy ndarray with 
    50_000 elements, where each element is a numpy ndarray with 784 values, 
    representing the pixels in a single MNIST image. 
    The second element is a numpy ndarray with the digit values (0...9) of each 
    sample. 

    The `validation_data` and `test_data` are similar, except each contains only 
    10_000 images. 
    """
    with gzip.open("mnist.pkl.gz", "rb") as f:
        training_data, validation_data, test_data = map(list, 
                pickle.load(f, encoding="latin1"))
    return (training_data, validation_data, test_data)

def load_data_wrapper():
    """
    Return the MNIST data as a tuple with training, validiation, and test data. 
    We're using `load_data` but changing `training_data` so that each sample is 
    (x, y) where we change y to be a 10-dimensional ndarray representing a 
    *unit vector* corresponding to the correct digit for x. 
    `validation_data` and `test_data` stay the same, so we're using slightly 
    different formats for these two compared to `training_data`. 
    We're also slighly modifying the x values for all sets so that they're 
    (784, 1) instead of (784,). 
    """
    tr_d, va_d, te_d = load_data()
    training_inputs = [np.reshape(x, (784, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = zip(training_inputs, training_results)
    validation_inputs = [np.reshape(x, (784, 1)) for x in va_d[0]]
    validation_data = zip(validation_inputs, va_d[1])
    test_inputs = [np.reshape(x, (784, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return map(list, [training_data, validation_data, test_data])

def vectorized_result(j):
    e = np.zeros((10, 1))
    e[j] = 1. 
    return e 
