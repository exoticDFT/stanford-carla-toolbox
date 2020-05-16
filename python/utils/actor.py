import carla

import math
import random
import time


def create_random_blueprint(
    blueprints: carla.BlueprintLibrary,
    color: str = ''
):
    '''
    Creates a random Carla actor blueprint based on some provided blueprint
    library.

    Parameters
    ----------
    blueprints : carla.BlueprintLibrary
        A set of Carla blueprint templates used for creating a blueprint.
    color : string, default is empty string
        RGB string used for determining the vehicle's color, order and format
        is 'R, G, B'

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
    actor,
    life_time=-1.0,
    color=carla.Color(255, 0, 0),
    thickness=0.1,
    offset=carla.Location(0.0, 0.0, 0.0)
):
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
    world,
    blueprint,
    position=carla.Vector3D(0.0, 0.0, 0.0),
    rotation=carla.Rotation(0.0, 0.0, 0.0),
    transform=None,
    verbose=False
):
    '''
    Initializes a Carla actor with the provided data and returns the created
    actor.
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


def print_info(actor):
    '''
    Prints some information about the actor provided.
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
    actor,
    origin=carla.Location(0.0, 0.0, 0.0),
    max_distance=100.0,
    verbose=False
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
