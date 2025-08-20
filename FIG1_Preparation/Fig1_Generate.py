import json
import math
import random
import sys
alpha = 0.5
exponent = 2.0
prefactor = 1.0
NPart = 10000; NSites = 2 * NPart
NIter = 100000
Text = 'Periodic lifted TASEP, N= ' + str(NPart) + ', L= ' + str(NSites) + ', alpha= ' + str(alpha)
Density = {}
PDensity = {}
NRuns = 50000
for nconf in range(NRuns):
    NStrob = 100
    Conf = [1] * NPart + [0] * (NSites - NPart)
    Active = NPart - 1  # We know that this site is occupied
    if Conf[Active] == 0: sys.exit('Particle not active')
    for iter in range(NIter):
        NewActive = (Active + 1) % NSites
        if Conf[NewActive] == 0:
            Conf[Active], Conf[NewActive] = 0, 1
        Active = NewActive
        if  random.uniform(0.0, 1.0) < alpha:
            while True:
                Active = (Active - 1) % NSites
                if Conf[Active] == 1: break
        if iter + 1 == NStrob :
            NStrob *= 10
            Offset = 0
            if iter + 1 not in Density: Density[iter + 1] = [0] * NSites
            for k in range(NSites):
                if Conf[k] != 0 and Active !=k: Density[iter + 1][k - Offset] += 1
                elif Active == k: Offset = 1
            if iter + 1 not in PDensity: PDensity[iter + 1] = [0] * NSites
            PDensity[iter + 1][Active] += 1


filename = "DATAFILES/LTASEPStep_" + str(NPart) + '_' + str(NSites) + '_' + str(NRuns) +  "_.data"
with open(filename, 'w') as file:
     file.write(json.dumps(Density)) 
     file.write('\n')
     file.write(json.dumps(PDensity))
