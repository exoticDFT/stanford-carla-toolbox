import carla

import logging


def create(
    host='127.0.0.1',
    port=2000,
    timeout=3.0,
    map_name='/Game/Carla/Maps/Town03',
    force_reset=False
):
    '''
    Creates a Carla client to be used in a Carla runtime script.

    Parameters
    ----------
    host : str, optional
        The string containing the host address.
    port : int, optional
        The port in which the client will connect.
    timeout : float, optional
        The time in which to wait for a response from the server.
    map_name : carla.Map, optional
        The Carla map that you would like the world to load.
    force_reset : Boolean, optional
        The decision to reset the whole world on initialization.

    Returns
    -------
    carla.Client
        A Carla client that is connected to the provided server.
    '''
    client = carla.Client(host, port)
    client.set_timeout(timeout)
    world = client.get_world()

    if world.get_map().name != map_name or force_reset:
        client.load_world(map_name)

    return client


def destroy_actors_in_list(client, actor_list):
    '''
    Destroys (removes) the list of actors from Carla server in which  the client
    is connected.

    Parameters
    ----------
    client : carla.Client
        The Carla client that is connected to the Carla server in which to
        remove the actors.
    actor_list : List
        The list of actors that should be destroyed.
    '''
    logging.info('Destroying {} actors'.format(len(actor_list)))
    client.apply_batch([carla.command.DestroyActor(x) for x in actor_list])


def start_recording(
    client: carla.Client,
    filename: str
):
    '''
    Starts the Carla recording functionality for the Carla server.

    Parameters
    ----------
    client : carla.Client
        The Carla client connected to the Carla server to record.
    filename : str
        The name of the file the recording will be saved. This can be a full
        path to the file or just a file name. If the latter is used, the
        recording will be saved to the default location Carla uses.
    '''
    logging.info(
        'This scenario is being recorded as {}'.format(
            filename
        )
    )
    client.start_recorder(filename)


def stop_recording(client: carla.Client):
    '''
    Stops the recording of the Carla server.

    Parameters
    ----------
    client : carla.Client
        The Carla client connected to the Carla server to stop recording.
    '''
    logging.info(
        'The scenario is no longer recording.'
    )
    client.stop_recorder()
