# Plot saved snapshots from wall-normal statistics

import numpy as np
import matplotlib.pyplot as plt

# Empty index to extract dictionary
snapList = np.load("snapList.npy")[()]

# Initialize arrays
nd = np.zeros((32,200))
vz = np.zeros((32,200))
vz_rms = np.zeros((32,200))
temp = np.zeros((32,200))
yf = np.zeros((32,200))

# Scaling
d0 = 80e-6
U = 23.75
t_ref = d0/U

# Assemble matrices
for i in range(0,200):
  # ND
  nd[:,i] = snapList[i]['ND']

  # VZ
  vz[:,i] = snapList[i]['VZ']

  # VZ_RMS
  vz_rms[:,i] = snapList[i]['VZ_RMS']

  # TEMP
  temp[:,i] = snapList[i]['TEMP']

  # YF
  yf[:,i] = snapList[i]['ZMIX']

# Plot figures
x = np.linspace(0,4e-3/t_ref,200)
y = np.linspace(-0.5,0.5,32)
fig = plt.figure(facecolor='white')
CS=plt.contourf(x,y,nd,30,cmap=plt.cm.bone)
plt.title('Particle Count');
# Make a colorbar for the ContourSet returned by the contourf call.
cbar = plt.colorbar(CS); cbar.ax.set_ylabel('Particle count')
plt.xlabel('t*U/d'); plt.ylabel('y/h')

fig = plt.figure(facecolor='white')
CS=plt.contourf(x,y,vz/U,30,cmap=plt.cm.bone)
plt.title('Wall-normal velocity');
# Make a colorbar for the ContourSet returned by the contourf call.
cbar = plt.colorbar(CS); cbar.ax.set_ylabel('Vy')
plt.xlabel('t*U/d'); plt.ylabel('y/h')

fig = plt.figure(facecolor='white')
CS=plt.contourf(x,y,vz_rms/U,30,cmap=plt.cm.bone)
plt.title('Wall-normal velocity RMS');
# Make a colorbar for the ContourSet returned by the contourf call.
cbar = plt.colorbar(CS); cbar.ax.set_ylabel('Vy RMS')
plt.xlabel('t*U/d'); plt.ylabel('y/h')

fig = plt.figure(facecolor='white')
CS=plt.contourf(x,y,temp,30,cmap=plt.cm.bone)
plt.title('Temperature');
# Make a colorbar for the ContourSet returned by the contourf call.
cbar = plt.colorbar(CS); cbar.ax.set_ylabel('Temperature')
plt.xlabel('t*U/d'); plt.ylabel('y/h')

fig = plt.figure(facecolor='white')
CS=plt.contourf(x,y,yf,30,cmap=plt.cm.bone)
plt.title('Mass Fraction');
# Make a colorbar for the ContourSet returned by the contourf call.
cbar = plt.colorbar(CS); cbar.ax.set_ylabel('Mass Fraction')
plt.xlabel('t*U/d'); plt.ylabel('y/h')

plt.show()

