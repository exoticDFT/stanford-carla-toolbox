"""
    actor_to_entity(actor, actor_type)

Takes the provided Carla Actor and AutomotiveSimulator AgentClass to convert the
Carla Actor into an AutomotiveSimulator Entity.

...
# Arguments
- `actor`: The Carla Actor that will be converted.
- `actor_type`: The AutomotiveSimulator AgentClass the actor will be converted
    into.
...

Returns an AutomotiveSimulator.Entity converted from the provided Carla Actor.
"""
function actor_to_entity(
    actor::PyCall.PyObject,
    roadway::AutomotiveSimulator.Roadway,
    actor_type::Int64 # AgentClass should be provided
)
    # Get information from the Carla actor
    trans = actor.get_transform()
    position = trans.location
    orientation = trans.rotation
    velocity = actor.get_velocity()
    bounding_box = actor.bounding_box.extent

    # Calculate variables from above
    heading = orientation.yaw
    speed = sqrt(velocity.x*velocity.x + velocity.y*velocity.y)
    global_pos = AutomotiveSimulator.Vec.VecSE2(position.x, position.y, heading)
    length = 2.0 * bounding_box.x
    width = 2.0 * bounding_box.y

    # Set our vehicle parameters
    vehicle_state = AutomotiveSimulator.VehicleState(global_pos, roadway, speed)
    vehicle_def = AutomotiveSimulator.VehicleDef(actor_type, length, width)
    vehicle_id = actor.id

    return AutomotiveSimulator.Entity(
        vehicle_state,
        vehicle_def,
        vehicle_id
    )
end

"""
    add_entity_to_world(entity, world)

Adds the provided entity as a Carla Actor into the Carla environment.

...
# Arguments
- `entity`: The AutomotiveSimulator Entity that will be converted.
- `world`: The Carla World in which to add the created Actor.
...

Returns a Carla Actor containing the information provided by the entity, or None
if the actor was unable to be created.
"""
function add_entity_to_world(
    entity::AutomotiveSimulator.Entity,
    world::PyCall.PyObject
)
    carla = PyCall.pyimport("carla")
    sct_world_util = PyCall.pyimport("python.utils.world")
    veh_bps = world.get_blueprint_library().filter("vehicle*")

    entity_state = entity.state
    global_pos = AutomotiveSimulator.posg(entity)
    trans = carla.Transform()
    trans.location.x = global_pos.x
    trans.location.y = -global_pos.y
    trans.location.z = 2.0
    trans.rotation.yaw = global_pos.θ + 180.0

    entity_def = entity.def
    class = entity_def.class
    length = entity_def.length
    width = entity_def.width

    entity_id = entity.id

    actor = sct_world_util.spawn_actor(world, veh_bps, trans, false)

    return actor
end

"""
    current_world_to_scene(world)

Takes the provided Carla World and returns the currect state of all vehicles and
pedestrians as a AutomotiveSimulator Scene.

...
# Arguments
- `world`: The Carla World on the running server.
...

Return a AutomotiveSimulator.Scene with vehicle and pedestrian actors in the
current Carla World.
"""
function current_world_to_scene(
    world::PyCall.PyObject,
    roadway::AutomotiveSimulator.Roadway
)
    # Get the Carla actors
    actors = world.get_actors()
    vehicles = actors.filter("vehicle.*")
    pedestrians = actors.filter("pedestrian.*")

    entities = Vector{
        AutomotiveSimulator.Entity{
            AutomotiveSimulator.VehicleState,
            AutomotiveSimulator.VehicleDef,
            Int64
        }
    }()

    for actor in vehicles
        push!(
            entities,
            actor_to_entity(actor, roadway, AutomotiveSimulator.AgentClass.CAR)
        )
    end
    
    for actor in pedestrians
        push!(
            entities,
            actor_to_entity(
                actor,
                roadway,
                AutomotiveSimulator.AgentClass.PEDESTRIAN
            )
        )
    end

    return AutomotiveSimulator.Scene(entities)
end

"""
    get_entity_from_scene(scene, index)

Takes a AutomotiveSimulator Scene and index in the scene to return that specific
Entity.

...
# Arguments:
- `scene`: A AutomotiveSimulator Scene that contains the details of the
    simulator at that instant.
- `index`: An index representing the Entity to get from the scene.
...

Returns the Entity represented by its index in the provided scene.
"""
function get_entity_from_scene(
    scene::AutomotiveSimulator.Scene,
    index::Int
)
    return scene[index]
end

# function get_entity_transform(
#     entity::AutomotiveSimulator.Entity,
#     right_handed::Bool = false
# )
#     carla = PyCall.pyimport("carla")

#     global_pos = AutomotiveSimulator.posg(entity)
#     trans = carla.Transform()
#     trans.location.x = global_pos.x

#     if right_handed
#         trans.location.y = -global_pos.y
#     else
#         trans.location.y = global_pos.y
#     end

#     trans.rotation.yaw = global_pos.θ

#     return trans
# end

