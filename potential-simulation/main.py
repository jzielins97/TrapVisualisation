import trap
import utility as AEgIS_Utility
from animation import AnimationObject
import os


def PrepareHVTrapShaping(AEgIS_trap:trap.TTrap):
    AEgIS_trap.FastReshapeMalmberg("HV_trap", -12000, 0, -12000, "HV_ON")
    AEgIS_trap.FastReshape("HV_trap","outlet",-12000,"HV3_ON")
    AEgIS_trap.FastReshape("HV_trap","inlet",-12000,"HV1_ON")
    AEgIS_trap.SlowReshape("HV_trap", "inlet",-12000,0,None,10,"HV1_OFF" )
    AEgIS_trap.SlowReshape("HV_trap", "outlet",-12000,0,None,10,"HV3_OFF" )

def PrepareNestedTrapShaping(AEgIS_Trap:trap.TTrap, TrapFloor, TrapWall, SqueezeTime, TrapType, SqueezeType):
        print("Preparing DMA for nested traps ...")
        # Ion catching traps
        if TrapType == 'Standard':
            AEgIS_Trap.FastReshapeMalmberg("nested_trap", TrapWall, TrapFloor, TrapWall, "NestedTrap_On")
        elif TrapType == 'Valts':
            AEgIS_Trap.FastReshapeMalmberg("nested_trap", -TrapWall, -TrapWall, -TrapWall, "NestedTrap_On")
            #AEgIS_Trap.FastReshapeMalmberg( "nested_trap", TrapWall, -TrapWall, TrapWall, "NestedTrap_Valts_2")
            #AEgIS_Trap.FastReshapeMalmberg( "nested_trap", TrapWall, TrapFloor, TrapWall, "NestedTrap_Valts_3")
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
            AEgIS_Trap.SlowReshape("symmetric_nested_trap", "squeeze", -TrapWall, TrapWall, SqueezeTime, 100, "NestedTrap_SR2")
            AEgIS_Trap.SlowReshape("symmetric_nested_trap", "inner_floor", -TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR3")
            AEgIS_Trap.FastReshape("symmetric_nested_trap", "pre-dump", 0, "NestedTrap_SR4")
        elif SqueezeType == 'MIDDLE':
            AEgIS_Trap.NiceSlowReshape("symmetric_nested_trap", "squeeze", -TrapWall, TrapWall, SqueezeTime, 100, "NestedTrap_SR2")
            AEgIS_Trap.SlowReshape("symmetric_nested_trap", "inner_floor", -TrapWall, TrapFloor, RaiseTime, 100, "NestedTrap_SR3")
            AEgIS_Trap.FastReshape("symmetric_nested_trap", "pre-dump", 0, "NestedTrap_SR4")
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

def PrepareEloading(AEgIS_Trap:trap.TTrap, *trap_names):
        print("Preparing the trap shaping procedures ...")
        
        if "ctrap" in trap_names:
            print("\t Preparing C-trap")
            AEgIS_Trap.FastReshapeMalmberg("ctrap", 0.0, 0.0, 0.0, "Ctrap_Reset")
            AEgIS_Trap.SlowReshapeMalmberg("ctrap", 0.0, +190.0, 0.0, +190.0, 0.0, -190.0, 100, 40, "Ctrap_Eloading")
            AEgIS_Trap.FastReshapeMalmberg("ctrap", -190.0, +190.0, -190.0, "Ctrap_Close")
            AEgIS_Trap.SlowReshape("ctrap", "floor", +190.0, -10.0, 1000, 100, "Ctrap_Predump_Slow")
            AEgIS_Trap.FastReshapeMalmberg("ctrap", -190.0, -10.0, -190.0, "Ctrap_Predump_Fast")
            AEgIS_Trap.FastReshapeMalmberg("ctrap", -190.0, -10.0,  0.0, "Ctrap_Edump_Downstream")
            AEgIS_Trap.FastReshapeMalmberg("ctrap", -190.0, -10.0,  -190.0+AEgIS_Trap.Eloading_TransferredSpaceCharge, "Ctrap_PTrapLoading")
            AEgIS_Trap.FastReshapeMalmberg("ctrap", -190.0, -10.0,  -190.0, "Ctrap_StopPTrapLoading")
            AEgIS_Trap.FastReshapeMalmberg("ctrap", 0.0, -10.0,  -190.0, "Ctrap_Edump_Upstream")
            AEgIS_Trap.SlowReshape("ctrap_modes", "prepare", 0.0, -190.0, 1000, 100, "Ctrap_Modes_Prepare1")  
            AEgIS_Trap.SlowReshape("ctrap_modes", "extend", -190.0, -10.0, 1000, 100, "Ctrap_Modes_Prepare2")  
            # AEgIS_Trap.SlowReshape("Ctrap_Modes_Prepare3",                                                                      
            #                         ["C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15"],
            #                         {"C2": -133.401, "C3": -162.925, "C4": -109.141, "C5": -28.878, "C6": -1.272, "C7": -0.621, "C8": 2.825, "C9": -6.192, "C10": -19.946, "C11": -41.929, "C12": -71.768, "C13": -104.783, "C14": -169.172, "C15": -146.339, "C16": -149.206},
            #                         2000, 200,
            #                         {"C2": -190, "C3": -10, "C4": -10, "C5": -10, "C6": -10, "C7": -10, "C8": -10, "C9": -10, "C10": -10, "C11": -10, "C12": -10, "C13": -10, "C14": -10, "C15": -10, "C16": -190})
            # AEgIS_Trap.SlowReshape("Ctrap_Modes_Unprepare1",
            #                         ["C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "C13", "C14", "C15"],
            #                         {"C2": -190, "C3": -10, "C4": -10, "C5": -10, "C6": -10, "C7": -10, "C8": -10, "C9": -10, "C10": -10, "C11": -10, "C12": -10, "C13": -10, "C14": -10, "C15": -10, "C16": -190},
            #                         2000, 200,
            #                         {"C2": -133.401, "C3": -162.925, "C4": -109.141, "C5": -28.878, "C6": -1.272, "C7": -0.621, "C8": 2.825, "C9": -6.192, "C10": -19.946, "C11": -41.929, "C12": -71.768, "C13": -104.783, "C14": -169.172, "C15": -146.339, "C16": -149.206})            
            AEgIS_Trap.SlowReshape("ctrap_modes", "extend", -10.0, -190.0, 1000, 100, "Ctrap_Modes_Unprepare2")
            AEgIS_Trap.SlowReshape("ctrap_modes", "prepare", -190.0, 0.0, 1000, 100, "Ctrap_Modes_Unprepare3")


        if "ptrap" in trap_names:
            print("\t Preparing P-trap")
            # Direct electron loading
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short", 0.0, 0.0, 0.0, AEgIS_Trap.Eloading_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Ecooling_TrapEndcap, 100, 40, "Ptrap_DirectLoading_Eloading")
            AEgIS_Trap.SlowReshape(  "ptrap_short", "inlet", 0.0, AEgIS_Trap.Ecooling_TrapEndcap, 200, 40, "Ptrap_DirectLoading_Close")
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short", AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Eloading_TrapFloor, AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Ecooling_TrapEndcap, 1000, 100, "Ptrap_DirectLoading_Predump")                                                  
            # Two-step electron loading
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short2", 0.0, 0.0, 0.0, +150.0, -190.0, -190.0, 100, 40, "Ptrap_Eloading")               
            AEgIS_Trap.SlowReshape(  "ptrap_short2", "outlet", -190.0, 0.0, 1000, 100, "Ptrap_PbarCooling")  
            # Reshapings
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short", 0.0, AEgIS_Trap.Ecooling_TrapEndcap, +150.0, AEgIS_Trap.Ecooling_TrapFloor, 0.0, AEgIS_Trap.Ecooling_TrapEndcap, 2, 1000, "Ptrap_Reshape_PbarToDump")                
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, AEgIS_Trap.Ecooling_TrapFloor, 150.0, AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 2, 1000, "Ptrap_Reshape_DumpToPbar")  
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short", 0.0, AEgIS_Trap.Ecooling_TrapEndcap-AEgIS_Trap.Ecooling_TrapFloor, +150.0, 0.0, 0.0, AEgIS_Trap.Ecooling_TrapEndcap-AEgIS_Trap.Ecooling_TrapFloor, 2, 1000, "Ptrap_Reshape_PbarToModes")                
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short", AEgIS_Trap.Ecooling_TrapEndcap-AEgIS_Trap.Ecooling_TrapFloor, 0.0, 0.0, +150.0, AEgIS_Trap.Ecooling_TrapEndcap-AEgIS_Trap.Ecooling_TrapFloor, 0.0, 2, 1000, "Ptrap_Reshape_ModesToPbar")            
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short",AEgIS_Trap. Ecooling_TrapEndcap-AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, 0.0, AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap-AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, 2, 1000, "Ptrap_Reshape_ModesToDump")  
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short", 0.0, AEgIS_Trap.Ecooling_TrapEndcap, 150.0, 150.0, 0.0, AEgIS_Trap.Ecooling_TrapEndcap, 2, 1000, "Ptrap_Reshape_PbarToCompress")                
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_short", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 150.0, 150.0, AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 2, 1000, "Ptrap_Reshape_CompressToPbar")                                  
            AEgIS_Trap.SlowReshape(  "ptrap_short", "floor", AEgIS_Trap.Ecooling_TrapFloor, +150.0, 2, 1000, "Ptrap_Reshape_DumpToCompress")
            AEgIS_Trap.SlowReshape(  "ptrap_short", "floor", 150.0, AEgIS_Trap.Ecooling_TrapFloor, 2, 1000, "Ptrap_Reshape_CompressToDump")
            AEgIS_Trap.SlowReshape(  "ptrap_short", "probe", AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, 2, 1000, "Ptrap_Reshape_DumpToProbe")
            AEgIS_Trap.SlowReshape(  "ptrap_short", "probe", AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Ecooling_TrapFloor, 2, 1000, "Ptrap_Reshape_ProbeToDump")            
            # Reshaping from dump to transfer trap
            AEgIS_Trap.SlowReshape(  "ptrap_transfer", "all_but_inlet", 0.0, AEgIS_Trap.Ecooling_TrapEndcap, 2, 1000, "Ptrap_DumpToTransfer_Prepare")
            # AEgIS_Trap.NiceSlowReshape("ptrap_short", "extend_to_long", Ecooling_TrapEndcap, Ecooling_TrapFloor, 1, 100, "Ptrap_DumpToTransfer_Extend")
            # AEgIS_Trap.NiceSlowReshape("ptrap_long", "squeeze_to_transfer", Ecooling_TrapFloor, Ecooling_TrapEndcap, 1, 100, "Ptrap_DumpToTransfer_Squeeze")
            AEgIS_Trap.SlowReshape("ptrap_short", "extend_to_long", AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Ecooling_TrapFloor, 2, 1000, "Ptrap_DumpToTransfer_Extend")
            AEgIS_Trap.SlowReshape("ptrap_long", "squeeze_to_transfer", AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, 2, 1000, "Ptrap_DumpToTransfer_Squeeze")
            AEgIS_Trap.SlowReshape("ptrap_transfer", "floor", AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_LaunchPotential, 2, 1000, "Ptrap_DumpToTransfer_Float")
            # Electron reloading
            AEgIS_Trap.SlowReshape(  "ptrap_transfer", "second_inlet", AEgIS_Trap.Ecooling_LaunchPotential, AEgIS_Trap.Ecooling_TrapEndcap, 1, 100, "Ptrap_Reloading_RaiseSecondInlet")
            AEgIS_Trap.FastReshapeMalmberg("ptrap_reloading", 0.0, 150.0, AEgIS_Trap.Ecooling_TrapEndcap, "Ptrap_Reloading_Eloading")                
            AEgIS_Trap.SlowReshapeMalmberg("ptrap_transfer",  0.0, AEgIS_Trap.Ecooling_TrapEndcap, 150.0, AEgIS_Trap.Transfer_RecyclingPotential, AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Ecooling_TrapEndcap, 1000, 100, "Ptrap_Reloading_ToRecycling")                
            AEgIS_Trap.SlowReshape(  "ptrap_transfer", "second_inlet", AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Ecooling_LaunchPotential, 1, 100, "Ptrap_Reloading_LowerSecondInlet")
            # Pbar recycling trap
            # AEgIS_Trap.SlowReshape("ptrap_transfer", "second_inlet", Ecooling_TrapEndcap, Ecooling_LaunchPotential, 1, 100, "Ptrap_ElectronRecycling_LowerSecondInlet")                
            AEgIS_Trap.SlowReshape("ptrap_short", "floor", AEgIS_Trap.Ecooling_TrapEndcap, AEgIS_Trap.Transfer_RecyclingPotential, 1, 1000, "Ptrap_ElectronRecycling_Floor")
            # Reshaping from transfer to dump trap
            AEgIS_Trap.FastReshape("parabola", "flat_to_zero", 0.0, "Ptrap_RemoveParabola")
            AEgIS_Trap.FastReshape("ptrap_long", "floor", AEgIS_Trap.Transfer_RecyclingPotential, "Ptrap_ElectronRecycling_Flatten")
            AEgIS_Trap.SlowReshape("ptrap_long", "floor", AEgIS_Trap.Transfer_RecyclingPotential, AEgIS_Trap.Ecooling_TrapFloor, 500, 50, "Ptrap_ElectronRecycling_Float")
            AEgIS_Trap.NiceSlowReshape("ptrap_long", "squeeze_to_short_downstream", AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, 500, 50, "Ptrap_ElectronRecycling_SqueezeDownstream")
            AEgIS_Trap.SlowReshape("ptrap_long", "squeeze_to_short_upstream", AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, 500, 50, "Ptrap_ElectronRecycling_SqueezeUpstream")
            AEgIS_Trap.NiceSlowReshape("ptrap_long", "reduce_to_short_downstream", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 500, 50, "Ptrap_ElectronRecycling_ReduceDownstream")
            AEgIS_Trap.SlowReshape("ptrap_long", "reduce_to_short_upstream",  AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 500, 50, "Ptrap_ElectronRecycling_ReduceUpstream")                
            # Pbar dumping
            AEgIS_Trap.FastReshapeMalmberg("ptrap_short", 0.0, AEgIS_Trap.Ecooling_TrapFloor, AEgIS_Trap.Ecooling_TrapEndcap, "Ptrap_Dump_Upstream_Fast")
            AEgIS_Trap.SlowReshape(  "ptrap_short", "inlet", 0.0, AEgIS_Trap.Ecooling_TrapEndcap, 1, 100, "Ptrap_Dump_Upstream_Reset")
            AEgIS_Trap.SlowReshape(  "ptrap_short", "inlet", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 5, 200, "Ptrap_Dump_Upstream_5s")
            AEgIS_Trap.SlowReshape(  "ptrap_short", "inlet", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 30, 1000, "Ptrap_Dump_Upstream_30s")
            AEgIS_Trap.SlowReshape(  "ptrap_short", "inlet", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 180, 5000, "Ptrap_Dump_Upstream_180s")                
            AEgIS_Trap.SlowReshape(  "ptrap_short", "outlet", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 30, 1000, "Ptrap_Dump_Downstream_Slow_Short")
            AEgIS_Trap.SlowReshape(  "ptrap_long", "outlet", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 30, 1000, "Ptrap_Dump_Downstream_Slow_Long")
            AEgIS_Trap.SlowReshape(  "ptrap_transfer", "outlet", AEgIS_Trap.Ecooling_TrapEndcap, 0.0, 30, 1000, "Ptrap_Dump_Downstream_Slow_Transfer")
            # Temperature measurement
            AEgIS_Trap.Reshape_TemperatureMeasurement("P13", AEgIS_Trap.Ecooling_TrapEndcap, -120.0, 0.1, "Ptrap_Dump_TemperatureMeasurement1")
            AEgIS_Trap.Reshape_TemperatureMeasurement("P13", -120.0, AEgIS_Trap.Ecooling_LaunchPotential+5.0,  1.0, "Ptrap_Dump_TemperatureMeasurement2")    
            # Resetting
            AEgIS_Trap.FastReshape("ptrap", "all", 0.0, "Ptrap_Reset")       
            AEgIS_Trap.SlowReshape("ptrap_short2", "floor", 150.0, 0.0, 1000, 100, "Ptrap2_SlowReset")
 

        if "atrap" in trap_names:
            print("\t Preparing A-trap")
            AEgIS_Trap.FastReshapeMalmberg("atrap_long", 0.0, 0.0, 0.0, "Atrap_Reset_Long")
            AEgIS_Trap.FastReshapeMalmberg("atrap_long", 0.0, +120.0, -150.0, "Atrap_Eloading_Long")
            AEgIS_Trap.FastReshapeMalmberg("atrap_long", -150.0, +120.0, -150.0, "Atrap_Close_Long")
            AEgIS_Trap.FastReshapeMalmberg("atrap_long", -150.0, -30.0, -150.0, "Atrap_Predump_Fast_Long")
            AEgIS_Trap.FastReshapeMalmberg("atrap", 0.0, 0.0, 0.0, "Atrap_Reset")
            AEgIS_Trap.FastReshapeMalmberg("atrap", 150.0, +150.0, -150.0, "Atrap_Eloading")
            AEgIS_Trap.FastReshapeMalmberg("atrap", -150.0, +150.0, -150.0, "Atrap_Close")
            AEgIS_Trap.FastReshapeMalmberg("atrap", -150.0, -31.6, -150.0, "Atrap_Predump_Fast")
            AEgIS_Trap.SlowReshape("atrap", "floor", 150.0, -31.6, 1000, 100, "Atrap_Predump_Slow")
            AEgIS_Trap.SlowReshape(  "atrap_long", "hot",    +120.0, 0.0, 1000, 100, "Atrap_Squeeze")
            AEgIS_Trap.SlowReshape(  "atrap_long", "inlet",  -150.0, 0.0, 1000, 100, "Atrap_Hotdump1")
            AEgIS_Trap.SlowReshape(  "atrap_long", "outlet", -150.0, 0.0, 1000, 100, "Atrap_Hotdump2")
            AEgIS_Trap.SlowReshapeMalmberg("atrap_short", 0.0, -150.0, +120.0, -30.0, 0.0, -150.0, 1000, 100, "Atrap_Predump")
            AEgIS_Trap.SlowReshape(  "atrap_short", "outlet", -150.0, 0.0, 1000, 100, "Atrap_Dump_Downstream")

