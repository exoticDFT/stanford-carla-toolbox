import StanfordCarlaToolbox
import PyCall
import AutomotiveSimulator
import AutomotiveVisualization
import Reel
import OpenDriveToRoadway
using Formatting

AS = AutomotiveSimulator
OD2R = OpenDriveToRoadway
SCT = StanfordCarlaToolbox

DATA_FOLDER = "/"*relpath((@__DIR__)*"/../data","/")

# Runtime stuff (Main)
carla = PyCall.pyimport("carla")
sct_world_util = PyCall.pyimport("python.utils.world")
# client = SCT.create_carla_client("localhost", 2000, 6.0, "Town01")
client = SCT.create_carla_client("msl-zephyrus.local", 2000, 6.0, "Town01")
world = client.get_world()
sct_world_util.change_weather(world)
sct_world_util.move_spectator(
    world,
    transform=carla.Transform(
        carla.Location(x=216.032944, y=265.309021, z=124.616531),
        carla.Rotation(pitch=-44.674000, yaw=-90.054848, roll=0.000034)
    )
)

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
spawnpoints = [84, 153, 154, 156]
sp1 = spawnpoints[1]
sp2 = spawnpoints[2]
sp3 = spawnpoints[3]
sp4 = spawnpoints[4]

vehicles = Dict(sp4 => bp4, sp3 => bp3, sp2 => bp2, sp1 => bp1)
actors = Vector{PyCall.PyObject}()

try
    # Generate our AutomotiveSimulator Roadway from Carla Town01
    roadway = OD2R.OpenDriveToRoadwaysConverter(
        joinpath(DATA_FOLDER, "Town01.xodr"),
        12
    )

    # Initialize the scenario in AutomotiveSimulator and Carla
    append!(actors, SCT.initiate_scenario(world, vehicles))

    # Add a driver model to each entity/actor
    i = 0
    models = Dict{Int, AS.DriverModel}()
    for actor in actors
        models[actor.id] = AS.LatLonSeparableDriver(
            AS.ProportionalLaneTracker(),
            AS.IntelligentDriverModel(v_des=7.5 + 2.5*i)
        )
        i = i + 1
    end

    # Run the AutomotiveSimulator simulation
    num_ticks = 1000
    timestep = 1.0/60.0
    scene = SCT.current_world_to_scene(world, roadway)
    scenes = AS.simulate(scene, roadway, models, num_ticks, timestep)

    # Visualize with AutomotiveVisualization
    AutomotiveVisualization.colortheme["background"] = AutomotiveVisualization.colorant"white"; # hide
    colors = [
        AutomotiveVisualization.colorant"purple",
        AutomotiveVisualization.colorant"blue",
        AutomotiveVisualization.colorant"green",
        AutomotiveVisualization.colorant"red",
    ]
    camera = AutomotiveVisualization.StaticCamera(
        position=AutomotiveSimulator.VecE2(212.0, 197.0),
        zoom=3,
        canvas_height=200
    )
    snapshot = AutomotiveVisualization.render(
        [roadway, (AutomotiveVisualization.FancyCar(car=scene[i], color=colors[i]) for i in 1:4)...],
        camera=camera
    )

    animation = Reel.roll(fps=1.0/timestep, duration=num_ticks*timestep) do t, dt
        i = Int(floor(t/dt)) + 1
        AutomotiveVisualization.render([roadway, scenes[i]], canvas_height=120)
    end

    # Visualize with Carla
    for i = 1:num_ticks
        # Get some current Carla info and print it out
        scene = scenes[i]
        actor = actors[1]
        printfmtln("Entity({1}): {2}", actor.id, AS.get_by_id(scene, actor.id))
        printfmtln("Actor({1}): {2}", actor.id, PyCall.pystr(actor.get_transform()))
        SCT.update_world_from_scene(world, scene)
        sleep(timestep)
    end

finally
    # Sleep a bit, then remove the actors from the simulator
    sleep(3.0)
    SCT.destroy_actors(actors)
end