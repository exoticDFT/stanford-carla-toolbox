import carla

import math
import random
import time


def create_random_blueprint(
    blueprints: carla.BlueprintLibrary,
    color: str = ''
) -> carla.ActorBlueprint:
    '''
    Creates a random Carla actor blueprint based on some provided blueprint
    library.

    Parameters
    ----------
    blueprints : carla.BlueprintLibrary
        A set of Carla blueprint templates used for creating a blueprint.
    color : str, optional
        RGB string used for determining the vehicle's color, order and format
        is 'R, G, B', by default ''.

    Returns
    -------
    carla.ActorBlueprint
        A Carla blueprint to be used for a Carla actor.
    '''
    blueprint = random.choice(blueprints)

    if blueprint.has_attribute('color'):
        if color == '':
            color = random.choice(
                blueprint.get_attribute('color').recommended_values
            )

        blueprint.set_attribute('color', color)

    blueprint.set_attribute('role_name', 'autopilot')

    return blueprint


def draw_boundingbox(
    actor: carla.Actor,
    life_time: float = -1.0,
    color: carla.Color = carla.Color(255, 0, 0),
    thickness: float = 0.1,
    offset: carla.Location = carla.Location(0.0, 0.0, 0.0)
):
    '''
    Draws a bounding box around the Carla Actor.

    Parameters
    ----------
    actor : carla.Actor
        The Carla Actor to draw the bounding box around.
    life_time : float, optional
        The amount of time the bounding box should display, by default -1.0.
    color : carla.Color, optional
        The color of the bounding box, by default carla.Color(255, 0, 0).
    thickness : float, optional
        The thickness of the bounding box lines, by default 0.1.
    offset : carla.Location, optional
        An offset from the actor's center, by default
        carla.Location(0.0, 0.0, 0.0).
    '''
    world = actor.get_world()
    world.debug.draw_box(
        carla.BoundingBox(
            actor.get_location() + actor.bounding_box.location + offset,
            actor.bounding_box.extent
        ),
        actor.get_transform().rotation,
        color=color,
        thickness=thickness,
        life_time=life_time
    )


def initialize(
    world: carla.World,
    blueprint: carla.ActorBlueprint,
    position: carla.Vector3D = carla.Vector3D(0.0, 0.0, 0.0),
    rotation: carla.Rotation = carla.Rotation(0.0, 0.0, 0.0),
    transform: carla.Transform = None,
    verbose: bool = False
) -> carla.Actor:
    '''
    Initializes a Carla actor with the provided data and returns the created
    actor.

    Either provide the location and rotation directly, or a transform. If both
    are provided, the location and rotation parameters will override the
    transform parameter.

    Parameters
    ----------
    world : carla.World
        The Carla World to spawn the actor.
    blueprint : carla.ActorBlueprint
        The blueprint for the actor.
    position : carla.Vector3D, optional
        The location of the actor, by default carla.Vector3D(0.0, 0.0, 0.0).
    rotation : carla.Rotation, optional
        The rotation of the actor, by default carla.Rotation(0.0, 0.0, 0.0)
    transform : carla.Transform, optional
        The transform (location and rotation) of the actor, by default None.
    verbose : bool, optional
        Used to determine whether some information should be displayed, by
        default False.

    Returns
    -------
    carla.Actor
        The spawned actor
    '''
    if not transform:
        transform = carla.Transform(position, rotation)

    actor = world.try_spawn_actor(blueprint, transform)

    if not actor:
        print("Problem creating actor. Returning None")
    elif verbose:
        time.sleep(0.1)
        print("Creating actor:")
        print_info(actor)
        world.debug.draw_box(
            carla.BoundingBox(
                actor.get_location() + actor.bounding_box.location,
                actor.bounding_box.extent
            ),
            actor.get_transform().rotation
        )

    return actor


def print_info(actor: carla.Actor) -> None:
    '''
    Prints some information about the actor provided.

    Parameters
    ----------
    actor : carla.Actor
        The Carla Actor to print information about.
    '''
    print("   Id:", actor.id)
    print("   Type Id:", actor.type_id)
    print("   Transform:", actor.get_transform())
    print("   Velocity:", actor.get_velocity())
    print("   Acceleration:", actor.get_acceleration())
    print("   Bounding box:", actor.bounding_box)
    print(
        "   Waypoint:",
        actor.get_world().get_map().get_waypoint(actor.get_location())
    )


def in_range(
    actor: carla.Actor,
    origin: carla.Location = carla.Location(0.0, 0.0, 0.0),
    max_distance: float = 100.0,
    verbose: bool = False
):
    '''
    Checks if a Carla actor is within a certain distance from a location.

    Parameters
    ----------
    actor : carla.Actor
        The Carla actor in which to check its distance
    origin : carla.Location, optional
        The origin location in which the actor's distance will be determined.
    max_distance : float, optional
        The maximum distance the actor is from the origin used to evaluate
        whether it is within the range.
    verbose : bool, optional
        Used to determine whether some information should be displayed.

    Returns
    -------
    bool
        True if actor is in the range, False otherwise.
    '''
    dist_from_origin = actor.get_location().distance(origin)

    if verbose:
        print("Actor", actor.id, "is", dist_from_origin, "meters away.")

    if dist_from_origin <= max_distance:
        return True
    else:
        return False
