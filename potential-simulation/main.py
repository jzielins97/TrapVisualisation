import trap
from IPython import display
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np


def PrepareHVTrapShaping(AEgIS_trap:trap.TTrap):
    AEgIS_trap.FastReshapeMalmberg("nested_trap", -14000, 0, -14000, "HV_ON")
    AEgIS_trap.FastReshape("nested_trap", "inlet",0,"HV3_OFF")
    AEgIS_trap.SlowReshape("nested_trap", "outlet",-14000,0,None,10,"HV1_OFF" )

def PrepareNestedTrapShaping(AEgIS_Trap:trap.TTrap, TrapFloor, TrapWall, SqueezeTime, TrapType, SqueezeType):
        print("Preparing DMA for nested traps ...")
        # Ion catching traps
        if TrapType == 'Standard':
            AEgIS_Trap.FastReshapeMalmberg("nested_trap", TrapWall, TrapFloor, TrapWall, "NestedTrap_On")
        elif TrapType == 'Valts':
            AEgIS_Trap.FastReshapeMalmberg("nested_trap", -TrapWall, -TrapWall, -TrapWall, "NestedTrap_On")
            #AEgIS_Trap.FastReshapeMalmberg(self, "nested_trap", TrapWall, -TrapWall, TrapWall, "NestedTrap_Valts_2")
            #AEgIS_Trap.FastReshapeMalmberg(self, "nested_trap", TrapWall, TrapFloor, TrapWall, "NestedTrap_Valts_3")
            AEgIS_Trap.SlowReshapeMalmberg("nested_trap", -TrapWall, TrapWall, -TrapWall, -TrapWall, -TrapWall, TrapWall, 4, 100, "NestedTrap_Valts_slow1to2")
            AEgIS_Trap.SlowReshapeMalmberg("nested_trap", TrapWall, TrapWall, -TrapWall, TrapFloor, TrapWall, TrapWall, 4, 100, "NestedTrap_Valts_slow2to3")
            print("Valts rules ...")
        else:
            print('Wrong trap name!')

        # Ion squeezing traps
        if SqueezeType == 'None':
            pass
        elif SqueezeType == '2E_MCP':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "2E_MCP", TrapFloor, TrapWall, SqueezeTime, 100, "NestedTrap_Squeeze")
        elif SqueezeType == '4E_MCP':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "4E_MCP", TrapFloor, TrapWall, SqueezeTime, 100, "NestedTrap_Squeeze")
        elif SqueezeType == '6E_MCP':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "6E_MCP", TrapFloor, TrapWall, SqueezeTime, 100, "NestedTrap_Squeeze")
        elif SqueezeType == '8E_MCP':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "8E_MCP", TrapFloor, TrapWall, SqueezeTime, 100, "NestedTrap_Squeeze")
        elif SqueezeType == 'Half_MCP':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "Half_MCP", TrapFloor, TrapWall, SqueezeTime, 100, "NestedTrap_Squeeze")
        elif SqueezeType == '2E_ELENA':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "2E_ELENA_start", TrapFloor, TrapWall, SqueezeTime, 100, "NestedTrap_Squeeze")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_ELENA_end", TrapWall, 0.0, 1.0, 100, "NestedTrap_Squeeze_part2")
            print("Valts is awesome")
        elif SqueezeType == '2E_ELENA_NICE': # for future memory, now identical to 2E_ELENA
            AEgIS_Trap.NiceSlowReshape("nested_trap", "2E_ELENA_start", TrapFloor, TrapWall, SqueezeTime, 100, "NestedTrap_Squeeze")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_ELENA_end", TrapWall, 0.0, 1.0, 100, "NestedTrap_Squeeze_part2")
        elif SqueezeType == '2E_ELENA_MRTOF':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "2E_ELENA_start", TrapFloor, TrapWall, SqueezeTime, 100, "NestedTrap_Squeeze")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_ELENA_MRTOF_end", TrapWall, TrapFloor, 1.0, 100, "NestedTrap_Squeeze_part2")
        else:
            print('Wrong squeeze trap name!')
        # Resetting trap
        AEgIS_Trap.FastReshapeMalmberg("nested_trap", 0.0, 0.0, 0.0, "NestedTrap_Off")

