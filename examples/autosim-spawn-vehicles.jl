import StanfordCarlaToolbox
import PyCall
import AutomotiveSimulator

AS = AutomotiveSimulator
SCT = StanfordCarlaToolbox

# Runtime stuff (Main)
carla = PyCall.pyimport("carla")
client = SCT.create_carla_client("localhost", 2000, 3.0, "Town04")
world = client.get_world()

# Create a blueprint for the vehicle
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

# List of spawnpoints visible to default camera location of map (0.9.7)
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

finally
    # Sleep a bit, then remove the actors from the simulator
    sleep(3.0)
    SCT.destroy_actors(actors)
end