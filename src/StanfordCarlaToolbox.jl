module StanfordCarlaToolbox

import AutomotiveSimulator
import Dates
import Formatting
import PyCall

# AutomotiveSimulator based functions
include("autosim_utils.jl")
export actor_to_entity,
       add_entity_to_world,
       current_world_to_scene,
       get_entity_from_scene,
       update_actor_from_entity,
       update_world_from_scene,
       visualize_in_carla

# Carla client based functions
include("client_utils.jl")
export create_carla_client,
       get_server_information

# Carla scenario generation related functions
include("scenario_utils.jl")
export destroy_actors,
       initiate_scenario

end #StanfordCarlaToolbox