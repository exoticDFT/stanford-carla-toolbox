# Example: `spawn-vehicle.jl`

This section will display code snippets throughout of the example and break down
each line of the snippet. Let's take a look...

## Imports
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

## Carla basics

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
3. This returns a Carla World object containing our loaded Town04 map. A world
   object is generally needed for interacting with the Carla server (spawning,
   retrieving actor details, etc.)

## Generating Vehicle Blueprints

Here we create an actor blueprint, necessary for spawning an actor. In this
example, we want a car, so we get all the available vehicle blueprints and then
pick a specific car model and specify a color.

```julia
blueprint_library = world.get_blueprint_library().filter("vehicle.*")
blueprints = blueprint_library.filter("prius")
bp1 = get(blueprints, 0)

bp1.set_attribute("color", "255, 0, 0")
```

1. This line returns all the available actor blueprints provided by Carla and
   filters it down to just the ones with "vehicle" in the name.
2. Here we pair down further and just return the ones with "prius" in the name.
3. This returns a single blueprint from the list of blueprints. It turns out
   that Carla currently only has one vehicle with this name, but since we don't
   want the whole list of blueprints, we have to pick the first element.
4. Empty line, purely for code readability.
5. Finally we set the color of the blueprint to red.

## Initializing the scenario

This section initializes the input parameters for the scenario generation. The
first part provides a set of predetermined map spawn locations where we want the
cars to appear. These specific locations are chosen to be on one of the main
highway segments which the server camera is viewing (at least in 0.9.7.). We
also create a list of PyObjects to store all the actors in the scenario that we
are going to create.

```julia
spawnpoints = [53, 54, 55, 56]
sp1 = spawnpoints[1]

vehicles = Dict(sp1=>bp1)
actors = PyCall.PyObject[]

try
    # Create a scenario with the vehicle
    append!(actors, SCT.initiate_scenario(world, vehicles))
```

1. Here we create a list of desired spawnpoint indices from the list of all
   possible spawnpoints of the Carla map.
2. We set the first index in the list to a variable for later use.
3. Empty line, purely for code readability.
4. We need a dictionary with spawnpoint indices as keys and vehicle blueprints
   as values, which will be used in the scenario initialization function.
5. Last is a list to store all the actors we will be creating during the
   scenario generation. This will be used to manage the actors during
   co-simulation.
6. Empty line, purely for code readability.
7. Start of try-finally block. This isn't strictly necessary, but allows us to
   perform some actions even if some problems arise during the scenario
   generation.
8. Comment, purely for code readability.
9. Here we call another toolkit function that will create our vehicle actors in
   the Carla server and return the carla.Actor objects. We store these objects
   in our predefined actor list. 

## Running the main sim loop

In this section we discuss the actual loop that is running for the client. This
specific client example only runs for a short period of time and prints some
information about the vehicles. Nothing fancy here, just showing you an idea of
how a sim loop could work. In general, we would do some calculations and move
the vehicles in the Carla server based on these calculations. Since we are not
doing any co-simulation, this example is just giving the user a basic flow of
a Carla client.

```julia
    timestep = 1.0/60.0

    num_ticks = 10

    # Run the basic sim loop
    for i = 1:num_ticks
        # Get some current Carla info and print it out
        println("Actors[1]: ", PyCall.pystr(actors[1].get_transform()))
        sleep(timestep)
    end
```

1. The simulation loop will need to know now long each tick should take. In this
   case, we set the timestep to 1/60th of a second, or 60 ticks per second.
2. Empty line, purely for code readability.
3. This variable is to tell the loop to run 10 times.
4. Empty line, purely for code readability.
5. Comment, purely for code readability.
6. The beginning of the `for` loop. This loop will start at 1 and run until
   `num_ticks` is reached.
7. Comment, purely for code readability.
8. Here we are just printing the actor's transform, which is an object of all
   carla.Actor objects. We need to call the `PyCall.pystr` function to make sure
   the python string is printed for the object and not Julia's representation of
   the object.
9. The loop now sleeps for the desired time before doing the next tick.
10. The end of the `for` loop.

## Ending the client

This last section wait a few seconds before removing the actors from the Carla
server. Nothing else fancy here.

```julia
finally
    # Sleep a bit, then remove the actors from the simulator
    sleep(3.0)
    SCT.destroy_actors(actors)
end
```

1. This is the finally section of the try-finally block discussed earlier.
2. Comment, purely for code readability.
3. Sleep the client for three seconds before continuing.
4. This call to the toolbox function for removing, or "destroying" the actors we
   created on the Carla server.
5. Ends the try-finally block and the end of the client.
