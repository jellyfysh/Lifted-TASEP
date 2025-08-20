import json
import math
import random
import matplotlib.pyplot as plt
import matplotlib.transforms

from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
import sys
import glob
cm = 1.0 / 2.56
fig, axs = plt.subplots(1, 3, figsize= (20 * cm , 8 * cm))

# 
# Make figure a (from scratch)
#

alpha = 0.5
exponent = 2.0
prefactor = 1.0

random.seed('Werner20')
NPart = 1000; NSites = 2 * NPart
NIter = int(prefactor * NPart ** exponent)
NStrob = NIter // 10000
Conf = [1] * NPart + [0] * (NSites - NPart)
Active = NPart - 1
while Conf[Active] != 1: Active = random.randint(0, NSites - 1)
ActPlot = []
ParabolaPlus = []
ParabolaMinus = []
IterPlot = []
for iter in range(NIter):
    NewActive = (Active + 1) % NSites
    if Conf[NewActive] == 0:
        Conf[Active], Conf[NewActive] = 0, 1
    Active = NewActive
    if  random.uniform(0.0, 1.0) < alpha:
        while True:
            Active = (Active - 1) % NSites
            if Conf[Active] == 1: break
    if iter % NStrob == 0:
        ActPlot.append(Active)
        IterPlot.append(iter)
        ParabolaPlus.append(NPart + math.sqrt(iter))
        ParabolaMinus.append(NPart - math.sqrt(iter))
x_values = [0,40,80,120,160]
y_values = [100000] * 5
axs[0].invert_yaxis()
#axs[0].plot(x_values, y_values, marker = 'o')
 
axs[0].xaxis.set_label_coords(0.5, -0.04)

axs[0].xaxis.set_label_coords(0.5, -0.04)
axs[0].text(0.05, 0.75, '$\\rho(x,t)\! =\! 1$',transform=axs[0].transAxes, 
bbox=dict(facecolor='white', alpha=0.5))
axs[0].text(0.95, 0.75, '$\\rho(x,t)\! =\! 0$',transform=axs[0].transAxes, 
bbox=dict(facecolor='white', alpha=0.5), horizontalalignment='right')
axs[0].xaxis.set_ticks([0, NPart, 2 * NPart], ['$0$', '' , '$L$'])
axs[0].yaxis.set_ticks([0, NIter], ['$0$', '$L^2/4$'])
axs[0].set_xlabel('$x, x_p$ (position)')
axs[0].set_ylabel('$\leftarrow$ $t$ (time) $\leftarrow$') 
axs[0].yaxis.set_label_coords(-0.04, 0.5)

axs[0].plot(ActPlot,IterPlot, label='pointer')
axs[0].fill_between(ParabolaMinus, IterPlot, color = 'red', alpha = 0.4)
axs[0].fill_between(ParabolaPlus, IterPlot, color = 'green', alpha = 0.4)
axs[0].plot(ParabolaMinus,IterPlot, label='pointer')
axs[0].plot(ParabolaPlus,IterPlot, label='pointer')
#axs[0].legend(loc='lower center')

# 
# Make figure b (from data on DATAFILES)
#

for filename in glob.glob("DATAFILES/LTASEPStep*.data"):
    FIELDS = filename.split("_")
    NPart = int(FIELDS[1])
    NSites = int(FIELDS[2])
    NRuns = int(FIELDS[3])
    infile = open(filename, "r")
    Density = json.loads(infile.readline())
    PDensity = json.loads(infile.readline())
    Texta = 'Lifted TASEP, $N=$ ' + str(NPart) + ', $L=$ ' + str(NSites) + ', $Nruns =$ ' + str(NRuns)
    for k in Density:
        time = float(k)
        if time < 50000000:
            XValues = [(l - NSites / 2) / math.sqrt(time) for l in range(NSites)]
            YValues = [Density[k][l] / NRuns for l in range(NSites)]
            axs[(1)].plot(XValues, YValues, label = '$t = $' + str(k))    



#axs[1].set_title(Texta)

