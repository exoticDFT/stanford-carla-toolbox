import StanfordCarlaToolbox
import PyCall

SCT = StanfordCarlaToolbox

# Runtime stuff (Main)
carla = PyCall.pyimport("carla")
client = SCT.create_carla_client("localhost", 2000, 3.0, "Town04")
world = client.get_world()

# Create a blueprint for the vehicle
blueprint_library = world.get_blueprint_library().filter("vehicle.*")
blueprints = blueprint_library.filter("prius")
bp1 = get(blueprints, 0)

bp1.set_attribute("color", "255, 0, 0")

# List of spawnpoints visible to default camera location of map (0.9.7)
spawnpoints = [53, 54, 55, 56]
sp1 = spawnpoints[1]

vehicles = Dict(sp1=>bp1)
actors = PyCall.PyObject[]

try
    # Create a scenario with the vehicle
    append!(actors, SCT.initiate_scenario(world, vehicles))

    timestep = 1.0/60.0

    num_ticks = 10

    # Run the basic sim loop
    for i = 1:num_ticks
        # Get some current Carla info and print it out
        println("Actors[1]: ", PyCall.pystr(actors[1].get_transform()))
        sleep(timestep)
    end

finally
    # Sleep a bit, then remove the actors from the simulator
    sleep(3.0)
    SCT.destroy_actors(actors)
end