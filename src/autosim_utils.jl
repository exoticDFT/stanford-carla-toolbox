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

function update_actor_from_entity(
    actor::PyCall.PyObject,
    entity::AutomotiveSimulator.Entity
)
    global_pos = AutomotiveSimulator.posg(entity)
    trans = actor.get_transform()
    trans.location.x = global_pos.x
    trans.location.y = global_pos.y
    trans.rotation.yaw = global_pos.θ
    actor.set_transform(trans)
end

function update_world_from_scene(
    world::PyCall.PyObject,
    scene::AutomotiveSimulator.Scene
)
    actors = world.get_actors()
    vehicles = actors.filter("vehicle.*")
    pedestrians = actors.filter("pedestrian.*")
    actor_ids = Vector{Int}()

    for actor in vehicles
        println(actor)
        push!(actor_ids, actor.id)
    end

    for actor in pedestrians
        println(actor)
        push!(actor_ids, actor.id)
    end

    for entity in scene
        if entity.id in actor_ids
            update_actor_from_entity(world.get_actor(entity.id), entity)
        else
            println("Entity id not in Carla World", entity.id)
        end
    end

end
