# -*- coding: utf-8 -*-
# @Author: Brooke Mason
# @Date:   2020-01-15 09:57:05
# @Last Modified by:   Brooke Mason
# @Last Modified time: 2020-10-21 09:19:34

#Import time module
import time
startTime = time.time()

# Import required modules
from pyswmm import Simulation, Nodes, Links
from wq_toolbox.links import Link_Quality
from wq_toolbox.nodes import Node_Quality

# Make dictionaries for each water quality method
# Gravity Settling in Basins
# site mainly loam soil so Ss ~ 1.6 and d50 ~ 0.04
# v_s found to fit this data v_s ~ 0.0005 m/s = 1.8 m/hr = 5.9 ft/hr)
# C_s from Mallets Creek data
dict1 = {'93-50408': {0: [5.9, 21.0]},'93-50404': {0: [5.9, 21.0]}, \
         '93-49759': {0: [5.9, 21.0]}}

# Channel Erosion & Gravity Settling
# width parameter changed to match Mallet's Creek load
# So from site data in SWMM model
# w tweaked until get conc in the correct range from Mallet's Creek data
dict2 = {'95-69044': {0: [0.00000004, 0.0807, 1.6, 0.04, 5.9, 21.0]}, \
         '95-70180': {0: [0.00000004, 0.0411, 1.6, 0.04, 5.9, 21.0]}, \
         '95-51776': {0: [0.00000004, 0.0582, 1.6, 0.04, 5.9, 21.0]}, \
         '95-51774': {0: [0.00000004, 0.1333, 1.6, 0.04, 5.9, 21.0]}, \
         '95-51634': {0: [0.00000004, 0.1695, 1.6, 0.04, 5.9, 21.0]}, \
         '95-69048': {0: [0.00000004, 0.0368, 1.6, 0.04, 5.9, 21.0]}, \
         '95-70594': {0: [0.00000004, 1.7213, 1.6, 0.04, 5.9, 21.0]}, \
         '95-51760': {0: [0.00000004, 3.7373, 1.6, 0.04, 5.9, 21.0]}, \
         '95-69050': {0: [0.00000004, 0.1379, 1.6, 0.04, 5.9, 21.0]}, \
         '95-51758': {0: [0.00000004, 0.3719, 1.6, 0.04, 5.9, 21.0]}, \
         '95-51757': {0: [0.00000004, 0.0497, 1.6, 0.04, 5.9, 21.0]}, \
         '95-70713': {0: [0.00000004, 1.8003, 1.6, 0.04, 5.9, 21.0]}, \
         '95-70277': {0: [0.00000004, 0.3756, 1.6, 0.04, 5.9, 21.0]}}

#----------------------------------------------------------------------#

# Setup toolbox simulation
with Simulation("./TSS.inp") as sim:
    # Setup toolbox methods
    GS = Node_Quality(sim, dict1)
    ER_GS = Link_Quality(sim, dict2)
    
    # Step through the simulation    
    for index,step in enumerate(sim):

        # Calculate gravity settling in basins
        GS.GravitySettling()
        # Calculate erosion andn gravity settling in channels
        ER_GS.Erosion_and_Settling()

    sim._model.swmm_end()

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
