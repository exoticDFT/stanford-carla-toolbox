# stanford-carla-toolbox
A toolbox for the Carla Simulator.

This toolbox is a collection of useful C++, Python and Julia wrappers for
working with the Carla Simulator and other autonomous driving libraries and
packages.


## Prerequisites
These are the required prerequisites necessary for using the toolbox. A list of
general requirements and well as extras for the desired coding language.

* Carla Simulator (0.9.7)
* 

### Julia
Code has only been tested directly for version 1.3. Since Carla doesn't provide
direct Julia support, this wrapper currently uses their provided Python API.
Please make sure your environment is setup to load the Carla provided .egg file.

* AutomotiveSimulator.jl
* Formatting.jl
* PyCall.jl
* Python (3.5) - This is necessary as Carla only provides egg files for 2.7 and 3.5.