import os
import numpy as np
import matplotlib.pyplot as plt
import scipy as sc

def make_electrode_array():
    V = []
    V.append({'name':"C0",'from':0.0,'size':13.5,'V':0})
    V.append({'name':"HV1",'from':23.5,'size':40.0,'V':0})
    V.append({'name':"C1",'from':73.5,'size':27.5,'V':0})
    for i in range(2,6):
        V.append({'name':f"C{i}",'from':101.0 + (i-2)*30,'size':30,'V':0})
    for i in range(6,16):
        V.append({'name':f"C{i}",'from':221.0 + (i-6)*13.5,'size':13.5,'V':0})
    for i in range(16,19):
        V.append({'name':f"C{i}", 'from':356.0 + (i-16)*30.0,'size':30.0,'V':0})
    V.append({'name':"C19", 'from':446.0,'size':27.5,'V':0})
    V.append({'name':"HV2",'from':483.5,'size':40.0,'V':0})
    V.append({'name':"P1", 'from':533.5,'size':24.0,'V':0})
    V.append({'name':"P2", 'from':557.5,'size':30.0,'V':0})
    for i in range(3,13):
        V.append({'name':f"P{i}",'from':587.5+(i-3)*13.5,'size':13.5,'V':0})
    V.append({'name':"P13",'from':722.5,'size':30.0,'V':0})
    V.append({'name':"P14",'from':752.5,'size':24.0,'V':0})
    V.append({'name':"HV3",'from':786.5,'size':40,'V':0})
    V.append({'name':"T1",'from':836.5,'size':27.5,'V':300})
    for i in range(2,6):
        V.append({'name':f"T{i}", 'from':864.0+(i-2)*40,'size':40.0,'V':0})
    V.append({'name':"T6",'from':1024,'size':40.0,'V':0})
    return V

script_dir=os.path.dirname(__file__)
potential_matrix_path = os.path.join(script_dir, "ElectrodesPotentialMap.txt")
GROUNDED_ELECTRODES = ['C1'] # ,'C16','C17'
with open(potential_matrix_path, 'r') as f:
   __POTENTIAL_MATRIX__ = np.array([[float(value) for value in l.strip().split("\t")[1:2049]] if l.strip().split("\t")[0] not in  GROUNDED_ELECTRODES else [0]*2048 for l in f.readlines()])   

__POTENTIAL_MATRIX_INV__ = sc.linalg.pinv(__POTENTIAL_MATRIX__)

electrodes = make_electrode_array()

# for electrode in electrodes:
#     print(f"{electrode['name']} at {electrode['from']}-{electrode['from']+electrode['size']}")


set_potential = np.array([electrode['V'] for electrode in electrodes])
real_potential = __POTENTIAL_MATRIX__.T @ set_potential
recalculated_potential = real_potential @ __POTENTIAL_MATRIX_INV__

dx = (electrodes[-1]['from'] + electrodes[-1]['size'])/(__POTENTIAL_MATRIX__.shape[1])

electrodes_position = [electrode['from'] for electrode in electrodes]
# electrodes_position.append(electrodes_position[-1]+electrodes[-1]['size'])

x=np.arange(__POTENTIAL_MATRIX__.shape[1])*0.5

plt.figure(1)
plt.plot(x,real_potential,drawstyle='steps-mid',label="real potential")
plt.plot(electrodes_position,set_potential,drawstyle='steps-post',label="set potential")
plt.plot(electrodes_position,recalculated_potential,color='black',linestyle=(0,(5,10)),drawstyle='steps-post',label="reversed potential")
plt.legend()

plt.figure('parabola')
y = np.power(x - __POTENTIAL_MATRIX__.shape[1] * 0.5 / 2,2)/2000
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
def make_potential(x):
    floor=180
    wall=190
    return wall*(sc.stats.norm.pdf(x,loc=370,scale=10) + sc.stats.norm.pdf(x,loc=430,scale=10)) + floor*sc.stats.norm.pdf(x,loc=400,scale=10)
y = make_potential(x)

set_potential = np.array([electrode['V'] for electrode in electrodes])
y = set_potential

plt.plot(x,y,label='goal',drawstyle='steps-mid')
calculated_potential = y @ __POTENTIAL_MATRIX_INV__
calculated_potential[-1] = 0 
real_potential = calculated_potential @ __POTENTIAL_MATRIX__
plt.plot(electrodes_position,calculated_potential, drawstyle='steps-post',label="calculated potentials to set")
plt.plot(x,real_potential,color='black',linestyle=(0,(5,10)), drawstyle='steps-post',label="real potential to set")
plt.legend()


plt.show()