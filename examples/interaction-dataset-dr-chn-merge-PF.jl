import StanfordCarlaToolbox
import PyCall
import AutomotiveSimulator
import OpenDrive2Roadway
using Dates
using Formatting
using JLD

AS = AutomotiveSimulator
OD2R = OpenDrive2Roadway
SCT = StanfordCarlaToolbox

DATA_FOLDER = "/"*relpath((@__DIR__)*"/../data","/")

# Runtime stuff (Main)
carla = PyCall.pyimport("carla")
sct_client_util = PyCall.pyimport("python.utils.client")
sct_world_util = PyCall.pyimport("python.utils.world")
# client = SCT.create_carla_client("localhost", 2000, 10.0)
client = SCT.create_carla_client("msl-zephyrus.local", 2000, 10.0)
sct_client_util.load_xodr_world(
    client,
    joinpath(DATA_FOLDER, "interaction_ab1b2cd_paramPoly3.xodr"),
    wall_height=0.0,
    additional_width=0.0,
    smooth_junctions=false
)
world = client.get_world()
sct_world_util.change_weather(world)
sct_world_util.move_spectator(
    world,
    transform=carla.Transform(
        # Sideview of all of the road
        carla.Location(x=1089.920044, y=-899.645813, z=25.602356),
        carla.Rotation(pitch=-19.801695, yaw=-96.788994, roll=0.000028)
    )
)

scenelist = JLD.load(joinpath(DATA_FOLDER, "scenelist_ours.jld"), "scenelist")
scene1 = scenelist[1]

entity_actor_map = Dict{Int, Int}()

for entity in scene1
    actor = SCT.add_entity_to_world(entity, world)
    sleep(1.0)
    actor.set_simulate_physics(false)
    entity_actor_map[entity.id] = actor.id
end

# Visualize with Carla
timestep = 1/10.0

for i = 1:length(scenelist)
    start_time = Dates.datetime2epochms(now())
    scene = scenelist[i]
    SCT.update_world_from_scene(world, scene, entity_actor_map, true)
    sleep((start_time + timestep*1000 - Dates.datetime2epochms(now()))/1000)
end
