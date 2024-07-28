import numpy as np
import json
import os
from electrode import TElectrode

class TTrap():
    electrodes:[TElectrode]=[] # list of all electrodes
    electrode_mapping:{str:int}={} # mapping for quick access to electrode
    position:float=0 # inisitla position of the trap
    length:float=0 # length of the trap
    segments:int=2048 # total number of positions points 
    dx:float=0.5 # distance between position points
    __TRAP_CONFIGS:{str:{str:[str]}}={} # configurations of the trap
    __POTENTIAL_MATRIX:[[float]]=[[]] # matrix for calculating the final potential
    __DMA_DUMMY:{str:[[float]]}={} # internal memory for trapping sequences


    def __init__(self,position:float=0.0):
        self.position = position
        self.electrodes:list(TElectrode) = []

        script_dir = os.path.dirname(__file__)
        trap_setup_path = os.path.join(script_dir, "trap_setup.json")
        with open(trap_setup_path) as trap_config_file:
            self.__TRAP_CONFIGS = json.load(trap_config_file) 
            # for config_name,config in self.__TRAP_CONFIGS.items():
            #     print(config_name)
            #     for key,item in config.items():
            #         print(f"\t{key}:{item}")

        
        potential_matrix_path = os.path.join(script_dir, "ElectrodesPotentialMap.txt")
        with open(potential_matrix_path, 'r') as f:
            self.__POTENTIAL_MATRIX = np.array([[float(value) for value in l.strip().split("\t")[1:2049]] for l in f.readlines()])   

        self.electrodes.append(TElectrode("C0",position+0.0,13.5))
        self.electrodes.append(TElectrode("HV1",position+23.5,40.0))
        self.electrodes.append(TElectrode("C1",position+73.5,27.5))
        for i in range(2,6):
            self.electrodes.append(TElectrode(f"C{i}",position+101.0 + (i-2)*30,30))
        for i in range(6,16):
            self.electrodes.append(TElectrode(f"C{i}",position+221.0 + (i-6)*13.5,13.5))
        for i in range(16,19):
            self.electrodes.append(TElectrode(f"C{i}", position+356.0 + (i-16)*30.0,30.0))
        self.electrodes.append(TElectrode("C19", position+446.0,27.5))
        self.electrodes.append(TElectrode("HV2",position+483.5,40.0))
        self.electrodes.append(TElectrode("P1", position+533.5,24.0))
        self.electrodes.append(TElectrode("P2", position+557.5,30.0))
        for i in range(3,13):
            self.electrodes.append(TElectrode(f"P{i}",position+587.5+(i-3)*13.5,13.5))
        self.electrodes.append(TElectrode("P13",position+722.5,30.0))
        self.electrodes.append(TElectrode("P14",position+752.5,24.0))
        self.electrodes.append(TElectrode("HV3",position+786.5,40))
        self.electrodes.append(TElectrode("T1",position+836.5,27.5))
        for i in range(2,6):
            self.electrodes.append(TElectrode(f"T{i}", position+864.0+(i-2)*40,40.0))
        self.electrodes.append(TElectrode("T6",position+1024,40.0))

        self.length = self.electrodes[-1].GetElectrodeEnd() - self.electrodes[0].GetElectrodeStart()

        self.electrode_mapping = {}
        
        for i,e in enumerate(self.electrodes):
            self.electrode_mapping[e.GetName()] = i

    ########################## voltage functions ##########################
    def SetElectrodeV(self,electrode:str,V:float):
        self.electrodes[self.electrode_mapping[electrode]].SetPotential(V)

    def GetElectrodeV(self,electrode:str)->float:
        return self.electrodes[self.electrode_mapping[electrode]].GetPotential()

    def GetTotalV(self)->[float]:
        V = np.array([electrode.GetPotential() for electrode in self.electrodes])
        # print(V.T.shape)
        # print(self.__POTENTIAL_MATRIX.T.shape)
        return V
    
    def SetEverythingToZero(self, electrodes:[str]=None)->None:
        if electrodes is None:
            for i in range(1,len(self.electrodes)-1):
                self.electrodes[i].SetPotential(0)
        else:
            for electrode in electrodes:
                self.SetElectrodeV(electrode,0)

    def DetermineVoltageForRamp(self, V_start, V_end, steps, i):
        return (V_end - V_start)*(i+1)/steps

    ########################## log functions ##########################

    def Print(self):
        print('Trap configuration:')
        for electrode in self.electrodes:
            print(f'{electrode}')

    
    ########################## trapping functions ##########################
    
    def DefineTrapConfig(self, trap_name:str, config_name:str) -> [str]:
        electrodes = ["ERROR"]
        try:
            electrodes = self.__TRAP_CONFIGS[trap_name][config_name]
        except ValueError:
            print("This trap does not seem to be defined! Please provide a valid trap name!")
        return electrodes
    
    def NiceSlowReshape(self, trap_name, config_name, Vstart, Vend, duration, steps, handle_name):
        electrodes = self.DefineTrapConfig(trap_name, config_name)

        V_animate = []
        
        iteration = 0
        # check if we are dividing by 0
        if steps == 0:
            steps = 1
        if Vend > 160:
            Vend = 160 # coerce
        # calculate voltage step size
        dV = (Vend - Vstart)/steps
        # define counters for electrodes
        start_electrode = 0
        stop_electrode = 1

        # get number of electrodes
        n_electrodes = len(electrodes)

        # create an array of voltages set
        V = [Vstart]*n_electrodes

        while abs(V[n_electrodes-1]-Vstart) < abs(Vend-Vstart):
            # loop over electrodes that we want to update
            for electrode in range(start_electrode,stop_electrode):
                # calculate new voltage for the electrodes 
                V[electrode] = V[electrode] + dV
                if abs(V[electrode]-Vstart) > abs(Vend-Vstart):
                    V[electrode] = Vend
                    if electrode == start_electrode:
                        start_electrode = start_electrode+1
                # check if the value doesn"t extend the limit
                # # set new voltage for the electrode
                self.SetElectrodeV(electrodes[electrode],V[electrode])
                # delay(10*ns)            
                

            # # actually raise potential on all electrodes to set value    
            # for fastino in range(len(self.fastinos)):
            #     self.fastinos[fastino].update(0xFFFFFFFF)
            #     delay(10*ns)

            # update start_electrode
            # if abs(V[start_electrode]) >= abs(Vend):
            #     start_electrode = start_electrode+1
            # add another electrode if not all are already included
            if stop_electrode < n_electrodes:
                stop_electrode = stop_electrode + 1
            
            iteration = iteration+1
            V_animate.append(self.GetTotalV())
        self.__DMA_DUMMY[handle_name]=V_animate
    
    def FastReshapeMalmberg(self, trap_name, Vinlet, Vfloor, Voutlet, handle_name=''):
        inlet = self.DefineTrapConfig(trap_name, "inlet")
        for electrode in inlet:
            self.SetElectrodeV(electrode,Vinlet)
        floor = self.DefineTrapConfig(trap_name, "floor")
        for electrode in floor:
            self.SetElectrodeV(electrode,Vfloor)
        outlet = self.DefineTrapConfig(trap_name, "outlet")
        for electrode in outlet:
            self.SetElectrodeV(electrode,Voutlet)
    
        self.__DMA_DUMMY[handle_name]=[self.GetTotalV()]

    def SlowReshapeMalmberg(self, trap_name, Vinlet_start, Vinlet_end, Vfloor_start, Vfloor_end, Voutlet_start, Voutlet_end, duration, steps, handle_name=''):
        inlet = self.DefineTrapConfig(trap_name, "inlet")
        floor = self.DefineTrapConfig(trap_name, "floor")
        outlet = self.DefineTrapConfig(trap_name, "outlet")

        V = []
        for i in range(steps):
            for electrode in inlet:
                self.SetElectrodeV(electrode,Vinlet_start + self.DetermineVoltageForRamp(Vinlet_start,Vinlet_end,steps,i))
            for electrode in floor:
                self.SetElectrodeV(electrode,Vfloor_start + self.DetermineVoltageForRamp(Vfloor_start,Vfloor_end,steps,i))
            for electrode in outlet:
                self.SetElectrodeV(electrode,Voutlet_start + self.DetermineVoltageForRamp(Voutlet_start,Voutlet_end,steps,i))
            V.append(self.GetTotalV())
        self.__DMA_DUMMY[handle_name]=V

    def FastReshape(self, trap_name, config_name, V, handle_name='')->{str:[[float]]}:
        electrode_names = self.DefineTrapConfig(trap_name, config_name)
        for electrode in electrode_names:
            self.SetElectrodeV(electrode,V)
        self.__DMA_DUMMY[handle_name] = [self.GetTotalV()]

    def SlowReshape(self, trap_name, config_name, Vstart, Vend, duration, steps, handle_name='')->{str:[[float]]}:
        # determined_delay = self.Determinedt(duration, steps)
        electrode_names = self.DefineTrapConfig(trap_name, config_name)
        V = []
        for i in range(steps):
            for electrode in electrode_names:
                self.SetElectrodeV(electrode,Vstart + self.DetermineVoltageForRamp(Vstart, Vend, steps, i))
            V.append(self.GetTotalV())
        self.__DMA_DUMMY[handle_name]=V


    ########################## animation functions ##########################

    def GetFinalPotentials(self, i, handle_name:str):
        V = self.__POTENTIAL_MATRIX.T @ self.__DMA_DUMMY[handle_name][i]
        return V
        # totalV = [self.__POTENTIAL_MATRIX.T @ V for V in self.DMA_DUMMY[handle_name]]
        # for _ in range(frames_to_wait):
        #     totalV.append(self.__POTENTIAL_MATRIX.T @ self.DMA_DUMMY[handle_name][-1])
        # return totalV

    def GetHandleDuration(self,handle_name):
        return len(self.__DMA_DUMMY[handle_name])

    def GetLabelPositions(self):
        return [int((electrode.GetElectrodeCenter()-self.position)/self.dx) for electrode in self.electrodes]
    
    def GetMinorLabelPositions(self):
        ticks = []
        for electrode in self.electrodes:
            ticks.append((electrode.GetElectrodeStart()-self.position)/self.dx)
            ticks.append((electrode.GetElectrodeEnd()-self.position)/self.dx)
        return ticks
    
    def GetElectrodeNames(self):
        return list(self.electrode_mapping.keys())


