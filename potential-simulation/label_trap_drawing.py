from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from electrode import TElectrode
from trap import TTrap
import os

AEgIS_trap = TTrap(position=-1065-6.8-31) # 1065 - length of 5T trap, 6.8 - gap between 5T and 1T traps, 31 - half of B0 electrode
electrodes_5T = len(AEgIS_trap.electrodes)
position_1T = AEgIS_trap.electrodes[-1].GetElectrodeEnd() + 6.8
print(position_1T)
AEgIS_trap.electrodes.append(TElectrode("B0",position_1T,62.0))
for i in range(1,8):
    AEgIS_trap.electrodes.append(TElectrode(f"B{i}",position_1T+62.95+(i-1)*(43),42.0))
for i in range(8,11):
    AEgIS_trap.electrodes.append(TElectrode(f"B{i}",position_1T+363.95+(i-8)*16,15.0))
for i in range(4,7):
    AEgIS_trap.electrodes.append(TElectrode(f"HV{i}",position_1T+411.95+(i-4)*17,15.0))
for i in range(4):
    AEgIS_trap.electrodes.append(TElectrode(f"A{8-i}",position_1T+461.95+i*16,15.0))
for i in range(4):
    AEgIS_trap.electrodes.append(TElectrode(f"A{4-i}",position_1T+525.95+i*8.5,7.5))
AEgIS_trap.Print()

dpi=300 # pixels per inch
fontsize = 20
linewidth = 1.7
headwidth = 20
color = 'cornflowerblue'

fig_5T = plt.figure(figsize=(6563/dpi/0.8,3009/dpi/0.8))
ax_5T = fig_5T.add_subplot(anchor='NW')
img_5T = np.asarray(Image.open("C:\\Users\\jzielins\\OneDrive - Politechnika Warszawska\\AEgIS\\technical\\5T_trap-simplified.jpg"))
imgplot_5T = ax_5T.imshow(img_5T)
ax_5T.set_ylim()
ax_5T.margins(0,0)
ax_5T.set_axis_off()
# ax_5T.vlines([0,109.8,6319.2,6400,6563],ymin=0,ymax=3009)
# trap in the image starts at 6401 and ends at 108
# the thickness of the line is 4 pixels
# therefore the entire 5T trap is from 110 to 6399, which corresponds to 1065.00 mm
trap_5T_start = 6401
trap_5T_end = 110
trap_5T_legnth = AEgIS_trap.electrodes[electrodes_5T-1].GetElectrodeEnd() - AEgIS_trap.electrodes[0].GetElectrodeStart()
ppm_5T = (trap_5T_start - trap_5T_end) / trap_5T_legnth # pixels per mm
print("5T length:",trap_5T_legnth)
print("5T pixels per milimeter:",ppm_5T)
previous_electrode_end = 0
for i, electrode in enumerate(AEgIS_trap.electrodes[:electrodes_5T]):
    # position label
    label_pos = trap_5T_start - (electrode.GetElectrodeEnd()-AEgIS_trap.position)*ppm_5T
    ax_5T.vlines(label_pos,ymin=0.67*3009 + (i==electrodes_5T-1)*340,ymax=0.53*3009,color=color,lw=linewidth)
    # ax_5T.text(label_pos, 0.67*3009+50 + (i==electrodes_5T-1)*340, f'{AEgIS_trap.electrodes[electrodes_5T-1].GetElectrodeEnd() - electrode.GetElectrodeEnd()}', horizontalalignment= 'center', verticalalignment='top', rotation="vertical",size=fontsize)
    ax_5T.text(label_pos, 0.67*3009+50 + (i==electrodes_5T-1)*340, f'{electrode.GetElectrodeEnd():.1f}', horizontalalignment= 'center', verticalalignment='top', rotation="vertical",size=fontsize)
    if abs(previous_electrode_end - electrode.GetElectrodeStart()) > 2:
        label_pos = trap_5T_start - (electrode.GetElectrodeStart()-AEgIS_trap.position)*ppm_5T
        ax_5T.vlines(label_pos,ymin=0.7*3009+250,ymax=0.53*3009,color=color,lw=linewidth)
        # ax_5T.text(label_pos, 0.7*3009+300, f'{AEgIS_trap.electrodes[electrodes_5T-1].GetElectrodeEnd() - electrode.GetElectrodeStart()}', horizontalalignment= 'center', verticalalignment='top', rotation="vertical",size=fontsize)
        ax_5T.text(label_pos, 0.7*3009+300, f'{electrode.GetElectrodeStart():.1f}', horizontalalignment= 'center', verticalalignment='top', rotation="vertical",size=fontsize)
    previous_electrode_end = electrode.GetElectrodeEnd()

    # electrode label
    label_pos = trap_5T_start - (electrode.GetElectrodeCenter()-AEgIS_trap.position)*ppm_5T
    label_name = electrode.GetName()
    if label_name in ['P13','P3','P2','C16','C6','C5']:
        label_name += 'i'
    elif label_name in ['P8','P7','C11','C10']:
        label_name += '(a,b,c,d)'
    ax_5T.text(label_pos, 0.28*3009, f'{label_name}', horizontalalignment= 'center', verticalalignment='bottom', rotation='vertical',size=fontsize)
    ax_5T.arrow(label_pos,0.3*3009,0,0.18*3009,length_includes_head=True,head_width=headwidth,linewidth=linewidth,color=color)
