# -*- coding: utf-8 -*-
# @Author: Brooke Mason
# @Date:   2020-01-15 09:57:05
# @Last Modified by:   Brooke Mason
# @Last Modified time: 2020-10-21 09:22:02

# Import required modules
from pyswmm import Simulation, Nodes, Links
from wq_toolbox.links import Link_Quality
from wq_toolbox.nodes import Node_Quality
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as mse

# Make dictionaries for each water quality method# Gravity Settling in Basins
# v_s based on Mallet Creek data (0.0015 m/s = 5.27 m/hr = 17.29 ft/hr), C_s from Mallets Creek data
dict1 = {'93-50408': {0: [17.29, 21.0]},'93-50404': {0: [17.29, 21.0]}, \
         '93-49759': {0: [17.29, 21.0]}}

# Lists to store results
Ellsworth_conc = []
Ellsworth_outflow = []
Ellsworth_cumload = []

DBasin_conc = []
DBasin_outflow = []
DBasin_cumload = []

Wetland_conc = []
Wetland_outflow = []
Wetland_cumload = []


# Setup toolbox simulation
with Simulation("./TSS.inp") as sim:
    # Setup toolbox methods
    GS = Node_Quality(sim, dict1)
    # Get asset information
    Ellsworth = Nodes(sim)["93-50408"]
    Doyle_Basin = Nodes(sim)["93-50404"]
    Wetland = Nodes(sim)["93-49759"]

    # Step through the simulation    
    for step in enumerate(sim):

        # Calculate gravity settling 
        GS.GravitySettling()

        # Get TSS conc for each asset        
        Ell_p = Ellsworth.pollut_quality['TSS']
        Ellsworth_conc.append(Ell_p)
        DB_p = Doyle_Basin.pollut_quality['TSS']
        DBasin_conc.append(DB_p)
        Wt_p = Wetland.pollut_quality['TSS']
        Wetland_conc.append(Wt_p)

        # Get data for each asset
        Ell_of = Ellsworth.total_outflow
        Ellsworth_outflow.append(Ell_of)
        DB_of = Doyle_Basin.total_outflow
        DBasin_outflow.append(DB_of)
        Wt_of = Wetland.total_outflow
        Wetland_outflow.append(Wt_of)

    sim._model.swmm_end()
    print(sim.runoff_error)
    print(sim.flow_routing_error)
    print(sim.quality_error)

# Calculate load each timestep
conv_mgs_kgs = [0.000001]*len(Ellsworth_outflow)
conv_cfs_cms = [0.02832]*len(Ellsworth_outflow)
timestep = [5]*len(Ellsworth_outflow)
Ellsworth_load = [a*b*c*d*e for a,b,c,d,e in zip(Ellsworth_conc,Ellsworth_outflow,conv_cfs_cms, conv_mgs_kgs,timestep)]
DBasin_load = [a*b*c*d*e for a,b,c,d,e in zip(DBasin_conc,DBasin_outflow,conv_cfs_cms,conv_mgs_kgs,timestep)]
Wetland_load = [a*b*c*d*e for a,b,c,d,e in zip(Wetland_conc,Wetland_outflow,conv_cfs_cms, conv_mgs_kgs,timestep)]

# Calculate cumulative load
Ellsworth_cumload = np.cumsum(Ellsworth_load)
DBasin_cumload = np.cumsum(DBasin_load)
Wetland_cumload = np.cumsum(Wetland_load)
        
#----------------------------------------------------------------------#
# Confirm gravity settling matches toolbox simulation

# Lists to store results
Ellsworth_concS = []
Ellsworth_outflowS = []
Ellsworth_cumloadS = []

DBasin_concS = []
DBasin_outflowS = []
DBasin_cumloadS = []

Wetland_concS = []
Wetland_outflowS = []
Wetland_cumloadS = []

