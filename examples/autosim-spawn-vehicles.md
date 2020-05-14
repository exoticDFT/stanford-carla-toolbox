# Example: `autosim-spawn-vehicles.jl`

This section will display code snippets throughout of the example and break down
each line of the snippet. Let's take a look...

## Imports
This first section imports specific Julia packages the example needs for using
the toolbox. In general, these lines will be used in almost all the Julia code
you write that uses the toolbox.

```julia
import StanfordCarlaToolbox
import PyCall
import AutomotiveSimulator

AS = AutomotiveSimulator
SCT = StanfordCarlaToolbox
```

1. Imports this toolbox to be used throughout your Julia code.
2. Imports the PyCall package, which is used to call Python within Julia.
3. Imports AutomotiveSimulator package to be used throughout your Julia code.
4. Empty line, purely for code readability.
5. This is a helper variable that will simplify the functional calls to the
toolbox, so that you do not need to write the full package name every time you
want to use a function within the toolbox.
6. Same as above, but for the AutomoticeSimulator package.

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

Here we create 4 actor blueprints, necessary for spawning our actors. In this
example, we want cars, so we get all the available vehicle blueprints and then
pick a specific car model and specify colors.

```julia
blueprint_library = world.get_blueprint_library().filter("vehicle.*")
blueprints = blueprint_library.filter("prius")
bp1 = get(blueprints, 0)
bp2 = get(blueprints, 0)
bp3 = get(blueprints, 0)
bp4 = get(blueprints, 0)

bp1.set_attribute("color", "255, 0, 0")
bp2.set_attribute("color", "0, 255, 0")
bp3.set_attribute("color", "0, 0, 255")
bp4.set_attribute("color", "255, 0, 255")
```

1. This line returns all the available actor blueprints provided by Carla and
   filters it down to just the ones with "vehicle" in the name.
2. Here we pair down further and just return the ones with "prius" in the name.
3. This returns a single blueprint from the list of blueprints.
4. Same as above, but for the second blueprint.
5. Same as above, but for the third blueprint.
6. Same as above, but for the fourth blueprint.
7. Empty line, purely for code readability.
8. We set the color of the first blueprint to red.
9. We set the color of the first blueprint to green.
10. We set the color of the first blueprint to blue.
11. We set the color of the first blueprint to purple.

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
sp2 = spawnpoints[2]
sp3 = spawnpoints[3]
sp4 = spawnpoints[4]

vehicles = Dict(sp1=>bp1, sp2=>bp2, sp3=>bp3, sp4=>bp4)
actors = PyCall.PyObject[]

try
    # Create a scenario with the vehicle
    append!(actors, SCT.initiate_scenario(world, vehicles))
```

1. Here we create a list of desired spawnpoint indices from the list of all
   possible spawnpoints of the Carla map.
2. We set the first index in the list to a variable for later use.
3. Same as above, but for the second spawnpoint.
4. Same as above, but for the third spawnpoint.
5. Same as above, but for the fourth spawnpoint.
6. Empty line, purely for code readability.
7. We need a dictionary with spawnpoint indices as keys and vehicle blueprints
   as values, which will be used in the scenario initialization function.
8. Last is a list to store all the actors we will be creating during the
   scenario generation. This will be used to manage the actors during
   co-simulation.
9. Empty line, purely for code readability.
10. Start of try-finally block. This isn't strictly necessary, but allows us to
   perform some actions even if some problems arise during the scenario
   generation.
11. Comment, purely for code readability.
12. Here we call another toolkit function that will create our vehicle actors in
   the Carla server and return the carla.Actor objects. We store these objects
   in our predefined actor list. 

## Running the main sim loop

In this section we discuss the actual loop that is running for the client. This
specific client example only runs for a short period of time and prints some
information about the vehicles. Nothing fancy here, just showing you an idea of
how a sim loop could work. In general, we would do some calculations and move
the vehicles in the Carla server based on these calculations. Since we are doing
some co-simulation, this example shows the user a basic flow of a Carla client
that also interacts with AutomotiveSimulator (AS). We set up multiple agents
for AS with the Intelligent Driver Model at various speeds. During the loop, we
print some information from AS as well as Carla to show that the vehicle is
indeed in the same location in both simulator environments.

```julia
    timestep = 1.0/60.0

    models = Dict{Int, AS.DriverModel}()
    models[1] = AS.LatLonSeparableDriver(
        AS.ProportionalLaneTracker(),
        AS.IntelligentDriverModel()
    )
    models[2] = AS.LatLonSeparableDriver(
        AS.ProportionalLaneTracker(),
        AS.IntelligentDriverModel()
    )
    models[3] = AS.LatLonSeparableDriver(
        AS.ProportionalLaneTracker(),
        AS.IntelligentDriverModel()
    )
    models[4] = AS.LatLonSeparableDriver(
        AS.ProportionalLaneTracker(),
        AS.IntelligentDriverModel()
    )

    AS.set_desired_speed!(models[1], 15.0)
    AS.set_desired_speed!(models[2], 12.0)
    AS.set_desired_speed!(models[3], 10.0)
    AS.set_desired_speed!(models[4], 8.0)

    num_ticks = 10

    # Run the basic sim loop
    for i = 1:num_ticks
        # Get some current Carla info and print it out
        scene = SCT.current_world_to_scene(world)
        println("Scene: ", scene)
        println("Scene[1]: ", SCT.get_entity_scene(scene, 1))
        println("Actors[1]: ", PyCall.pystr(actors[1].get_transform()))
        sleep(timestep)
    end
```

1. The simulation loop will need to know now long each tick should take. In this
   case, we set the timestep to 1/60th of a second, or 60 ticks per second.
2. Empty line, purely for code readability.
3. We create a dictionary of models for each vehicle we will co-simulate.
4. The first model is created as an IDM agent.
5. Continuation of above line.
6. Continuation of above line.
7. Continuation of above line.
8. The second model is also created as an IDM agent.
9. Continuation of above line.
10. Continuation of above line.
11. Continuation of above line.
12. The third model is also created as an IDM agent.
13. Continuation of above line.
14. Continuation of above line.
15. Continuation of above line.
16. The fourth model is also created as an IDM agent.
17. Continuation of above line.
18. Continuation of above line.
19. Continuation of above line.
20. Empty line, purely for code readability.
21. Sets the desired speed of agent 1 to 15 mph.
22. Sets the desired speed of agent 2 to 12 mph.
23. Sets the desired speed of agent 3 to 10 mph.
24. Sets the desired speed of agent 4 to 8 mph.
25. Empty line, purely for code readability.
26. This variable is to tell the loop to run 10 times.
27. Comment, purely for code readability.
28. The beginning of the `for` loop. This loop will start at 1 and run until
   `num_ticks` is reached.
29. Comment, purely for code readability.
30. This calls another SCT function to convert the current Carla world into an
    AS Scene object.
31. Prints the overall scene information to show all the actors in the scene.
32. Calls another SCT function to return only one specific actor in the scene.
33. Here we are just printing the actor's transform, which is an object of all
   carla.Actor objects. We need to call the `PyCall.pystr` function to make sure
   the python string is printed for the object and not Julia's representation of
   the object.
31. The loop now sleeps for the desired time before doing the next tick.
32. The end of the `for` loop.

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
