# Setting Up Your Environment

Before using the toolbox, you must setup your environment. In order to use all
the toolbox's functionality, you must follow the entire procedure. More
information for setting up Julia and Python environments can be found online.
These instructions are to get you going in the same development environment the
toolbox was created. All instructions assume you have already downloaded and
extracted the Carla Binaries and installed the correct versions of Julia and
Python found under the [prerequisites section.](README.md#prerequisites)

> ***Note:** This setup assumes you are working on a Linux machine.*

## Carla Binaries

We'll assume the binary has been extracted to the location
`~/Simulators/Carla-0.9.7`. If you have extracted the binaries to another
location, simply replace this location with yours.

## Python

In order to use the Carla PythonAPI, you must update the PYTHONPATH environment
variable to include the correct egg file. in order to do this simply add the
following line to your `~/.bashrc` file or run the command directly in the
terminal you will be interacting with the toolbox.

```bash
export PYTHONPATH=~/Simulators/Carla-0.9.7/PythonAPI/carla/dist/carla-0.9.7-py3.5-linux-x86_64.egg:$PYTHONPATH
```

> ***Note:* Adding the line to your `~/.bashrc` file will load this path on every new
terminal instance, but will be persistent for any other Python REPL.*

## Julia

You can setup your Julia environment to constantly update to the working
directory of this toolbox. In other words, if you make changes in this repo
locally, they will be present in the next run of any Julia program using the
toolbox. The following is how the environment was setup during development.
Once again, it is assumed the locations referenced exist on your system. If you
would like to use different locations, simply update the location with your
preference.

```bash
julia
] activate ~/Development/VirtualEnvironments/Julia/sct-testing
] dev ~/Development/stanford-carla-toolbox
] add AutomotiveSimulator
] add PyCall
```

This will create a "virtual environment" specifically for development, testing
or just using the toolbox in the state cloned from GitHub.