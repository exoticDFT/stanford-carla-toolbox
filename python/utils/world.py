import python.utils.actor

import carla


def destroy_all_dynamic_actors(world: carla.World) -> None:
    '''
    Removes all the dynamic actors in the Carla World.

    Parameters
    ----------
    world : carla.World
        The Carla world in which to remove the actors
    '''
    actor_types = ['sensor', 'vehicle', 'walker',]

    for actor in world.get_actors():
        if any(sub in actor.type_id for sub in actor_types):
            actor.destroy()


def draw_spawn_points(world: carla.World, timeout: float = -1.0) -> None:
    '''
    Draws all the available spawn points in the current Carla world.

    Parameters
    ----------
    world : carla.World
        The Carla world in which to draw the spawn point indices.
    timeout : float, optional
        The total number of seconds in which to keep the labels in the 
        environment. (Default is -1.0, which leaves the label in the 
        environment indefinitely.)
    '''
    map = world.get_map()
    spawn_points = map.get_spawn_points()

    for num, spawn_point in enumerate(spawn_points):
        world.debug.draw_string(
            spawn_point.location,
            str(num),
            life_time=timeout
        )


def move_spectator(
    world: carla.World,
    location: carla.Location = None,
    rotation: carla.Rotation = None,
    transform: carla.Transform = carla.Transform(
        carla.Location(0.0, 0.0, 20.0),
        carla.Rotation(-90.0, 0.0, 0.0)
    )
) -> None:
    '''
    Moves the main camera in the server, also known as the spectator.
    
    Either provide the location and rotation directly, or a transform. If both
    are provided, the location and rotation parameters will override the
    transform parameter.

    Parameters
    ----------
    world : carla.World
        The Carla World of the spectator that will be moved.
    location : carla.Location, optional
        The location to move the camera, by default None
    rotation : carla.Rotation, optional
        The orientation of the camera, by default None
    transform : carla.Transform, optional
        The transform (location and rotation) of the camera, by default 20
        meters above the world origin facing straight down.
    '''
    if location and rotation:
        transform = carla.Transform(location, rotation)

    spectator = world.get_spectator()
    spectator.set_transform(transform)


def remove_distant_actors(
    world: carla.World,
    location: carla.Location = carla.Location(0, 0, 0),
    max_distance: float = 100.0,
    actor_filter: str = 'vehicle.*',
    verbose: bool = False
) -> None:
    '''
    Removes actors from the Carla world when outside a given area.

    Parameters:
    world : carla.World
        The Carla world in which to remove actors.
    location : carla.Location, optional
        The location used for determining the center of the area.
    max_distance : float, optional
        The maximum distance an actor can be from the location center.
    actor_filter : str, optional
        A string containing the filter to apply to the world's actor list.
        Only actors with this filter will be removed.
    verbose : bool, optional
        Used to determine whether some information should be displayed.
    '''
    to_remove = [
        actor
        for actor in world.get_actors().filter(actor_filter)
        if not python.utils.actor.in_range(
            actor,
            location,
            max_distance,
            verbose
        )
    ]

    for actor in to_remove:
        actor.destroy()

        if verbose:
            print("Actor", actor.id, "removed from scenario.")

    if verbose:
        print(
            'Total actors remaining:',
            len(world.get_actors().filter('vehicle.*'))
        )


def spawn_actor(
    world: carla.World,
    blueprints: carla.BlueprintLibrary,
    transform: carla.Transform,
    verbose: bool = False
) -> carla.Actor or None:
    '''
    Tries to spawn an actor in the Carla world.

    Parameters:
    world : carla.World
        The Carla world in which to spawn actors.
    blueprints : carla.BlueprintLibrary
        A set of Carla blueprint templates used for creating a blueprint.
    transform : carla.Transform
        The transform (pose) used spawn the actor. Usually determined from 
        carla.Map.get_spawn_points().
    verbose : bool, optional
        Used to determine whether some information should be displayed.

    Returns
    -------
    carla.Actor
        A Carla actor if Carla world was able to spawn an actor in the
        provided transform, otherwise None.
    '''
    blueprint = python.utils.actor.create_random_blueprint(blueprints)
    actor = python.utils.actor.initialize(
        world,
        blueprint,
        transform=transform,
        verbose=verbose
    )

    if actor:
        if "vehicle" in actor.type_id:
            actor.set_autopilot(True)

    return actor
