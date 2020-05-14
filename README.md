# stanford-carla-toolbox

[![Build Status](https://travis-ci.org/exoticdt/stanford-carla-toolbox.svg?branch=feature/code_coverage)](https://travis-ci.org/github/exoticDFT/stanford-carla-toolbox?branch=feature/code_coverage)
[![Coverage Status](https://codecov.io/gh/exoticDFT/stanford-carla-toolbox/badge.svg?branch=feature/code_coverage)](https://codecov.io/gh/exoticDFT/stanford-carla-toolbox?branch=feature/code_coverage)

A toolbox for the [Carla Simulator](http://carla.org/).

This toolbox is a collection of useful C++, Python and Julia wrappers for
working with the Carla Simulator and other autonomous driving libraries and
packages.

## Prerequisites

These are the required prerequisites necessary for using the toolbox. A list of
general requirements and well as extras for the desired coding language.

* Carla Simulator ([0.9.7](https://github.com/carla-simulator/carla/releases/tag/0.9.7))
* Python (3.5) - Carla only provides API binaries for Python 3.5.
* Julia (1.2+)

### Carla

The code has been verified to work with version 0.9.7 of the Carla simulator.
For more information on using the Carla simulator, please visit the Carla
[documentation](https://carla.readthedocs.io/en/latest/),
[forum](https://forum.carla.org/),
[Discord server](https://discord.gg/8kqACuC) and
[GitHub page](https://github.com/carla-simulator/carla).

### Python

The toolbox extensively utilizes the
[Carla PythonAPI](https://carla.readthedocs.io/en/latest/python_api/) for
interacting with the Carla simulator.

* Carla PythonAPI egg - Found in the `PythonAPI/carla/dist/` directory of the
  Carla simulator binary above. See
  ["Setting Up Your Environment"](Setup.md#setting-up-your-environment).

### Julia

The Julia codebase for this toolbox has only been tested directly for version
1.3 of Julia. Since Carla doesn't provide direct Julia support, this wrapper
currently uses their provided Python API. Please make sure your environment is
setup to load the Carla provided .egg file.

* AutomotiveSimulator.jl
* PyCall.jl

## Using the Toolbox

In order to use the toolbox, you must first have the above
[prerequisites](#prerequisites) installed on your system and follow the
instructions provided in
["Setting Up Your Environment"](Setup.md#setting-up-your-environment).

Before running any code that uses the toolbox, we must have a instance of the
Carla server running. Open a terminal with the appropriate environment and run:

```bash
~/Simulators/Carla-0.9.7/./CarlaUE4.sh
```

Next, open another terminal (or tab) with the appropriate environment and run
your code using the toolbox. Below is a simple Julia program that will connect
to a running Carla server and spawn a vehicle in the simulator.

```bash
julia --project=~/Development/VirtualEnvironments/Julia/sct-testing \
~/Development/stanford-carla-toolbox/examples/spawn-vehicle.jl
```

This example only provides a brief look at the functionality of the toolbox. For
further examples, look under the `examples` directory.