"""
    update_actor_from_entity(actor, entity, right_handed)

Function to modify a Carla Actor object based on the information provided by the
AutomotiveSimulator entity object.

This function considers the "handiness" of the entity data. Carla is a
left-handed system, so data from the entity must be converted if the data is
in a right-handed system. Left-handed means +x to the right, +y is down and +z
is out of the screen.

...
# Arguments:
- `actor`: The Carla Actor that will be updated based on entity data.
- `entity`: An AutomotiveSimulator Entity which will be used to move the actor.
- `right_handed`: A Boolean letting the system know if the entity data is in a
    right-handed coordinate system (+x to right, +y up)
"""
function update_actor_from_entity(
    actor::PyCall.PyObject,
    entity::AutomotiveSimulator.Entity,
    right_handed::Bool = false
)
    global_pos = AutomotiveSimulator.posg(entity)
    trans = actor.get_transform()
    trans.location.x = global_pos.x
    trans.location.y = global_pos.y
    trans.rotation.yaw = rad2deg(global_pos.θ)

    if right_handed
        trans.location.y = -global_pos.y
        trans.rotation.yaw = rad2deg(-global_pos.θ)
    end

    actor.set_transform(trans)
end

"""
    update_world_from_scene(world, scene)

Updates the Carla World to the current information from the provided
AutomotiveSimulator Scene.

...
# Arguments:
- `world`: The Carla World that will be updated.
- `scene`: A AutomotiveSimulator Scene that contains the details of the
    simulator at that instant.
"""
function update_world_from_scene(
    world::PyCall.PyObject,
    scene::AutomotiveSimulator.Scene
)
    actors = world.get_actors()
    vehicles = actors.filter("vehicle.*")
    pedestrians = actors.filter("pedestrian.*")
    actor_ids = Vector{Int}()

    for actor in vehicles
        push!(actor_ids, actor.id)
    end

    for actor in pedestrians
        push!(actor_ids, actor.id)
    end

    for entity in scene
        if entity.id in actor_ids
            update_actor_from_entity(world.get_actor(entity.id), entity)
        else
            println("Entity id not in Carla World: ", entity.id)
        end
    end
end

"""
    update_world_from_scene(world, scene, mapping, right_handed)

Updates the Carla World to the current information from the provided
AutomotiveSimulator Scene and the given mapping between the entity and actor
ids.

This function considers the "handiness" of the scene's data. Carla is a
left-handed system, so data from the entity must be converted if the data is
in a right-handed system. Left-handed means +x to the right, +y is down and +z
is out of the screen.

...
# Arguments:
- `world`: The Carla World that will be updated.
- `scene`: An AutomotiveSimulator Scene that contains the details of the
    simulator at that instant.
- `mapping`: A mapping representing the link between an actor and an entity.
    This is most likely necessary if the entity data was generated previous via
    AutomotiveSimulator (reading in pre-calculated Scene objects.)
- `right_handed`: A Boolean letting the system know if the entity data is in a
    right-handed coordinate system (+x to right, +y up)
"""
function update_world_from_scene(
    world::PyCall.PyObject,
    scene::AutomotiveSimulator.Scene,
    mapping::Dict{Any, Int},
    right_handed::Bool = false
)
    for entity in scene
        actor_id = get(mapping, entity.id, -999)
        update_actor_from_entity(
            world.get_actor(actor_id),
            entity,
            right_handed
        )
    end
end

"""
    visualize_in_carla(world, scenes, time_step, entity_map, right_handed)

Takes a collection of pre-simulated scenes from an Automotive Simulator run and
visualizes it in the provided Carla world.

This function considers the "handiness" of the scene's data. Carla is a
left-handed system, so data from the entity must be converted if the data is
in a right-handed system. Left-handed means +x to the right, +y is down and +z
is out of the screen.

...
# Arguments:
- `world`: The Carla World that will be updated.
- `scenes`: A collection of AutomotiveSimulator Scenes containing the details
    of the simulation over some time.
- `timestep`: The time-step used during the AutomotiveSimulator simulation.
- `entity_map`: A mapping representing the link between an actor and an entity.
    This is most likely necessary if the entity data was generated previous via
    AutomotiveSimulator (reading in pre-calculated Scene objects.)
- `right_handed`: A Boolean letting the system know if the entity data is in a
    right-handed coordinate system (+x to right, +y up)
"""
function visualize_in_carla(
    world::PyCall.PyObject,
    scenes::Vector{<:AutomotiveSimulator.Scene},
    time_step::AbstractFloat,
    entity_map::Dict{Any, Int},
    right_handed::Bool = false
)
    for i = 1 : length(scenes)
        start_time = Dates.datetime2epochms(Dates.now())
        scene = scenes[i]
        update_world_from_scene(world, scene, entity_map, right_handed)
        sleep_time_ms = (start_time + time_step*1000) -
            Dates.datetime2epochms(Dates.now())

        if sleep_time_ms > 0
            sleep(sleep_time_ms / 1000.0)
        end
    end
end