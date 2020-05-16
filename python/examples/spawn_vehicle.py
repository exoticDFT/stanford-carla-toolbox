import python.utils.actor
import python.utils.client
import python.utils.common
import python.utils.world

import carla

import logging
import os
import time


def main():
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=getattr(logging, "INFO")
    )

    logging.info("Starting the {} example.".format(os.path.basename(__file__)))
    carla_client = python.utils.client.create(
        map_name="Town04",
        force_reset=True
    )
    carla_world = carla_client.get_world()
    carla_map = carla_world.get_map()
    python.utils.world.draw_spawn_points(carla_world, 10.0)
    python.utils.world.move_spectator(
        carla_world,
        transform=carla.Transform(
            carla.Location(x=123.756668, y=0.951465, z=25.576216),
            carla.Rotation(pitch=-17.857296, yaw=174.745468, roll=0.000119)
        )
    )
    vehicle_blueprints = carla_world.get_blueprint_library().filter("vehicle.*")
    vehicle_spawnpoints = carla_map.get_spawn_points()
    actors = []

    try:
        actors.append(
            python.utils.world.spawn_actor(
                carla_world,
                vehicle_blueprints,
                vehicle_spawnpoints[56],
                False
            )
        )

        logging.info("Press crtl+c to exit the program.")

        while True:
            carla_world.wait_for_tick()

    finally:
        python.utils.common.sleep_random_time()
        python.utils.client.destroy_actors_in_list(carla_client, actors)


# Start the program
try:
    main()
except KeyboardInterrupt:
    time.sleep(5.0)
finally:
    logging.info('Program finished.')
