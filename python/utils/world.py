import python.utils.actor

import carla
import numpy

import logging
import re


def change_weather(
    world: carla.World,
    weather_preset: str = 'ClearNoon'
) -> None:
    '''
    Changes the weather in the Carla server.

    This function takes a string that is predefined for the simulator. Some
    examples include, "ClearNoon", "WetNoon", "ClearSunset", etc. For a list of
    all the available options, please look at the Carla documentation.

    Parameters
    ----------
    world : carla.World
        The Carla World in which to change the weather.
    weather_preset : str, optional
        A string representing a predefined weather setting, by default
        'ClearNoon'.
    '''
    weather = carla.WeatherParameters()
    presets = [func for func in dir(weather) if re.match('[A-Z].+', func)]
    if weather_preset in presets:
        world.set_weather(getattr(carla.WeatherParameters, weather_preset))
    else:
        logging.warning(
            '{} is not a recognized preset. Presets available:\n{}'.format(
                weather_preset,
                presets
            )
        )


def destroy_all_dynamic_actors(world: carla.World) -> None:
    '''
    Removes all the dynamic actors in the Carla World.

    Parameters
    ----------
    world : carla.World
        The Carla world in which to remove the actors
    '''
    actor_types = ['sensor', 'vehicle', 'walker']

    for actor in world.get_actors():
        if any(sub in actor.type_id for sub in actor_types):
            actor.destroy()


def draw_arc_between_actors(
    world: carla.World,
    actor1: carla.Actor,
    actor2: carla.Actor,
    z_offset: float = 2.0,
    z_peak: float = 5.0,
    thickness: float = 0.1,
    color: carla.Color = carla.Color(255, 0, 0),
    life_time: float = -1.0
) -> None:
    '''
    Renders a curved line (arc) in the Carla Server between the two provided
    Actors.

    Parameters
    ----------
    world : carla.World
        The Carla world in which the line will be rendered.
    actor1 : carla.Actor
        The first Carla actor to render the arc.
    actor2 : carla.Actor
        The second Carla actor to render the arc.
    z_offset : float, optional
        The z location above the vehicle to start the arc, by default 2.0.
    z_peak : float, optional
        Parameter for determing the height of the arc peak, by default 5.0.
    thickness : float, optional
        The thickness of the rendered arc, by default 0.1.
    color : carla.Color, optional
        The color of the rendered arc, by default carla.Color(255, 0, 0).
    life_time : float, optional
        The time in which the arc will stay on the server, by default -1.0.
    '''
    # z_peak quadratic term: Height of the arc
    actor1_position = actor1.get_location()
    actor2_position = actor2.get_location()
    x1 = actor1_position.x
    y1 = actor1_position.y
    z1 = actor1_position.z + z_offset
    x2 = actor2_position.x
    y2 = actor2_position.y
    z2 = actor2_position.z + z_offset
    prev_position = carla.Location(x2, y2, z2)

    for alpha in numpy.arange(0, 1.0, 0.01):
        x = alpha*x1 + (1 - alpha)*x2
        y = alpha*y1 + (1 - alpha)*y2
        z = alpha*z1 + (1 - alpha)*z2 + 4*z_peak*alpha*(1 - alpha)
        next_position = carla.Location(x, y, z)
        world.debug.draw_line(
            prev_position,
            next_position,
            thickness,
            color,
            life_time
        )
        prev_position = next_position


def draw_line_between_actors(
    world: carla.World,
    actor1: carla.Actor,
    actor2: carla.Actor,
    z_offset: float = 0.5,
    thickness: float = 0.1,
    color: carla.Color = carla.Color(255, 0, 0),
    life_time: float = -1.0
) -> None:
    '''
    Renders a line in the Carla Server between the two provided Actors.

    Parameters
    ----------
    world : carla.World
        The Carla world in which the line will be rendered.
    actor1 : carla.Actor
        The first Carla actor to render the line.
    actor2 : carla.Actor
        The second Carla actor to render the line.
    z_offset : float, optional
        The z location above the vehicle to start the arc, by default 0.5.
    thickness : float, optional
        The thickness of the rendered line, by default 0.1.
    color : carla.Color, optional
        The color of the rendered line, by default carla.Color(255, 0, 0).
    life_time : float, optional
        The time in which the line will stay on the server, by default -1.0.
    '''
    world.debug.draw_line(
        actor1.get_location() + carla.Location(z=z_offset),
        actor2.get_location() + carla.Location(z=z_offset),
        thickness,
        color,
        life_time
    )


def draw_road_ids(world: carla.World, timeout: float = -1.0) -> None:
    '''
    Draws all the road ids from the OpenDrive info in the current Carla world.

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

    # TODO: Should find a better way to get all roads and then draw these ids
    for road_id in range(0, 500):
        waypoint = map.get_waypoint_xodr(road_id, 0, 0.5)

        if waypoint:
            world.debug.draw_string(
                waypoint.transform.location,
                str(road_id),
                life_time=timeout
            )


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
            print('Actor', actor.id, 'removed from scenario.')

    if verbose:
        print(
            'Total actors remaining:',
            len(world.get_actors().filter('vehicle.*'))
        )


def spawn_actor(
    world: carla.World,
    blueprints: carla.BlueprintLibrary,
    transform: carla.Transform,
    autopilot: bool = True,
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
    autopilot : bool, optional
        If the vehicle is a vehicle, this will set its autopilot functionality,
        by default True.
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

    if actor and autopilot:
        if 'vehicle' in actor.type_id:
            actor.set_autopilot(True)

    return actor