axs[1].xaxis.set_ticks([-2, -1, 0, 1, 2], ['$-2$', '', '', '',  '$2$'])
axs[1].xaxis.set_label_coords(0.5, -0.04)
axs[1].yaxis.set_label_coords(-0.04, 0.5)
axs[1].yaxis.set_ticks([0, 0.25, 0.5, 0.75, 1.0], ['$0$', '', '', '',  '$1$'])
axs[1].plot([-1.0, 1.0], [0.5, 0.5], linewidth=0.1)    
axs[1].plot([-1.5, -0.5], [0.75, 0.75], linewidth=0.1)    
axs[1].plot([0.5, 1.5], [0.25, 0.25], linewidth=0.1)    
axs[1].plot([-1.0, -1.0], [0.5, 1.0], linewidth=0.1)    
axs[1].plot([1.0, 1.0], [0.0, 0.5], linewidth=0.1)    
axs[1].set_xlim(-2.0, 2.0)
axs[1].set_ylabel('$\\langle \\rho(x, t) \\rangle$, (average density)')
axs[1].set_xlabel('$(x-L/2) / \sqrt{t}$ (rescaled position)')

axs[1].legend(loc='lower left') 

# 
# Make figure c (from scratch)
#
random.seed('Werner20')
alpha = 0.5
exponent = 2.0
prefactor = 1.0
NPart = 1000; NSites = 2 * NPart
NIter = int(prefactor * NPart ** exponent)
NStrob = 1
Conf = [1] * NPart + [0] * (NSites - NPart)
Active = NPart - 1
while Conf[Active] != 1: Active = random.randint(0, NSites - 1)
Text = 'Periodic lifted TASEP, N= ' + str(NPart) + ', L= ' + str(NSites) + ', alpha= ' + str(alpha)
ActPlot = []
ParabolaPlus = []
ParabolaMinus = []
IterPlot = []
for iter in range(NIter):
    NewActive = (Active + 1) % NSites
    if Conf[NewActive] == 0:
        Conf[Active], Conf[NewActive] = 0, 1
    Active = NewActive
    if  random.uniform(0.0, 1.0) < alpha:
        while True:
            Active = (Active - 1) % NSites
            if Conf[Active] == 1: break
    if iter % NStrob == 0 and iter > 700000 and iter < 900000:
        ActPlot.append(Active)
        IterPlot.append(iter)
        ParabolaPlus.append(NPart + math.sqrt(iter))
        ParabolaMinus.append(NPart - math.sqrt(iter))
        if iter > 853124 and Active < NPart - math.sqrt(iter): print(Active, iter)

axs[2].yaxis.set_label_coords(-0.04, 0.5)
axs[2].xaxis.set_ticks([700000, 900000], ['$t_1$', '$t_2$'])
axs[2].yaxis.set_ticks([700000, 900000], ['$t_1$', '$t_2$'])
axs[2].xaxis.set_label_coords(0.5, -0.04)
axs[2].xaxis.set_ticks([0, 1000, 2000], ['$0$', '',  '$L$'])
axs[2].invert_yaxis()
axs[2].set_ylabel('$\leftarrow$ $t$ (time) $\leftarrow$') 
axs[2].set_xlabel('$x_p$ (pointer position)')

axs[2].plot(ActPlot,IterPlot, label='pointer')
axs[2].text(0.1, 0.50, '$\leftarrow x = L/2\! - \! \sqrt{t}$',transform=axs[2].transAxes)
axs[2].text(0.85, 0.90, '$x = L/2\! + \! \sqrt{t} \\rightarrow$',transform=axs[2].transAxes, horizontalalignment='right')
axs[2].plot(ParabolaMinus,IterPlot, label='pointer')
axs[2].plot(ParabolaPlus,IterPlot, label='pointer')
#axs[2].text(1919, 845124, '$\leftarrow$',horizontalalignment='left')
#axs[2].text(52, 898136, '$\\rightarrow$',horizontalalignment='right')


#ax.legend(loc='lower center')



plt.savefig('Triptych.pdf',bbox_inches="tight")
plt.show()
