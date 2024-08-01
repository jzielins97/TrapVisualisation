import trap
from animation import AnimationObject


def PrepareHVTrapShaping(AEgIS_trap:trap.TTrap):
    AEgIS_trap.FastReshapeMalmberg("HV_trap", -14000, 0, -14000, "HV_ON")
    AEgIS_trap.FastReshape("HV_trap", "inlet",0,"HV3_OFF")
    AEgIS_trap.SlowReshape("HV_trap", "outlet",-14000,0,None,10,"HV1_OFF" )

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
        elif SqueezeType == '2E_MCP_flat':
            AEgIS_Trap.SlowReshape("nested_trap", "2E_MCP", -TrapWall, TrapWall, SqueezeTime, 100, "NestedTrap_SR2")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_MCP_SR3", -TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR3")
            AEgIS_Trap.SlowReshape("nested_trap", "2E_MCP_SR4", TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR4")
        elif SqueezeType == 'MIDDLE_flat':
            AEgIS_Trap.SlowReshape("symetric_nested_trap", "squeeze", -TrapWall, TrapWall, SqueezeTime, 100, "NestedTrap_SR2")
            AEgIS_Trap.SlowReshape("symetric_nested_trap", "inner_floor", -TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR3")
            AEgIS_Trap.FastReshape("symetric_nested_trap", "pre-dump", 0, "NestedTrap_SR4")
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
    Vfloor = 90
    steps = 100

    AEgIS_trap.SetEverythingToZero()
    
    PrepareHVTrapShaping(AEgIS_trap)
    PrepareNestedTrapShaping_SqueezeRaise(AEgIS_trap, TrapFloor=Vfloor, TrapWall=Vwall, SqueezeTime=10, SqueezeType="MIDDLE_flat", RaiseTime=10)

    ani = AnimationObject(AEgIS_trap)
    ani.add_sequence("HV_ON")
    ani.add_sequence("NestedTrap_On")
    ani.add_sequence("HV3_OFF")
    ani.add_sequence("HV1_OFF")
    ani.add_sequence("NestedTrap_SR1")
    ani.add_sequence("NestedTrap_SR2")
    ani.add_sequence("NestedTrap_SR3")
    ani.add_sequence("NestedTrap_SR4")

    ani.animate(save=True)




