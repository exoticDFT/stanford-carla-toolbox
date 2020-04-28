function current_world_to_scene(
    world::PyCall.PyObject
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
            actor_to_entity(actor, AutomotiveSimulator.AgentClass.CAR)
        )
    end
    
    for actor in pedestrians
        push!(
            entities,
            actor_to_entity(
                actor,
                AutomotiveSimulator.AgentClass.PEDESTRIAN
            )
        )
    end

    return AutomotiveSimulator.Scene(entities)
end

function actor_to_entity(
    actor::PyCall.PyObject,
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
    length = 2.0 * bounding_box.y
    width = 2.0 * bounding_box.x

    # Set our vehicle parameters
    vehicle_state = AutomotiveSimulator.VehicleState(global_pos, speed)
    vehicle_def = AutomotiveSimulator.VehicleDef(actor_type, length, width)
    vehicle_id = actor.id

    return AutomotiveSimulator.Entity(
        vehicle_state,
        vehicle_def,
        vehicle_id
    )
end

function get_entity_scene(
    scene::AutomotiveSimulator.Scene,
    index::Int
)
    return scene[index]
end