def FurtherRecordingForCalibtration(AEgIS_Trap:trap.TTrap):
    AEgIS_Trap.SlowReshape("ptrap_transfer","second_inlet",-70,-150,2,102,"Ptrap_Further_Reshape_ForCalibration")



def HCI_CatchAndDump_py(animation:AnimationObject,trap:trap.TTrap,NestedTrap_SqueezedTrapType = '2E_MCP',NestedTrap_Wall = 160,NestedTrap_TrapFloor = 90):
    
    PrepareHVTrapShaping(trap)
    PrepareNestedTrapShaping_SqueezeRaise(trap, TrapFloor=NestedTrap_TrapFloor, TrapWall=NestedTrap_Wall, SqueezeTime=10, SqueezeType=NestedTrap_SqueezedTrapType, RaiseTime=10)

    trap.NestedTrap_SqueezedTrapType = NestedTrap_SqueezedTrapType
    trap.NestedTrap_Wall = NestedTrap_Wall
    trap.NestedTrap_TrapFloor = NestedTrap_TrapFloor

    # trap pbars
    animation.add_sequence("HV3_ON")
    animation.add_wait(1)
    animation.add_sequence("HV1_ON")
    animation.add_wait(1)
    animation.add_sequence("NestedTrap_On")
    animation.add_wait(1)
    animation.add_sequence("HV1_OFF")
    animation.add_sequence("HV3_OFF")
    animation.add_wait(1)
    animation.add_sequence("NestedTrap_SR1")
    animation.add_sequence("NestedTrap_SR2")
    animation.add_sequence("NestedTrap_SR3")
    if NestedTrap_SqueezedTrapType in ['2E_ELENA','2E_ELENA_MRTOF','MIDDLE','MIDDLE_flat']:
        animation.add_sequence("NestedTrap_SR4")
    
    return f'HCI_CatchAndDump_py_{NestedTrap_SqueezedTrapType}_floor={NestedTrap_TrapFloor}V_wall={NestedTrap_Wall}V'

