import json
import matplotlib.pyplot as plt
import math
import numpy as np
import os
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

cutoff = 2049

# Read in file values as needed and create z array

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "ElectrodesPotentialMap.txt")
with open(file_path, 'r') as f:
    potential_values_all_string = np.array([l.strip().split("\t") for l in f.readlines()])[:, 1:cutoff]
potential_values_all = np.array([[float(value) for value in line] for line in potential_values_all_string])
z = np.array([0.5e-3 * n for n in range(1, cutoff)])

# Reduce to relevant P trap range
ptrap = range(22,36)
ptrap_ext = range(22,43)
# potential_values = np.array(potential_values_all[ptrap_ext, :])
potential_values = np.array(potential_values_all[ptrap, :])


#plt.imshow((z, ptrap), )

# Define potentials
P1 = P2 = P3 = P4 = P5 = P6 = P7 = P8 = P9 = P10 = P11 = P12 = P13 = P14 = 0 # To used them freely as placeholders
# This mostly are for the pbar/electrons separation
EndCap = -180
EndCap2 = -180
FloorRecycl = -40
P10 = -70 # -75.0
P11 = -65.7867 # -70 # 65.7867
P12 = -61.6964 # -66 # 61.6964
P14 = -47.8167 # -53 # 47.8167
PulseP9  = 110.0
PulseP13 = 124.6

#REAL Potentials maps for plots
potentials          = np.array([P1,     P2,     P3,             P4,             P5,             P6,             P7,             P8,             P9,         P10,        P11,    P12,    P13,    P14])#  HV3,    T1,     T2,     T3,     T4,     T5,     T6
test                = np.array([0,      180,    0,              0,              0,              180,            0,              0,              0,          0,          0,      0,      0,      0])
eloading            = np.array([0,      0,      0,              150,            150,            150,            150,            150,            -190,       -190,       -190,   0,      0,      0])
pbar_cooling        = np.array([0,      0,      0,              150,            150,            150,            150,            150,            0,          0,          0,      0,      0,      0])
ready_to_dump       = np.array([0,      0,     -150,            -10,            -10,            -10,            -10,            -10,            -150,       0,          0,      0,      0,      0])
transfer_prepare    = np.array([0,      0,     -150,            -10,            -10,            -10,            -10,            -10,            -150,       -150,       -150,   -150,   -150,   0])
transfer_extend     = np.array([0,      0,     -150,            -10,            -10,            -10,            -10,            -10,            -10,        -10,        -10,    -10,    -150,   0])
transfer_squeeze    = np.array([0,      0,     -150,            -150,           -150,           -150,           -150,           -150,           -150,       -10,        -10,    -10,    -150,   0])
transfer_float      = np.array([0,      0,     -150,            -150,           -150,           -150,           -150,           -150,           -150,       -70,        -70,    -70,    -150,   0])
recycling           = np.array([0,      0,     -150,            -40,            -40,            -40,            -40,            -40,            -150,       -70,        -70,    -70,    -150,   0])
parabola            = np.array([0,      0,     -150,            -40,            -40,            -40,            -40,            -40,            -150,       -70,        -68,    -66,    -150,   -57])
parabola_ext        = np.array([0,      0,     -150,            -40,            -40,            -40,            -40,            -40,            -150,       -70,        -65.8,  -62.1,  -150,   -47.5,  -38.5,  -29.9,  -22.2,  -15.3,  -9.2,   -4.1,   0])
parabola_ext_pulsed = np.array([0,      0,     -150,            -40,            -40,            -40,            -40,            -40,            -150,       -70,        -65.8,  -62.1,  -55.9,  -47.5,  -38.5,  -29.9,  -22.2,  -15.3,  -9.2,   -4.1,   0])


