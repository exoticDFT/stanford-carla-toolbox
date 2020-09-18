import carla

import logging


def create(
    host: str = '127.0.0.1',
    port: int = 2000,
    timeout: float = 3.0,
    map_name: str = '/Game/Carla/Maps/Town03',
    force_reset: bool = False
) -> carla.Client:
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
    map_name : str, optional
        The Carla map that you would like the world to load.
    force_reset : bool, optional
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


def destroy_actors_in_list(client: carla.Client, actor_list: list) -> None:
    '''
    Destroys (removes) the list of actors from Carla server in which  the
    client is connected.

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


def load_xodr_world(
    client: carla.Client,
    filename: str,
    **args: dict
) -> None:
    '''
    Load a standalone OpenDrive file into the Carla server.

    Parameters
    ----------
    client : carla.Client
        The Carla client that will load the OpenDrive file into the server.
    filename : str
        The name of the file that will be loaded by Carla.
    '''
    try:
        logging.info('Loading OpenDrive file: {}'.format(filename))
        f = open(filename, "r")
        odr_string = f.read()
        f.close()
    except FileNotFoundError:
        logging.error('Could not find file: {}'.format(filename))

    params = carla.OpendriveGenerationParameters()

    if "vertex_distance" in args:
        params.vertex_distance = args.get("vertex_distance")

    if "max_road_length" in args:
        params.max_road_length = args.get("max_road_length")

    if "wall_height" in args:
        params.wall_height = args.get("wall_height")

    if "additional_width" in args:
        params.additional_width = args.get("additional_width")

    if "smooth_junctions" in args:
        params.smooth_junctions = args.get("smooth_junctions")

    if "enable_mesh_visibility" in args:
        params.enable_mesh_visibility = args.get("enable_mesh_visibility")

    if "enable_pedestrian_navigation" in args:
        params.enable_pedestrian_navigation = args.get(
            "enable_pedestrian_navigation"
        )

    client.generate_opendrive_world(odr_string, params)


def start_recording(
    client: carla.Client,
    filename: str
) -> None:
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
    logging.info('This scenario is being recorded as {}'.format(filename))
    client.start_recorder(filename)


def stop_recording(client: carla.Client) -> None:
    '''
    Stops the recording of the Carla server.

    Parameters
    ----------
    client : carla.Client
        The Carla client connected to the Carla server to stop recording.
    '''
    logging.info('The scenario is no longer recording.')
    client.stop_recorder()
