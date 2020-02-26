"""
    destroy_actors(actors)

Destroys all the provided actors in the current Carla world.

This function takes an array of carla.Actor objects. If the actor is in the
    current world, then it is removed (destroyed) from the Carla server.

...
# Arguments
- `actors::Array{PyCall.PyObject <class carla.Actor>}`: An array of Carla actors
    that should be destroyed.
"""
function destroy_actors(actors::Array)
    for actor in actors
        if actor != PyCall.PyObject(nothing) && actor.is_alive
            println("Destroying actor ", actor.id)
            actor.destroy()
        end
    end
end

"""
    initiate_scenario(world, vehicles)

Initialize a scenario in the loaded Carla world.

This version of the function is used for generating a scenario of vehicles (no
    pedestrians) within the specified Carla World. The vehicle type and
    location in the map are provided by the "vehicles" dictionary, where the
    key is a spawnpoint value from the list of all spawnpoints of the Carla map
    and the value is the blueprint corresponding to the vehicle's properties.

...
# Arguments
- `world::PyCall.PyObject <class carla.World>`: The Carla world in which to
    initialize the scenario. 
- `vehicles::Dict{Int64, PyCall.Object <class carla.BlueprintLibrary>}`: A
    dictionary of (index, blueprint) pairs, where the index represents one
    value of the Carla map's available spawnpoints and the blueprint represents
    a `carla.ActorBlueprint` for a specific vehicle.
...

Return an Array{PyCall.PyObject <class carla.Vehicle>} containing all the Carla
vehicles that were added to the world.
"""
function initiate_scenario(
    world::PyCall.PyObject,
    vehicles::Dict{Int, PyCall.PyObject}
)
    all_sp = world.get_map().get_spawn_points()
    actors = PyCall.PyObject[]

    for (spawnpoint, blueprint) in vehicles
        actor = world.try_spawn_actor(blueprint, all_sp[spawnpoint+1])

        # If the actor was created, didn't return None, add to actors array
        if actor != PyCall.PyObject(nothing)
            push!(actors, actor)
        end
    end

    return actors
end