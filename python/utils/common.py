# Import modules
import carla
import numpy

import logging
import random
import time


def modify_transform(
    transform: carla.Transform,
    position_offset: carla.Vector3D,
    orientation_offset: carla.Rotation
) -> carla.Transform:
    '''
    Translates and rotates the provided Carla Transform by the position offset
    and orientation offset, respectively.

    Parameters
    ----------
    transform : carla.Transform
        The Carla Transform to be modified.
    position_offset : carla.Vector3D
        The direction in which to translate the transform.
    orientation_offset : carla.Rotation
        The orientation in which to rotate the transform.

    Returns
    -------
    carla.Transform
        The modified transform.
    '''
    new_pitch = transform.rotation.pitch + orientation_offset.pitch
    new_yaw = transform.rotation.yaw + orientation_offset.yaw
    new_roll = transform.rotation.roll + orientation_offset.roll
    orientation = carla.Rotation(pitch=new_pitch, yaw=new_yaw, roll=new_roll)
    transform = translate(transform, position_offset)

    return carla.Transform(transform.location, orientation)


def np_array_to_vector2D(array: numpy.array) -> carla.Vector2D:
    '''
    Converts a numpy array to a Carla 2D Vector.

    Parameters
    ----------
    array : numpy.array
        A 1x2 numpy array containing data to convert to a Carla.Vector2D.

    Returns
    -------
    carla.Vector2D
        A 2D Carla Vector that represents the provided numpy array.
    '''
    return carla.Vector2D(array[0], array[1])


def np_array_to_vector3D(array: numpy.array) -> carla.Vector3D:
    '''
    Converts a numpy array to a Carla 3D Vector.

    Parameters
    ----------
    array : numpy.array
        A 1x3 numpy array containing data to convert to a Carla.Vector3D.

    Returns
    -------
    carla.Vector3D
        A 3D Carla Vector that represents the provided numpy array.
    '''
    return carla.Vector3D(array[0], array[1], array[2])


def translate(
    transform: carla.Transform,
    offset: carla.Vector3D
) -> carla.Transform:
    '''
    Translates the provided Carla Transform by the offset.

    Parameters
    ----------
    transform : carla.Transform
        The Carla Transform to be modified.
    offset : carla.Vector3D
        The direction in which to translate the transform.

    Returns
    -------
    carla.Transform
        The transform translated by the offset.
    '''
    return carla.Transform(transform.location + offset, transform.rotation)


def sleep_random_time(start: float = 2.0, end: float = 6.0) -> None:
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
