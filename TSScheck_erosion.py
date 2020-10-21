# -*- coding: utf-8 -*-
# @Author: Brooke Mason
# @Date:   2020-06-04 16:30:20
# @Last Modified by:   Brooke Mason
# @Last Modified time: 2020-10-20 16:08:07

# -*- coding: utf-8 -*-
# @Author: Brooke Mason
# @Date:   2020-01-15 09:57:05
# @Last Modified by:   Brooke Mason
# @Last Modified time: 2020-06-04 16:29:33

# Import required modules
from pyswmm import Simulation, Nodes, Links
from wq_toolbox.links import Link_Quality
from wq_toolbox.nodes import Node_Quality
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error as mse

# Make dictionaries for each water quality method
# Channel Erosion & Gravity Settling
# width parameter changed to match Mallet's Creek load
# Slope from SWMM model
# SS and d50 found to match v_s, v_s and C_s same as bove
dict2 = {'95-69044': {0: [0.0000005, 0.0807, 2.68, 0.04, 17.29, 21.0]}, \
         '95-70180': {0: [0.0000005, 0.0411, 2.68, 0.04, 17.29, 21.0]}, \
         '95-51776': {0: [0.0000005, 0.0582, 2.68, 0.04, 17.29, 21.0]}, \
         '95-51774': {0: [0.0000005, 0.1333, 2.68, 0.04, 17.29, 21.0]}, \
         '95-51634': {0: [0.0000005, 0.1695, 2.68, 0.04, 17.29, 21.0]}, \
         '95-69048': {0: [0.0000005, 0.0368, 2.68, 0.04, 17.29, 21.0]}, \
         '95-70594': {0: [0.0000005, 1.7213, 2.68, 0.04, 17.29, 21.0]}, \
         '95-51760': {0: [0.0000005, 3.7373, 2.68, 0.04, 17.29, 21.0]}, \
         '95-69050': {0: [0.0000005, 0.1379, 2.68, 0.04, 17.29, 21.0]}, \
         '95-51758': {0: [0.0000005, 0.3719, 2.68, 0.04, 17.29, 21.0]}, \
         '95-51757': {0: [0.0000005, 0.0497, 2.68, 0.04, 17.29, 21.0]}, \
         '95-70713': {0: [0.0000005, 1.8003, 2.68, 0.04, 17.29, 21.0]}, \
         '95-70277': {0: [0.0000005, 0.3756, 2.68, 0.04, 17.29, 21.0]}}

Wetland_conc = []
Wetland_outflow = []
Wetland_cumload = []

Channel_conc = []
Channel_flow = []
Channel_cumload = []

Outfall_inflow = []
Outfall_conc = []
Outfall_cumload = []

# Setup toolbox simulation
with Simulation("./modifiedMBDoyle_TSS_V2.inp") as sim:
    # Setup toolbox methods
    ER = Link_Quality(sim, dict2)
    # Get asset information
    Wetland = Nodes(sim)["93-49759"]
    Channel = Links(sim)["95-70277"]
    Outfall = Nodes(sim)["97-50253"]

    # Step through the simulation    
    for step in enumerate(sim):

        # Calculate erosion produced
        ER.Erosion()

        # Get TSS conc for each asset        
        Wt_p = Wetland.pollut_quality['TSS']
        Wetland_conc.append(Wt_p)
        Ch_p = Channel.pollut_quality['TSS']
        Channel_conc.append(Ch_p)
        Of_p = Outfall.pollut_quality['TSS']
        Outfall_conc.append(Of_p)

        Wt_of = Wetland.total_outflow
        Wetland_outflow.append(Wt_of)
        Ch_f = Channel.flow
        Channel_flow.append(Ch_f)
        Of_if = Outfall.total_inflow
        Outfall_inflow.append(Of_if)
    
    sim._model.swmm_end()
    print(sim.runoff_error)
    print(sim.flow_routing_error)
    print(sim.quality_error)

# Convert flow rate from cfs to m3/s
conv_cfs_cms = [0.02832]*len(Channel_flow)
Wetland_flow_m = [a*b for a,b in zip(Wetland_outflow,conv_cfs_cms)]
Channel_flow_m = [a*b for a,b in zip(Channel_flow,conv_cfs_cms)]
Outfall_flow_m = [a*b for a,b in zip(Outfall_inflow,conv_cfs_cms)]

# Calculate load each timestep
conv_mgs_kgs = [0.000001]*len(Wetland_outflow)
conv_cfs_cms = [0.02832]*len(Wetland_outflow)
timestep = [5]*len(Wetland_outflow)
Wetland_load = [a*b*c*d*e for a,b,c,d,e in zip(Wetland_conc,Wetland_outflow,conv_cfs_cms, conv_mgs_kgs,timestep)]
Channel_load = [a*b*c*d*e for a,b,c,d,e in zip(Channel_conc,Channel_flow,conv_cfs_cms, conv_mgs_kgs,timestep)]
Outfall_load = [a*b*c*d*e for a,b,c,d,e in zip(Outfall_conc,Outfall_inflow,conv_cfs_cms,conv_mgs_kgs,timestep)]

# Calculate cumulative load
Wetland_cumload = np.cumsum(Wetland_load)
Channel_cumload = np.cumsum(Channel_load)
Outfall_cumload = np.cumsum(Outfall_load)

#----------------------------------------------------------------------#
# Calculate error
Conc_error = mse(Channel_conc, Outfall_conc)
Flow_error = mse(Channel_flow, Outfall_inflow)
Load_error = mse(Channel_load, Outfall_load)
print("Concentration Error", Conc_error)
print("Flow Error", Flow_error)
print("Load Error", Load_error)

#----------------------------------------------------------------------#
# Plot Result
fig, ax = plt.subplots(3, 1, sharex=True)
ax[0].plot(Wetland_conc, color='#B08CA1', linewidth=2, label='Wetland')
ax[0].plot(Channel_conc, '--', color='#695580', linewidth=2, label='Channel')
ax[0].plot(Outfall_conc, ':', color='#818282', linewidth=2, label='Outfall')
ax[0].set_xlim(0,86400)
ax[0].set_xticks([0,17280,34560,51840,69120,86400])
ax[0].set_ylabel("TSS Conc (mg/L)")
ax[1].plot(Wetland_outflow, color='#B08CA1', linewidth=2, label='Wetland')
ax[1].plot(Channel_flow, '--', color='#695580', linewidth=2, label='Channel')
ax[1].plot(Outfall_inflow,':', color='#818282', linewidth=2, label='Outfall')
ax[1].set_xlim(0,86400)
ax[1].set_xticks([0,17280,34560,51840,69120,86400])
ax[1].set_ylabel("Flow (m³/s)")
ax[2].set_xlim(0,86400)
ax[2].set_xticks([0,17280,34560,51840,69120,86400])
ax[2].set_xticklabels(["0","1","2","3","4","5"])
ax[2].plot(Wetland_cumload, color='#B08CA1', linewidth=2, label='Wetland')
ax[2].plot(Channel_cumload, '--', color='#695580', linewidth=2, label='Channel')
ax[2].plot(Outfall_cumload,':', color='#818282', linewidth=2, label='Outfall')
ax[2].set_xlabel("Time (days)")
ax[2].set_ylabel("Cum. Load (kg)")

plt.legend()
plt.savefig('ErosionApdx.jpeg',dpi=300)
