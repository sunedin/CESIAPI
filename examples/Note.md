# Notes:

### CallSimulationScripts.ipynb

For matlab, there is no built-in object type of mathmatical programming 'model', 'set', 'parameter'. Therefore, it is not feasible to use method such as .getParams() etc.

The interface support calling user-script matlab functions, and return values as python dictionary data type.

#### CallPlanMod.ipynb

For JuMP, in order to get values of JumP variables and constraints, use above syntax which involves a bit raw julia statement.
