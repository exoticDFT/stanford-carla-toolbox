# Elaboration of the Examples

This page will try to elaborate on the example code contained in the examples
folder. The examples should already be commented some and the individual
functions should be fully documented. However, it is still useful to explain
what the sections in the example code are attempting to do.

## Example: `spawn-vehicle.jl`

This section will display code snippets throughout of the example and break down
each line of the snippet. Let's take a look...

#### Imports
This first section imports specific Julia packages the example needs for using
the toolbox. In general, these lines will be used in almost all the Julia code
you write that uses the toolbox.

```julia
import StanfordCarlaToolbox
import PyCall

SCT = StanfordCarlaToolbox
```

1. Imports this toolbox to be used throughout your Julia code.
2. Imports the PyCall package, which is used to call Python within Julia.
3. Empty line, purely for code readability.
4. This is a helper variable that will simplify the functional calls to the
toolbox, so that you do not need to write the full package name every time you
want to use a function within the toolbox.

#### Carla basics

This section calls several Carla related functions necessary for creating a
Carla client.

```julia
carla = PyCall.pyimport("carla")
client = SCT.create_carla_client("localhost", 2000, 3.0, "Town04")
world = client.get_world()
```

1. Imports the Python library for Carla. This is needed if you are ever calling
   direct Carla PythonAPI functions. 
2. This creates our Carla client by calling the toolbox function. Specifically,
   we connect to the local computer on port 2000 with a timeout of 3 seconds and
   load the "Town04" map once connected.
3. This returns a Carla would object containing our loaded Town04 map. A world
   object is generally needed for interacting with the Carla server (spawning,
   retrieving actor details, etc.)

#### Generating Vehicle Blueprints

Here we create an actor blueprint, necessary for spawning a actor. In this
example, we want a car, so we get all the available vehicle blueprints and then
pick a specific car model and specify a color.

```julia
blueprint_library = world.get_blueprint_library().filter("vehicle.*")
blueprint = blueprint_library.filter("prius")
bp1 = get(blueprint, 0)

bp1.set_attribute("color", "255, 0, 0")
```

1. This line returns all the available actor blueprints provided by Carla and
   filters it down to just the ones with "vehicle" in the name.
2. Here we pair down further and just return the ones with "prius" in the name.
3. This returns a single blueprint from the list of blueprints with the provided
   filters. It turns out that Carla currently only has one vehicle with this
   name, but since we don't want a single blueprint, we have to pick the first
   element in the list.
4. Empty line, purely for code readability.
5. Finally we set the color of the blueprint to red.