ax_5T.text(trap_5T_end-100,3009/2+20,"1T\nside",horizontalalignment= 'center',verticalalignment='center',fontsize=fontsize,rotation='vertical')
ax_5T.text(trap_5T_start+100,3009/2+20,"AD\nside",horizontalalignment= 'center',verticalalignment='center',fontsize=fontsize,rotation='vertical')
fig_5T.tight_layout()
fig_5T.savefig(os.path.join(os.path.dirname(__file__),"plots","5T_labeled.png"),dpi=600)

# 1T trap
fig_1T = plt.figure(figsize=(3711/dpi/0.8,1711/dpi/0.8))
ax_1T = fig_1T.add_subplot(anchor='NW')
img_1T = np.asarray(Image.open("C:\\Users\\jzielins\\OneDrive - Politechnika Warszawska\\AEgIS\\technical\\1T_trap-simplified.jpg"))
imgplot_1T = ax_1T.imshow(img_1T)
ax_1T.set_axis_off()

trap_1T_start = 3655
trap_1T_end = 355
trap_1T_legnth = AEgIS_trap.electrodes[-1].GetElectrodeEnd() - AEgIS_trap.electrodes[electrodes_5T].GetElectrodeStart()
ppm_1T = (trap_1T_start - trap_1T_end) / trap_1T_legnth # pixels per mm
print("1T length:",trap_1T_legnth)
print("1T pixels per milimeter:",ppm_1T)
previous_electrode_end = 0

scale =0.6 # 3711 / 6563 
# print(scale)
for i, electrode in enumerate(AEgIS_trap.electrodes[electrodes_5T:]):
    # position label
    # label_pos = trap_5T_start - (electrode.GetElectrodeEnd()-AEgIS_trap.position)*ppm_5T
    label_pos = trap_1T_start - (electrode.GetElectrodeEnd() - position_1T)*ppm_1T
    ax_1T.vlines(label_pos,ymin=0.9*1711,ymax=0.53*1711,color=color,lw=linewidth*scale)
    # ax_1T.text(label_pos, 0.9*1711+30, f'{electrode.GetElectrodeEnd() - AEgIS_trap.electrodes[electrodes_5T-1].GetElectrodeEnd():.1f}', horizontalalignment= 'center', verticalalignment='top', rotation="vertical",size=fontsize*scale)
    ax_1T.text(label_pos, 0.9*1711+30, f'{electrode.GetElectrodeEnd():.1f}', horizontalalignment= 'center', verticalalignment='top', rotation="vertical",size=fontsize*scale)
    if abs(previous_electrode_end - electrode.GetElectrodeStart()) > 2:
        # label_pos = trap_1T_start - (electrode.GetElectrodeStart()- AEgIS_trap.electrodes[electrodes_5T].GetElectrodeStart())*ppm_1T
        label_pos = trap_1T_start - (electrode.GetElectrodeStart()- position_1T)*ppm_1T
        ax_1T.vlines(label_pos,ymin=0.9*1711,ymax=0.53*1711,color=color,lw=linewidth*scale)
        # ax_1T.text(label_pos, 0.9*1711+30, f'{electrode.GetElectrodeStart() - AEgIS_trap.electrodes[electrodes_5T-1].GetElectrodeEnd():.1f}', horizontalalignment= 'center', verticalalignment='top', rotation="vertical",size=fontsize*scale)
        ax_1T.text(label_pos, 0.9*1711+30, f'{electrode.GetElectrodeStart():.1f}', horizontalalignment= 'center', verticalalignment='top', rotation="vertical",size=fontsize*scale)
    previous_electrode_end = electrode.GetElectrodeEnd()

    # electrode label
    # label_pos = trap_1T_start - (electrode.GetElectrodeCenter()- AEgIS_trap.electrodes[electrodes_5T].GetElectrodeStart())*ppm_1T
    label_pos = trap_1T_start - (electrode.GetElectrodeCenter()- position_1T)*ppm_1T
    label_name = electrode.GetName()
    if label_name in ['A8','B10','B0']:
        label_name += '(a,b,c,d)'
    ax_1T.text(label_pos, 0.1*1711, f'{label_name}', horizontalalignment= 'center', verticalalignment='bottom', rotation='vertical',size=fontsize*scale)
    ax_1T.arrow(label_pos,0.12*1711,0,0.334*1711,length_includes_head=True,head_width=headwidth*scale,color=color,lw=linewidth*scale)
ax_1T.text(trap_1T_start+50,1711/2,"5T\nside",horizontalalignment= 'center',verticalalignment='center',fontsize=fontsize*scale,rotation='vertical')
ax_1T.margins(0,0)

fig_1T.tight_layout()
fig_1T.savefig(os.path.join(os.path.dirname(__file__),"plots","1T_labeled.png"),dpi=600)

plt.show()