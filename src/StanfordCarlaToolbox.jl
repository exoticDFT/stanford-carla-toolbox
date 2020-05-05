module StanfordCarlaToolbox

import AutomotiveSimulator
import Formatting
import PyCall

# AutomotiveSimulator based functions
include("autosim_utils.jl")
export current_world_to_scene,
       actor_to_entity,
       get_entity_scene

# Carla client based functions
include("client_utils.jl")
export create_carla_client,
       get_server_information

# Carla scenario generation related functions
include("scenario_utils.jl")
export destroy_actors,
       initiate_scenario

end #StanfordCarlaToolbox