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
   object configured with the provided parmeters. It will load the Town04 world
   and force it to reload if the server already has this world loaded.
6. Gets the Carla World from the server to be used later.
7. Gets the Carla Map from the server to be used later.

## First interaction with the server

This section 