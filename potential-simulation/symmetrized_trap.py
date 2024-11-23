import os
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from trap import TTrap


def find_best_symmetric_potential(trap_wall:float = 190, trap_floor:float = 170,plot:bool=True, include_pulsing:bool=True, save:bool=True, verbose:int=0)->{float}:
    # prepare the trap object
    AEgIS_trap = TTrap(position=-1095)
    if verbose > 1:
        AEgIS_trap.Print()

    electrodes = AEgIS_trap.GetElectrodeNames()

    symmetric_wall_V = {'P13':trap_wall,'P12':trap_floor,'P11':trap_floor,'P10':trap_floor}
    full_wall_V = {}
    for electrode in electrodes:
        if electrode == 'P10':
            break
        full_wall_V[electrode] = trap_wall
    for key,value in symmetric_wall_V.items():
        AEgIS_trap.SetElectrodeV(key,value)
        full_wall_V[key] = value
    potentials = [full_wall_V]

    voltage_diff = trap_wall
    best_voltage = 0
    for i in range(0,100):
        V = trap_wall + i*0.05
        if verbose > 1:
            print(f"++++++  {V} V  ++++++")
        AEgIS_trap.SetElectrodeV('P9',V)
        AEgIS_trap.SetElectrodeV('P8',V)
        real_potential = AEgIS_trap.get_final_V()
        p11_voltage_id = int((AEgIS_trap._GetElectrode('P11').GetElectrodeCenter()-AEgIS_trap.position)/AEgIS_trap.dx)
        voltage_right = np.max(real_potential[:p11_voltage_id])
        voltage_left = np.max(real_potential[p11_voltage_id:])
        if np.abs(voltage_left - voltage_right) < voltage_diff:
            voltage_diff = np.abs(voltage_left - voltage_right)
            best_voltage = AEgIS_trap.GetElectrodeV("P8")
        if verbose > 2:
            print("max voltage right of the P11:",voltage_right)
            print("voltate at the center of the P11:",real_potential[p11_voltage_id])
            print("maxvoltage left of the P12",voltage_left)
    if verbose > 0:
        print("====================================")
        print("Best voltage at P8&9:",best_voltage,"V")
        print(f"\tdelta V: {voltage_diff:.3f} V")
    symmetric_wall_V['P9'] = best_voltage
    symmetric_wall_V['P8'] = best_voltage
    potentials.append(symmetric_wall_V)
    result = {'trap_floor':trap_floor,'trap_wall':trap_wall,'P9':best_voltage}
    
    if not plot:
        return result
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
    for i,potential_map in enumerate(potentials):
        AEgIS_trap.SetEverythingToZero()
        for electrode,V in potential_map.items():
            AEgIS_trap.SetElectrodeV(electrode,V)
        real_potential = AEgIS_trap.get_final_V()
        electrode_p8_V = AEgIS_trap.GetElectrodeV("P8")
        if i == 0:
            for axi in ax:
                axi.stairs(real_potential,label=f'full wall',color='tab:blue') #color='blue'
        else:
            if verbose > 0:
                print("++++++++++++++++")
                print(f"Ploting #{i} {electrode_p8_V} V")
            for axi in ax:
                axi.stairs(real_potential,label=f'P8@{electrode_p8_V} V',color='tab:orange')
            # pulsing loop
            if not include_pulsing:
                continue
            for pulse in range(1,8):
                AEgIS_trap.SetElectrodeV('P13',trap_wall - pulse*0.5*(trap_wall-trap_floor))
                for axi in ax:
                    axi.stairs(AEgIS_trap.get_final_V(),linestyle='--',label=f'pulsed P13 for -{0.5*pulse}*(wall-floor) V')

    ax[0].legend()
    if save:
        fig.savefig(os.path.join(os.path.dirname(__file__),'plots','symmetric_trap',f'floor={trap_floor:.1f}V_wall={trap_wall:.1f}V.png'))
    
    return result

if __name__ == "__main__":
    
    results = [find_best_symmetric_potential(trap_floor=trap_floor,trap_wall=190,save=False,plot=True)  for trap_floor in range(165,190,5)]
    for res in results:
        print(res)
    
    if False:
        results = [find_best_symmetric_potential(trap_floor=trap_floor,trap_wall=trap_wall,save=False,plot=False)  for trap_wall in range(170,190,5) for trap_floor in range(165,trap_wall)]
        wall_diff = []
        trap_depth = []
        trap_floors = []
        trap_walls = []
        p9=[]
        for res in results:
            p9.append(res['P9'])
            trap_floors.append(res['trap_floor'])
            trap_walls.append(res['trap_wall'])
            wall_diff.append(res['P9']-res['trap_wall'])
            trap_depth.append(res['trap_wall']-res['trap_floor'])
        
        # print(results)
        fig = plt.figure('relation')
        ax00 = fig.add_subplot(2,2,1)

        # p9 vs trap_wall
        ax00.plot(trap_walls,p9,'.')
        ax00.set_title('p9 vs trap floors')
        ax00.set_xlabel('set trap wall [V]')
        ax00.set_ylabel('set p9 [V]')

        # p9 vs trap depth
        ax10 = fig.add_subplot(2,2,2)
        ax10.plot(trap_depth,p9,'.')
        ax10.set_title('p9 vs trap depth')
        ax10.set_xlabel('set trap depth [V]')
        ax10.set_ylabel('set p9 [V]')

        # wall difference vs trap depth
        ax01 = fig.add_subplot(2,2,3)
        ax01.plot(trap_depth,wall_diff,'.')
        ax01.set_title('wall difference vs trap depth')
        ax01.set_xlabel('set trap depth [V]')
        ax01.set_ylabel('set wall difference [V]')

        # p9 vs trap floor and trap wall
        ax11 = fig.add_subplot(2,2,4,projection='3d')
        ax11.scatter(trap_floors,trap_walls,p9)
        ax11.set_title('p9 vs trap wall and floor')
        ax11.set_xlabel('set trap wall [V]')
        ax11.set_ylabel('set trap floor [V]')
        ax11.set_zlabel('set P9 [V]')


    # show the plots
    plt.show()