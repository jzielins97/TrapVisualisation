import os
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from trap import TTrap

# prepare the trap object
AEgIS_trap = TTrap(position=-1095)
AEgIS_trap.Print()

electrodes = AEgIS_trap.GetElectrodeNames()

trap_wall = 190
trap_floor = 180
potential = {'P13':trap_wall,'P12':trap_floor,'P11':trap_floor,'P10':trap_floor,'P9':191.5,'P8':191.5}
potentials = [potential]
full_potential = {}
for electrode in electrodes:
    if electrode == 'P10':
        break
    full_potential[electrode] = trap_wall
for key,value in potential.items():
    full_potential[key] = value
potentials.append(full_potential)
# for V in range(160,185,5):
#     potentials.append({key:value if key != 'P13' else V for key,value in potential.items()})


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
ax.set_ylim(130,200)
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
    p11_voltage_id = int((AEgIS_trap._GetElectrode('P11').GetElectrodeCenter()-AEgIS_trap.position)/AEgIS_trap.dx)
    print("max voltage right of the P11:",np.max(real_potential[:p11_voltage_id]))
    print("voltate at the center of the P11:",real_potential[p11_voltage_id])
    print("maxvoltage left of the P12",np.max(real_potential[p11_voltage_id:]))


# show the plot
plt.legend()
plt.show()