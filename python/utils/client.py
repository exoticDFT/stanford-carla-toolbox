import carla


def create(
    host='127.0.0.1',
    port=2000,
    timeout=3.0,
    map_name='/Game/Carla/Maps/Town03'
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
    map_name : carla.Map
        The Carla map that you would like the world to load.

    Returns
    -------
    carla.Client
        A Carla client that is connected to the provided server.
    '''
    client = carla.Client(host, port)
    client.set_timeout(timeout)
    world = client.get_world()

    if world.get_map().name != map_name:
        client.load_world(map_name)

    return client