def PrepareNestedTrapShaping_SqueezeRaise(AEgIS_Trap:trap.TTrap, TrapFloor, TrapWall, SqueezeTime, SqueezeType, RaiseTime):
        # Only Valts traps are allowed
        print(f"Preparing DMA for nested '{SqueezeType}' traps ...")
        # Ion catching trap
        AEgIS_Trap.FastReshapeMalmberg("nested_trap", -TrapWall, -TrapWall, -TrapWall, "NestedTrap_On")
        AEgIS_Trap.SlowReshapeMalmberg("nested_trap", -TrapWall, TrapWall, -TrapWall, -TrapWall, -TrapWall, TrapWall, 4, 100, "NestedTrap_SR1")

        # Ion squeezing traps
        if SqueezeType == '2E_MCP':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "2E_MCP", -TrapWall, TrapWall, SqueezeTime, 100, "NestedTrap_SR2")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_MCP_SR3", -TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR3")
        elif SqueezeType == '2E_MCP_flat':
            AEgIS_Trap.SlowReshape("nested_trap", "2E_MCP", -TrapWall, TrapWall, SqueezeTime, 100, "NestedTrap_SR2")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_MCP_SR3", -TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR3")
        elif SqueezeType == '2E_ELENA':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "2E_ELENA_start", -TrapWall, TrapWall, SqueezeTime, 100, "NestedTrap_SR2")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_ELENA_end", TrapWall, 0.0, 1.0, 100, "NestedTrap_SR3")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_ELENA_SR4", -TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR4")
        elif SqueezeType == '2E_ELENA_MRTOF':
            AEgIS_Trap.NiceSlowReshape("nested_trap", "2E_ELENA_start", -TrapWall, TrapWall, SqueezeTime, 100, "NestedTrap_SR2")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_ELENA_MRTOF_end", TrapWall, 10.0, 1.0, 100, "NestedTrap_SR3")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_ELENA_SR4", -TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR4")
        else:
            print('Wrong squeeze trap name!')
        # Resetting trap
        AEgIS_Trap.FastReshapeMalmberg("nested_trap", 0.0, 0.0, 0.0, "NestedTrap_Off")
        return

if __name__ == '__main__':
    AEgIS_trap = trap.TTrap(position=-1095)
    AEgIS_trap.Print()

    Vwall = 160
    Vfloor = -160
    steps = 100

    # AEgIS_trap.ResetV(Vfloor,Vwall)

    AEgIS_trap.SetEverythingToZero()
    
    V_animate = [AEgIS_trap.GetTotalV()]
    PrepareHVTrapShaping(AEgIS_trap)
    PrepareNestedTrapShaping_SqueezeRaise(AEgIS_trap, TrapFloor=Vfloor, TrapWall=Vwall, SqueezeTime=10, SqueezeType="2E_MCP", RaiseTime=10)
    

    V_animate = AEgIS_trap.playback_handle("HV_ON")
    V_animate += AEgIS_trap.playback_handle("HV3_OFF")
    V_animate += AEgIS_trap.playback_handle("HV1_OFF")

    fig, ax = plt.subplots(figsize=(18, 10))

    # ax.clear()
    # ax.set_ylim(-200,200)
    # ax.set_xticks(AEgIS_trap.GetLabelPositions())
    # ax.set_xticklabels(AEgIS_trap.GetElectrodeNames())
    # ax.set_xticks(AEgIS_trap.GetMinorLabelPositions(),minor=True)
    # ax.grid(axis='x',which='minor',linestyle = "dashed",linewidth = 0.5,alpha=0.5)
    # ax.tick_params(which = "minor", bottom = False, left = False)
    # plt.xticks(rotation=45)
    # ax.set_xlabel("electrode")
    # ax.set_ylabel("voltage [V]")
    # line = ax.stairs(AEgIS_trap.GetTotalV())

    def animate(i):
        ax.clear()
        ax.set_ylim(-300,300)
        ax.set_xticks(AEgIS_trap.GetLabelPositions())
        ax.set_xticklabels(AEgIS_trap.GetElectrodeNames())
        ax.set_xticks(AEgIS_trap.GetMinorLabelPositions(),minor=True)
        ax.grid(axis='x',which='minor',linestyle = "dashed",linewidth = 0.5,alpha=0.5)
        ax.tick_params(which = "minor", bottom = False, left = False)
        plt.xticks(rotation=45)
        ax.set_xlabel("electrode")
        ax.set_ylabel("voltage [V]")
        line = ax.stairs(V_animate[i])
        return line, 


    ani = FuncAnimation(fig, animate, interval=40, blit=True, repeat=True, frames=len(V_animate),repeat_delay=500)
    print("Animation prepared")   
    plt.show()
    # ani.save("squeeze_MCP.gif", dpi=150, writer=PillowWriter(fps=steps))


