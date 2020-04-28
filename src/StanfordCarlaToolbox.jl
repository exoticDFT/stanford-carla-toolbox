module StanfordCarlaToolbox

import AutomotiveSimulator
import Formatting
import PyCall

# AutomotiveSimulator records based functions
include("adm_records.jl")
export current_world_to_frame,
       actor_to_entity

# Carla scenario generation related functions
include("adm_scenario.jl")
export destroy_actors,
       initiate_scenario

# AutomotiveSimulator simulation based functions
include("adm_sim.jl")
export create_carla_client,
       get_server_information

end #StanfordCarlaToolbox