#FAKE Potentials maps for plots
potentials              = np.array([P1,     P2,     P3,     P4,     P5,     P6,     P7,     P8,     P9,     P10,        P11,    P12,    P13,    P14])
fake_ready_to_dump      = np.array([0,      0,      -180,   -10,    -10,    -10,    -10,    -10,    -180,   0,          0,      0,      0,      0])
fake_transfer_prepare   = np.array([0,      -180,   -180,   -10,    -10,    -10,    -10,    -10,    -180,   -180,       -180,   -180,   -180,   0])
fake_transfer_extend    = np.array([0,      -180,   -180,   -10,    -10,    -10,    -10,    -10,    -10,    -10,        -10,    -10,    -180,   0])
fake_transfer_squeeze   = np.array([0,      -180,   -180,   -180,   -180,   -180,   -180,   -180,   -180,   -10,        -10,    -10,    -180,   0])
fake_transfer_slope     = np.array([0,      -180,   -180,   -70,    -60,    -50,    -40,    -30,    -20,    -10,        -10,    -10,    -180,   0])
fake_transfer_slope2    = np.array([0,      -180,   -180,   -120,   -110,   -100,   -90,    -80,    -70,    -10,        -10,    -10,    -180,   0])
fake_transfer_float     = np.array([0,      -180,   -180,   -180,   -180,   -180,   -180,   -180,   -180,   -70,        -70,    -70,    -180,   0])
fake_recycling          = np.array([0,      -180,   -40,    -40,    -40,    -40,    -40,    -40,    -180,   -70,        -70,    -70,    -180,   0])
fake_parabola_ext       = np.array([0,      -180,   -40,    -40,    -40,    -40,    -40,    -40,    -180,   -70,        -65.8,  -62.1,  -180,   -47.5,  -38.5,  -29.9,  -22.2,  -15.3,  -9.2,   -4.1,   0])
fake_parabola_ext_pulsed= np.array([0,      -180,   -40,    -40,    -40,    -40,    -40,    -40,    -180,   -70,        -65.8,  -62.1,  -55.9,  -47.5,  -38.5,  -29.9,  -22.2,  -15.3,  -9.2,   -4.1,   0])


# We study if we can use the two pulses on P9 and P13 to separate electrons and pbars effectively
V0                  = np.array([0,      EndCap, FloorRecycl,    FloorRecycl,    FloorRecycl,    FloorRecycl,    FloorRecycl,    FloorRecycl,    EndCap,     P10,        P11,    P12,   EndCap2, P14])
V1                  = np.array([0,      EndCap, FloorRecycl,    FloorRecycl,    FloorRecycl,    FloorRecycl,    FloorRecycl,    FloorRecycl,    EndCap+PulseP9, P10,    P11,    P12,   EndCap2, P14])
# V2 = np.array([0, EndCap, FloorRecycl, FloorRecycl, FloorRecycl, FloorRecycl, FloorRecycl, FloorRecycl, EndCap+PulseP9, P10, P11, P12, EndCap2+PulseP13, P14])

#potentials = [V0[i] * potential_values[i] for i in range(len(V0))]
potentials1 = np.matmul(fake_transfer_slope, potential_values)
# potentials2 = np.matmul(fake_parabola_ext_pulsed, potential_values)
# potentials3 = np.matmul(V2, potential_values)


# Create a figure with the specified size (width and height, in inches) and DPI
plt.figure(figsize=(4, 3), dpi=300)
# Plot lines
plt.plot(z, potentials1) #, linestyle='--')
# plt.plot(z, potentials2)
# plt.plot(z, potentials3, label ="V2")
# Set labels etc.
plt.xlabel("z-position [m]")
plt.ylabel("Amplitude [V]")
#plt.xscale("log")
plt.xlim([0.5, 1])
plt.ylim([-200, 200])
# plt.title('')
# if plt.legend():
#     plt.legend().remove()
plt.tight_layout()

# Show plot
plt.show()


##############################################################################
# This was to place the trap figure on top of the graph, but it doesn't work...

# # Create a figure with the specified size (width and height, in inches) and DPI
# # plt.figure(figsize=(4, 3), dpi=300)
# fig, ax = plt.subplots()
# # Plot lines
# ax.plot(z, potentials1)
# ax.plot(z, potentials2)
# # plt.plot(z, potentials3, label ="V2")
# # Load the image
# img = plt.imread('C:\\Users\\marco\\Documents\\Mega\\Università\\PhD CERN\\Misc\\Trap config plotter\\5T_trap_axis.png')
# # Create an image object
# imagebox = OffsetImage(img, zoom=0.8)  # Adjust 'zoom' to scale your image size
# # Create an annotation box
# ab = AnnotationBbox(imagebox, (0.5, 1.2), xycoords='axes fraction', boxcoords="axes fraction",
#                     xybox=(0, 10), box_alignment=(0.5, 0), pad=0, frameon=False)
# # Add the image to the plot
# ax.add_artist(ab)
# # Optional: Adjust the main plot to make room for the inset image
# plt.subplots_adjust(top=1)

# # Set labels etc.
# ax.xlabel("z-position [m]")
# ax.ylabel("Amplitude [V]")
# #plt.xscale("log")
# ax.xlim([0.5, 1.0])
# ax.ylim([-200, 10])
# ax.title('')
# if ax.legend():
#     ax.legend().remove()
# ax.tight_layout()

# # Show plot
# plt.show()
