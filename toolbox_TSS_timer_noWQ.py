# -*- coding: utf-8 -*-
# @Author: Brooke Mason
# @Date:   2020-01-15 09:57:05
# @Last Modified by:   Brooke Mason
# @Last Modified time: 2020-10-19 08:35:26

#Import time module
import time
startTime = time.time()

# Import required modules
from pyswmm import Simulation

#----------------------------------------------------------------------#

# Setup toolbox simulation
sim = Simulation("./modifiedMBDoyle_TSS_V2.inp")
sim.execute()

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