def HCI_CnD_eCool_py(animation:AnimationObject,trap:trap.TTrap,
                     NestedTrap_SqueezedTrapType = '2E_MCP',
                     NestedTrap_Wall = 160,
                     NestedTrap_TrapFloor = 90,
                     Eloading_TrapFloor = 150.,
                     Ecooling_TrapFloor = -10.0,
                     Ecooling_TrapEndcap = -150.0,
                     Ecooling_LaunchPotential = -70.0,
                     Transfer_RecyclingPotential = -70.0,
                     Eloading_TransferredSpaceCharge = 30):
    
    trap.NestedTrap_SqueezedTrapType = NestedTrap_SqueezedTrapType
    trap.NestedTrap_Wall = NestedTrap_SqueezedTrapType
    trap.NestedTrap_TrapFloor = NestedTrap_TrapFloor
    trap.Eloading_TrapFloor = Eloading_TrapFloor
    trap.Ecooling_TrapFloor = Ecooling_TrapFloor
    trap.Ecooling_TrapEndcap = Ecooling_TrapEndcap
    trap.Ecooling_LaunchPotential = Ecooling_LaunchPotential
    trap.Transfer_RecyclingPotential = Transfer_RecyclingPotential
    trap.Eloading_TransferredSpaceCharge = Eloading_TransferredSpaceCharge
    
    PrepareHVTrapShaping(trap)
    PrepareNestedTrapShaping_SqueezeRaise(trap, TrapFloor=NestedTrap_TrapFloor, TrapWall=NestedTrap_Wall, SqueezeTime=10, SqueezeType=NestedTrap_SqueezedTrapType, RaiseTime=10)
    PrepareEloading(trap, "ptrap","ctrap")

    animation.add_sequence("Ctrap_Eloading")
    animation.add_sequence("Ctrap_Close")
    animation.add_sequence("Ctrap_Predump_Slow")
    animation.add_wait(1)
    animation.add_sequence("Ptrap_Eloading")
    animation.add_wait(1)
    animation.add_sequence("Ctrap_PTrapLoading")
    animation.add_sequence("Ctrap_StopPTrapLoading")
    animation.add_sequence("Ctrap_Edump_Upstream")
    animation.add_sequence("Ctrap_Reset")
    animation.add_sequence("Ptrap_PbarCooling")
    # end of the ecooling thingy
    animation.add_wait(1)
    # trap pbars
    animation.add_sequence("HV3_ON")
    animation.add_wait(1)
    animation.add_sequence("HV1_ON")
    animation.add_wait(5)
    # flatten before 
    animation.add_sequence("Ctrap_Reset")
    animation.add_sequence("Ptrap_Reset")
    animation.add_wait(1)
    # nested trap
    animation.add_sequence("NestedTrap_On")
    # ion accumulation time
    animation.add_wait(5)
    # release pbars
    animation.add_sequence("HV1_OFF")
    animation.add_sequence("HV3_OFF")
    animation.add_wait(1)
    
    animation.add_wait(1)
    # reshape for HCI
    animation.add_sequence("NestedTrap_SR1")
    animation.add_sequence("NestedTrap_SR2")
    animation.add_sequence("NestedTrap_SR3")
    if NestedTrap_SqueezedTrapType in ['2E_ELENA','2E_ELENA_MRTOF','MIDDLE','MIDDLE_flat']:
        animation.add_sequence("NestedTrap_SR4")
    
    return f'HCI_CnD_eCool_py_{NestedTrap_SqueezedTrapType}_floor={NestedTrap_TrapFloor}V_wall={NestedTrap_Wall}V_eLoadFloor={Eloading_TrapFloor}V_eCoolFloor={Ecooling_TrapFloor}V_eCoolEndCap={Ecooling_TrapEndcap}V_eCoolLaunch={Ecooling_LaunchPotential}V_recPotential={Transfer_RecyclingPotential}V_tCharge={Eloading_TransferredSpaceCharge}'

