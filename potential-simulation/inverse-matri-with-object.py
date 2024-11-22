import os
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
from trap import TTrap

script_dir=os.path.dirname(__file__)
potential_matrix_path = os.path.join(script_dir, "ElectrodesPotentialMap.txt")
GROUNDED_ELECTRODES = ['C1'] # ,'C16','C17'
with open(potential_matrix_path, 'r') as f:
   __POTENTIAL_MATRIX__ = np.array([[float(value) for value in l.strip().split("\t")[1:2049]] if l.strip().split("\t")[0] not in  GROUNDED_ELECTRODES else [0]*2048 for l in f.readlines()])   

__POTENTIAL_MATRIX_INV__ = sc.linalg.pinv(__POTENTIAL_MATRIX__)

# for electrode in electrodes:
#     print(f"{electrode['name']} at {electrode['from']}-{electrode['from']+electrode['size']}")

AEgIS_trap = TTrap(position=-1095)
AEgIS_trap.Print()

set_potential = AEgIS_trap.GetTotalV()
real_potential = AEgIS_trap.get_final_V()
recalculated_potential = real_potential @ __POTENTIAL_MATRIX_INV__

electrodes_position = AEgIS_trap.GetElectrodePositions()
# electrodes_position.append(electrodes_position[-1]+electrodes[-1]['size'])

x=np.array([AEgIS_trap.position + i * AEgIS_trap.dx for i in range(len(real_potential))])

plt.figure(1)
plt.plot(x,real_potential,drawstyle='steps-mid',label="real potential")
plt.plot(electrodes_position,set_potential,drawstyle='steps-post',label="set potential")
plt.plot(electrodes_position,recalculated_potential,color='black',linestyle=(0,(5,10)),drawstyle='steps-post',label="reversed potential")
plt.legend()

plt.figure('parabola')
y = np.power(x - AEgIS_trap.position * 2,2)/2000
y[:10]=0
y[-10:]=0
plt.plot(x,y,label='parabola',drawstyle='steps-mid')

calculated_potential = y @ __POTENTIAL_MATRIX_INV__
calculated_potential[-1]=0
real_potential = calculated_potential @ __POTENTIAL_MATRIX__
plt.plot(electrodes_position,calculated_potential, drawstyle='steps-post',label="calculated potentials to set")
plt.plot(x,real_potential,color='black',linestyle=(0,(5,10)), drawstyle='steps-post',label="real potential to set")
plt.legend()



plt.figure('janus')
AEgIS_trap = TTrap(position=-1095)
AEgIS_trap.SetElectrodeV('P8',190)
AEgIS_trap.SetElectrodeV('P9',190)
AEgIS_trap.SetElectrodeV('P10',180)
AEgIS_trap.SetElectrodeV('P11',180)
AEgIS_trap.SetElectrodeV('P12',180)
AEgIS_trap.SetElectrodeV('P13',190)
y = []
for electrode in AEgIS_trap.electrodes:
   for i in range(int(electrode.length / AEgIS_trap.dx)):
     y.append(electrode.GetPotential())
for i in range(40):
   y.append(0)

plt.plot(x,y,label='goal',drawstyle='steps-mid')
calculated_potential = y @ __POTENTIAL_MATRIX_INV__
calculated_potential[-1] = 0 
real_potential = calculated_potential @ __POTENTIAL_MATRIX__
plt.plot(electrodes_position,calculated_potential, drawstyle='steps-post',label="calculated potentials to set")
plt.plot(x,real_potential,color='black',linestyle=(0,(5,10)), drawstyle='steps-post',label="real potential to set")
plt.legend()


plt.show()