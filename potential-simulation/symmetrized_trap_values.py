import os
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from trap import TTrap
import pandas as pd


def find_best_symmetric_potential(trap_wall:float = 190, trap_floor:float = 170, verbose:int=0)->pd.DataFrame:
    # prepare the trap object
    AEgIS_trap = TTrap(position=-1095)
    if verbose > 1:
        AEgIS_trap.Print()

    symmetric_wall_V = {'P13':trap_wall,'P12':trap_floor,'P11':trap_floor,'P10':trap_floor,'P9':192.05,'P8':192.05}
    for key,value in symmetric_wall_V.items():
        AEgIS_trap.SetElectrodeV(key,value)
    potentials = [symmetric_wall_V]

    electrodes = pd.DataFrame()
    electrodes['label'] = AEgIS_trap.GetElectrodeNames()
    electrodes['start'] = [AEgIS_trap._GetElectrode(e).GetElectrodeStart() for e in electrodes['label']]
    electrodes['center'] = [AEgIS_trap._GetElectrode(e).GetElectrodeCenter() for e in electrodes['label']]
    electrodes['end'] = [AEgIS_trap._GetElectrode(e).GetElectrodeEnd() for e in electrodes['label']]
    electrodes = electrodes.set_index('label')
    electrodes.to_csv('electrodes.csv')
    
    # prepare the plot
    fig = plt.figure(f'floor={trap_floor} V & wall={trap_wall} V',figsize=(18,9),layout='tight')
    ax = fig.subplots(1,2)
    for i,axi in enumerate(ax):
        axi.set_xticks(AEgIS_trap.GetLabelPositions())
        axi.set_xticks(AEgIS_trap.GetMinorLabelPositions(),minor=True)
        axi.set_xticklabels(AEgIS_trap.GetElectrodeNames())
        axi.grid(axis='x',which='minor',linestyle = "dashed",linewidth = 0.5,alpha=0.5)
        axi.tick_params(which = "minor", bottom = False, left = False)
        axi.set_xlabel("electrode")
        axi.set_ylabel("voltage [V]")
        if i == 0:
            axi.set_title(f'floor={trap_floor} V & wall={trap_wall} V')
            axi.set_ylim(0,200)
        else:
            axi.set_title(f'ZOOM')
            axi.set_ylim(trap_floor-5,trap_wall+5)
        axi.set_xlim((AEgIS_trap.GetElectrodePosition('P7')-AEgIS_trap.position)/AEgIS_trap.dx,(AEgIS_trap.GetElectrodePosition('P14')-AEgIS_trap.position)/AEgIS_trap.dx)
    plt.xticks(rotation=45)

    # plotting loop
    data = pd.DataFrame()
    for i,potential_map in enumerate(potentials):
        AEgIS_trap.SetEverythingToZero()
        for electrode,V in potential_map.items():
            AEgIS_trap.SetElectrodeV(electrode,V)
        real_potential = AEgIS_trap.get_final_V()
        data['position'] = [AEgIS_trap.position + AEgIS_trap.dx*j for j in range(len(real_potential))]
        data['full'] = real_potential
        electrode_p8_V = AEgIS_trap.GetElectrodeV("P8")
        for axi in ax:
            axi.stairs(real_potential,label=f'P8@{electrode_p8_V} V',color='m') # tab:orange
        # pulsing loop
        for pulse in range(trap_wall,0,-10):
            AEgIS_trap.SetElectrodeV('P13',trap_wall - pulse) 
            real_potential = AEgIS_trap.get_final_V()
            data[f'{pulse} V'] = real_potential
            for axi in ax:
                axi.stairs(AEgIS_trap.get_final_V(),linestyle='--',label=f'pulsed P13 for {pulse} V')
    ax[0].legend()
    return data

if __name__ == "__main__":
    
    results = [find_best_symmetric_potential(trap_floor=trap_floor,trap_wall=190)  for trap_floor in [180]] # range(165,190,5)
    for res in results:
        print(res)
        res.to_csv('pulsing.csv')


    # show the plots
    plt.show()