def Pbar_ElectronCooling2_valve_py(animation:AnimationObject,trap:trap.TTrap,
                     Eloading_TrapFloor = 150.,
                     Ecooling_TrapFloor = -10.0,
                     Ecooling_TrapEndcap = -150.0,
                     Ecooling_LaunchPotential = -70.0,
                     Transfer_RecyclingPotential = -70.0,
                     Eloading_TransferredSpaceCharge = 30):
    
    trap.Eloading_TrapFloor = Eloading_TrapFloor
    trap.Ecooling_TrapFloor = Ecooling_TrapFloor
    trap.Ecooling_TrapEndcap = Ecooling_TrapEndcap
    trap.Ecooling_LaunchPotential = Ecooling_LaunchPotential
    trap.Transfer_RecyclingPotential = Transfer_RecyclingPotential
    trap.Eloading_TransferredSpaceCharge = Eloading_TransferredSpaceCharge
    
    PrepareHVTrapShaping(trap)
    PrepareEloading(trap, "ptrap","ctrap")

    # ecooling thingy
    animation.add_sequence("Ctrap_Eloading")
    animation.add_sequence("Ctrap_Close")
    animation.add_sequence("Ctrap_Predump_Slow")
    animation.add_wait(1)
    animation.add_sequence("Ptrap_Eloading")
    animation.add_wait(1)
    animation.add_sequence("Ctrap_PTrapLoading")
    animation.add_sequence("Ctrap_StopPTrapLoading")
    animation.add_sequence("Ctrap_Edump_Upstream")
    animation.add_sequence("Ctrap_Reset")
    animation.add_sequence("Ptrap_PbarCooling")
    animation.add_wait(1)
    # trap pbars
    animation.add_sequence("HV3_ON")
    animation.add_wait(1)
    animation.add_sequence("HV1_ON")
    animation.add_wait(5)
    animation.add_sequence("HV1_OFF")
    animation.add_sequence("HV3_OFF")
    animation.add_wait(1)
    animation.add_sequence("Ptrap_Reshape_PbarToDump")
    animation.add_wait(5)

    return f'Pbar_ElectronCooling2_valve_py_eLoadFloor={Eloading_TrapFloor}V_eCoolFloor={Ecooling_TrapFloor}V_eCoolEndCap={Ecooling_TrapEndcap}V_eCoolLaunch={Ecooling_LaunchPotential}V_recPotential={Transfer_RecyclingPotential}V_tCharge={Eloading_TransferredSpaceCharge}'

