# Import modules
import carla
import numpy

import logging
import random
import time


# modules
def np_array_to_vector2D(array):
    '''
    Converts a numpy array to a Carla 2D Vector.

    Parameters
    ----------
    array : numpy.array
        A 1x2 numpy array containing data to convert to a Carla.Vector2D
    '''
    vector = carla.Vector2D(array[0], array[1])

    return vector

    
def array_to_vector3D(array):
    '''
    Converts a numpy array to a Carla 3D Vector.

    Parameters
    ----------
    array : numpy.array
        A 1x3 numpy array containing data to convert to a Carla.Vector3D
    '''
    vector = carla.Vector3D(array[0], array[1], array[2])

    return vector


def sleep_random_time(start=2.0, end=6.0):
    '''
    Sleeps the thread for some random time between the provided range.

    Parameters:
    start : float
        The minimum time in which to sleep.
    end : float
        The maximum time in which to sleep.
    '''
    sleep_time = random.uniform(start, end)

    logging.info('Sleeping for {} seconds.'.format(sleep_time))

    time.sleep(sleep_time)
