# TSS SWMM Simulations
Python scripts for running TSS simulations for StormReactor research article. 

## Files
1. TSS.inp: SWMM input file for TSS simulations based on real-world inspired stormwater network.
2. TSS_SWMMcheck.inp: SWMM input file for running gravity settling in SWMM.
3. toolbox_TSS.py: Primary Python script used for all TSS methods run for StormReactor research paper.
4. TSScheck_erosion.py: Python script for checking mass balance for StormReactor's erosion method.
5. TSScheck_settling.py: Python script for comparing SWMM's gravity settling to StormReactor's gravity settling method.
6. toolbox_TSS_time.py: Python script to check time requirement for running the TSS simulation.
7. toolbox_TSS_time_noWQ.py: Python script to check time requirement for running the simulation without the TSS module.

## License
GNU General Public License v3.0

## Status
These Python Scripts use wq_toolbox, the prerequisite package to StormReactor. These files will be updated once StormReactor is finalized.