def HCI_pbar_calibration_py(animation:AnimationObject,trap:trap.TTrap,
                     Eloading_TrapFloor = 150.,
                     Ecooling_TrapFloor = -10.0,
                     Ecooling_TrapEndcap = -150.0,
                     Ecooling_LaunchPotential = -70.0,
                     Transfer_RecyclingPotential = -70.0,
                     Eloading_TransferredSpaceCharge = 30):
    
    trap.Eloading_TrapFloor = Eloading_TrapFloor
    trap.Ecooling_TrapFloor = Ecooling_TrapFloor
    trap.Ecooling_TrapEndcap = Ecooling_TrapEndcap
    trap.Ecooling_LaunchPotential = Ecooling_LaunchPotential
    trap.Transfer_RecyclingPotential = Transfer_RecyclingPotential
    trap.Eloading_TransferredSpaceCharge = Eloading_TransferredSpaceCharge

    PrepareHVTrapShaping(trap)
    PrepareEloading(trap, "ptrap","ctrap")
    FurtherRecordingForCalibtration(AEgIS_trap)

    # ecooling thingy
    animation.add_sequence("Ctrap_Eloading")
    animation.add_sequence("Ctrap_Close")
    animation.add_sequence("Ctrap_Predump_Slow")
    animation.add_wait(1)
    animation.add_sequence("Ptrap_Eloading")
    animation.add_wait(1)
    animation.add_sequence("Ctrap_PTrapLoading")
    animation.add_sequence("Ctrap_StopPTrapLoading")
    animation.add_sequence("Ctrap_Edump_Upstream")
    animation.add_sequence("Ctrap_Reset")
    animation.add_sequence("Ptrap_PbarCooling")
    animation.add_wait(1)
    # trap pbars
    animation.add_sequence("HV3_ON")
    animation.add_wait(1)
    animation.add_sequence("HV1_ON")
    animation.add_wait(5)
    animation.add_sequence("HV1_OFF")
    animation.add_sequence("HV3_OFF")
    animation.add_wait(1)
    animation.add_sequence("Ptrap_Reshape_PbarToDump")
    animation.add_wait(1)
    animation.add_sequence("Ptrap_DumpToTransfer_Prepare")
    animation.add_sequence("Ptrap_DumpToTransfer_Extend")
    animation.add_sequence("Ptrap_DumpToTransfer_Squeeze")
    animation.add_sequence("Ptrap_DumpToTransfer_Float")
    animation.add_wait(1)
    animation.add_sequence("Ptrap_Further_Reshape_ForCalibration")
    animation.add_wait(5)

    return f'HCI_pbar_calibration_py_eLoadFloor={Eloading_TrapFloor}V_eCoolFloor={Ecooling_TrapFloor}V_eCoolEndCap={Ecooling_TrapEndcap}V_eCoolLaunch={Ecooling_LaunchPotential}V_recPotential={Transfer_RecyclingPotential}V_tCharge={Eloading_TransferredSpaceCharge}'


