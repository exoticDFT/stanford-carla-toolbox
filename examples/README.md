# Elaboration of the Examples

This page will try to elaborate on the example code contained in the examples
folder. The examples should already be commented some and the individual
functions should be fully documented. However, it is still useful to explain
what the sections in the example code are attempting to do.

## Example: `spawn-vehicle.jl`

The first section imports specific Julia packages the example needs for using
the toolbox. In general, these lines will be used in almost all Julia code
you create that uses the toolbox. Let's explain:

Line 1: Imports this toolbox to be used within your Julia code.
<br>
Line 2: Imports the PyCall package, which is used to call Python within Julia.
<br>
Line 4: This is a helper variable that will simplify the functional calls to the
toolbox, so that you do not need to write the full package name every time you
want to use a function within the toolbox.

```julia
1 import StanfordCarlaToolbox
2 import PyCall
3
4 SCT = StanfordCarlaToolbox
```
