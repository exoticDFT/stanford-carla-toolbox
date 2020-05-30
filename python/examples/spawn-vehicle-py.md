# Example: `spawn_vehicle.py`

This section will display code snippets throughout of the example and break down
each line of the snippet. Let's take a look...

## Imports

This first section imports specific Julia packages the example needs for using
the toolbox. In general, these lines will be used in almost all the Julia code
you write that uses the toolbox.

```python
import python.utils.actor
import python.utils.client
import python.utils.common
import python.utils.world

import carla

import logging
import os
import time
```

1. Imports the actor module of the toolbox to be used throughout your code.
2. Imports the client module of the toolbox to be used throughout your code.
3. Imports the common module of the toolbox to be used throughout your code.
4. Imports the world module of the toolbox to be used throughout your code.
5. Empty line, purely for code readability.
6. Imports the carla Python API.
7. Empty line, purely for code readability.
8. Imports the Python logging module, for better display of prints. Not 
   necessary in general, but used in this example.
9. Imports the Python os module, for some system details. Not necessary in
   general, but used in this example.
10. Imports the Python os module, for some system details. Not necessary in
    general, but used in this example.

## Main function and setting up a logger

This section defines are main function, to do the real work of the client and
sets up a Python logger, for better print statements on the status of your
application. The logger isn't entirely necessary, but it's really a nice
feature to have in your applications. It allows you to print things to the
terminal, and a file, in various ways. Look into the logging module if you want
to really understand the details. Here we are just logging "INFO" to the
terminal to get an idea of the application status.

```python
def main():
    logging.basicConfig(
        format='%(levelname)s: %(message)s',
        level=getattr(logging, "INFO")
    )

    logging.info("Starting the {} example.".format(os.path.basename(__file__)))
```

1. Creates a function called `main` which will be called later.
2-4. Creates a logger instance using some basic configuration. Specifically,
   sets the format of the output for every message and sets the logging level
   to "INFO". This will only display "INFO" level logging statements to the
   terminal.
5. Empty line, purely for code readability.
6. Writes a logging message (level "INFO") to the terminal, which will tell the
   users that the example client has started.

## Carla basics

This section calls several of the absolutely necessary components needed in
every client. The first is the client instance itself. This will always be
necessary, although in this example we are calling the specific wrapper function
that incorporates several API calls in one simple command. The `carla_world` and
`carla_map` aren't entirely necessary, but in general you will likely use them
throughout the code. Without the Carla World object, you won't be doing much
with your application. Same can be said about the Carla Map object.

```python
    carla_client = python.utils.client.create(
        timeout=6.0,
        map_name="Town04",
        force_reset=True
    )
    carla_world = carla_client.get_world()
    carla_map = carla_world.get_map()
```

1-5. Calls a function from the toolbox that creates and returns a Carla Client
   object configured with the provided parameters. It will load the Town04 world
   and force it to reload if the server already has this world loaded.
6. Gets the Carla World from the server to be used later.
7. Gets the Carla Map from the server to be used later.

## First interaction with the server

This section calls some functions from the toolbox's world module to showcase
some of the functionality you can capitalize in your application. The first part
takes the Carla world and displays text of the spawnpoint indices in the server.
This can be used for determining locations you would like to spawn vehicles at
throughout the Carla map. We then move the "spectator" camera which is always
created when initializing the Carla server. Here we move the spectator to a
location that will be able to view the vehicle we will spawn later. The second
part of this section grabs a list of all the available vehicle blueprints in
Carla and a list of all the available vehicle spawnpoints in the current Carla
map. Finally, we create a list of for holding the actors we will be creating,
which will be used later to destroy our vehicle before killing the application.

```python
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
```

1. Calls a toolbox function that writes all the available spawnpoint indices on
   the server window.
2-7. Calls another toolbox function that will move the Carla spectator camera to
   the desired location with the given orientation. The spectator is generally
   spawned in a location Carla is trying to promote, but may not be where you
   want to look. This function can be called at any time to update the camera
   location while the client is running.
8. Stores a list of all available vehicle blueprints from Carla.
9. Stores a list of all available vehicle spawnpoints from the Carla map.
10. Create a list for storing the actor (vehicle) we will create later.

## Spawn the vehicle and let it drive until you're done

This section spawns a Carla Vehicle in the Carla World and allows it to drive
around the map until the user decides they want to exit the application. When
the signal is given, the application will wait for a random amount of time and
then destroy the actor from the World and exit the application. Pretty simple
use of the functions here to give a sense of the functionality for some of the
available module functions.

```python
    try:
        actors.append(
            python.utils.world.spawn_actor(
                carla_world,
                vehicle_blueprints,
                vehicle_spawnpoints[56],
                True,
                False
            )
        )

        logging.info("Press crtl+c to exit the program.")

        while True:
            carla_world.wait_for_tick()

    finally:
        python.utils.client.destroy_actors_in_list(carla_client, actors)
```

1. Starts a try-finally block.
2-10. Here we append a single Actor, specifically a Vehicle, to our actor list
   by calling the world module spawn_actor function. This specific call is
   spawning the vehicle with a random blueprint at a point where the spectator
   is looking and allows it to drive autonomously with the Carla agent model.
11. Empty line, purely for code readability.
12. Writes a logging message to the terminal to tell the user the press a button
   combination in order to end the application.
13. Empty line, purely for code readability.
14. Loops the application indefinitely.
15. Calls the "tick" function of the Carla API.
16. Empty line, purely for code readability.
17. Starts the finally section of the try-finally block.
18. Calls a client module function to destroy all the actors on the server from
    the provided list of actors.

## Call the main function to actually start the application

This section calls our main function created above, watches for a keyboard
interrupt signal and exits the program once that signal is caught.

```python
try:
    main()
except KeyboardInterrupt:
    python.utils.common.sleep_random_time()
finally:
    logging.info('Program finished.')
```

1. Starts a try-except-finally block.
2. Calls our main function we created above.
3. This allows us to handle a keyboard interrupt command and do something before
   exiting the application.
4. Calls a common module function to sleep the application for some time.
5. Starts the finally section of the try-except-finally block.
6. Writes a logging message to the terminal to inform the user the application
   exited successfully.