if __name__ == '__main__':
    # parameters:
    AEgIS_trap = trap.TTrap(position=-1095)
    AEgIS_trap.Print()
    AEgIS_trap.SetEverythingToZero()
    

    ani = AnimationObject(AEgIS_trap,fps=100)
    Vwall = 195
    Vfloor = 195
    AEgIS_trap.SetElectrodeV("P8",Vwall)
    AEgIS_trap.SetElectrodeV("P9",Vwall)
    AEgIS_trap.SetElectrodeV("P10",Vfloor)
    # AEgIS_trap.SetElectrodeV("P11",Vfloor)
    # AEgIS_trap.SetElectrodeV("P12",Vfloor)
    # AEgIS_trap.SetElectrodeV("P13",Vwall)
    ani.plot_current_state()


    # file = HCI_pbar_calibration_py(ani,AEgIS_trap,Eloading_TrapFloor = 150.,Ecooling_TrapFloor = -10.0,Ecooling_TrapEndcap = -150.0,Ecooling_LaunchPotential = -70.0,Transfer_RecyclingPotential = -70.0,Eloading_TransferredSpaceCharge = 30)
    # file = Pbar_ElectronCooling2_valve_py(ani,AEgIS_trap,Eloading_TrapFloor = 150.,Ecooling_TrapFloor = -10.0,Ecooling_TrapEndcap = -150.0,Ecooling_LaunchPotential = -70.0,Transfer_RecyclingPotential = -70.0,Eloading_TransferredSpaceCharge = 30)
    # file = HCI_CnD_eCool_py(ani,AEgIS_trap,NestedTrap_SqueezedTrapType = '2E_MCP',NestedTrap_Wall = 160,NestedTrap_TrapFloor = 90,Eloading_TrapFloor = 150.,Ecooling_TrapFloor = -10.0,Ecooling_TrapEndcap = -150.0,Ecooling_LaunchPotential = -70.0,Transfer_RecyclingPotential = -70.0,Eloading_TransferredSpaceCharge = 30)
    # file = HCI_CatchAndDump_py(ani,AEgIS_trap,NestedTrap_SqueezedTrapType = '2E_MCP',NestedTrap_Wall = 160,NestedTrap_TrapFloor = 90)
    # ani.animate(show=False,save=True,file=os.path.join(os.path.dirname(__file__),'animations',file))



    exit(0)