# Setup toolbox simulation
with Simulation("./TSS_SWMMcheck.inp") as sim:
    # Get asset information
    Ellsworth = Nodes(sim)["93-50408"]
    Doyle_Basin = Nodes(sim)["93-50404"]
    Wetland = Nodes(sim)["93-49759"]
    # Step through the simulation    
    for step in sim:
        # Get TSS conc for each asset        
        Ell_p = Ellsworth.pollut_quality['TSS']
        Ellsworth_concS.append(Ell_p)
        DB_p = Doyle_Basin.pollut_quality['TSS']
        DBasin_concS.append(DB_p)
        Wt_p = Wetland.pollut_quality['TSS']
        Wetland_concS.append(Wt_p)

        # Get data for each asset
        Ell_of = Ellsworth.total_outflow
        Ellsworth_outflowS.append(Ell_of)
        DB_of = Doyle_Basin.total_outflow
        DBasin_outflowS.append(DB_of)
        Wt_of = Wetland.total_outflow
        Wetland_outflowS.append(Wt_of)

    sim._model.swmm_end()
    print(sim.runoff_error)
    print(sim.flow_routing_error)
    print(sim.quality_error)

# Calculate load each timestep
Ellsworth_loadS = [a*b*c*d*e for a,b,c,d,e in zip(Ellsworth_conc,Ellsworth_outflow,conv_cfs_cms, conv_mgs_kgs,timestep)]
DBasin_loadS = [a*b*c*d*e for a,b,c,d,e in zip(DBasin_conc,DBasin_outflow,conv_cfs_cms,conv_mgs_kgs,timestep)]
Wetland_loadS = [a*b*c*d*e for a,b,c,d,e in zip(Wetland_conc,Wetland_outflow,conv_cfs_cms, conv_mgs_kgs,timestep)]

# Calculate cumulative load
Ellsworth_cumloadS = np.cumsum(Ellsworth_loadS)
DBasin_cumloadS = np.cumsum(DBasin_loadS)
Wetland_cumloadS = np.cumsum(Wetland_loadS)

#----------------------------------------------------------------------#
# Calculate error
Ells_error = mse(Ellsworth_load, Ellsworth_loadS)
DB_error = mse(DBasin_load, DBasin_loadS)
Wt_error = mse(Wetland_load, Wetland_loadS)
print("Ellsworth Error", Ells_error)
print("DBasin Error", DB_error)
print("Wetland Error", Wt_error)

#----------------------------------------------------------------------#
# Plot Result
fig, ax = plt.subplots(1, 3, sharex=True)
ax[0].set_title("Detention Basin")
ax[0].plot(Ellsworth_cumload, color='#6CC6D1', linewidth=2)
ax[0].plot(Ellsworth_cumloadS, "k--", linewidth=2)
ax[0].set_xlim(0,86400)
ax[0].set_xticks([0,17280,34560,51840,69120,86400])
ax[0].set_xticklabels(["0","1","2","3","4","5"])
ax[0].set_xlabel("Time (days)")
ax[0].set_ylabel("Cumulative Load (kg)")
ax[1].set_title("Retention Basin")
ax[1].plot(DBasin_cumload, color='#3B4D7A', linewidth=2)
ax[1].plot(DBasin_cumloadS, "k--", linewidth=2)
ax[1].set_xlim(0,86400)
ax[1].set_xticks([0,17280,34560,51840,69120,86400])
ax[1].set_xticklabels(["0","1","2","3","4","5"])
ax[1].set_xlabel("Time (days)")
ax[2].set_title("Wetland")
ax[2].set_xlim(0,86400)
ax[2].set_xticks([0,17280,34560,51840,69120,86400])
ax[2].set_xticklabels(["0","1","2","3","4","5"])
ax[2].plot(Wetland_cumload, color='#B08CA1', linewidth=2)
ax[2].plot(Wetland_cumloadS, "k--", linewidth=2)
ax[2].set_xlabel("Time (days)")
plt.show()
