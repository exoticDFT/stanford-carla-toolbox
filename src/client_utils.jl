"""
    create_carla_client([host, port, timeout, map])

Create a link to a running Carla server via a Carla client object.

...
# Arguments
- `host::String="localhost"`: The location (IP) of the Carla server.
- `port::Integer=2000`: The port value of the Carla server.
- `timeout::Float=3.0`: The number of seconds in which to attempt any server
    query before timing out.
- `map::String="Town04"`: The name of the Carla map to load when connecting to
    the server. This will destroy any current "episode" running on the server
    and start a new one with the specified map.
...

Return a carla.Client python object which successfully connected to the Carla
server.
"""
function create_carla_client(
    host="localhost",
    port=2000,
    timeout=3.0,
    map="Town04"
)
    try
        carla = PyCall.pyimport("carla") #-> PyObject <module 'carla'> 
        client = carla.Client(host, port)
        client.set_timeout(timeout)

        # Load the specified map and get server details
        client.load_world(map)
        get_server_information(client)

        # Return the client and world objects
        return client
    catch err
        if isa(err, PyCall.PyError)
            println("ERROR: Cannot connect to the Carla server.")
            cause = err.val.args[1]

            if occursin("version", cause)
                println(
                    "   Are the server and client the same version? ",
                    "Please verify your PYTHONPATH or Python virtual ",
                    "environment is using the correct Carla egg file."
                )
            elseif occursin("time-out", cause)
                println("   Is the server available at ", host, ":", port, "?")
            elseif occursin("No module", cause)
                println(
                    "   The carla module doesn't seem to be installed.\n\n",
                    err.msg
                )
            else
                println(
                    "   Unhandled:",
                    "\n      ", err.msg,
                    "\n      ", err.T,
                    "\n      ", err.val
                )
            end
        else
            println(err)
        end

        println("\nExiting the program.\n")
        exit(0)
    end
end

"""
    get_server_information(client)

Print several settings and options of the running Carla server.

...
# Arguments
- `client::PyCall.PyObject <class carla.Client>`: The Carla client which is
    connected to the Carla server.
...
"""
function get_server_information(client::PyCall.PyObject)
    world = client.get_world()
    map = world.get_map()
    settings = world.get_settings()
    weather = world.get_weather()
    sync_mode = settings.synchronous_mode

    if (sync_mode)
        frame_rate = Formatting.format(
            Formatting.FormatExpr("{1:.2f}fps ({1:d}ms)"),
            1.0 / settings.fixed_delta_seconds,
            1000.0 * settings.fixed_delta_seconds
        )
    else
        frame_rate = "Variable"
    end

    # Get some Carla information
    println("Client Version: ", client.get_client_version())
    println("Map Name: ", map.name)
    println("Server Version: ", client.get_server_version())
    println("Server Settings: ")
    println("   Frame Rate: ", frame_rate)
    println("   No Render: ", settings.no_rendering_mode)
    println("   Sync mode: ", sync_mode)

    println("Weather: ")
    # println("   Cloudiness: ", weather.cloudiness)
    println("   Precip Deposits: ", weather.precipitation_deposits)
    println("   Precip Intensity: ", weather.precipitation)
    Formatting.printfmtln(
        Formatting.FormatExpr("   Sun Location (az, alt): ({}, {})"),
        weather.sun_azimuth_angle,
        weather.sun_altitude_angle
    )
    println("   Wind Intensity: ", weather.wind_intensity)
end