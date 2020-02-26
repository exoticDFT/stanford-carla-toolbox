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