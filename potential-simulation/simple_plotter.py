import os
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from trap import TTrap

potential = {'P13':190,'P12':185,'P11':185,'P10':185,'P9':191.5,'P8':191.5}
potentials = [potential]
# for V in range(160,185,5):
#     potentials.append({key:value if key != 'P13' else V for key,value in potential.items()})



# prepare the trap object
AEgIS_trap = TTrap(position=-1095)
AEgIS_trap.Print()

# prepare the plot
fig = plt.figure(1)
ax = fig.subplots()
ax.set_xticks(AEgIS_trap.GetLabelPositions())
ax.set_xticks(AEgIS_trap.GetMinorLabelPositions(),minor=True)
ax.set_xticklabels(AEgIS_trap.GetElectrodeNames())
ax.grid(axis='x',which='minor',linestyle = "dashed",linewidth = 0.5,alpha=0.5)
ax.tick_params(which = "minor", bottom = False, left = False)
ax.set_xlabel("electrode")
ax.set_ylabel("voltage [V]") 
ax.set_ylim(0,200)
ax.set_xlim((AEgIS_trap.GetElectrodePosition('P7')-AEgIS_trap.position)/AEgIS_trap.dx,(AEgIS_trap.GetElectrodePosition('P14')-AEgIS_trap.position)/AEgIS_trap.dx)
plt.xticks(rotation=45)

# plotting loop
for i,potential_map in enumerate(potentials):
    print(f"Ploting #{i}")
    AEgIS_trap.SetEverythingToZero()
    for electrode,V in potential_map.items():
        AEgIS_trap.SetElectrodeV(electrode,V)
    real_potential = AEgIS_trap.get_final_V()
    ax.stairs(real_potential,label=f'P13@{AEgIS_trap.GetElectrodeV("P13")} V')


# show the plot
plt.legend()
plt.show()