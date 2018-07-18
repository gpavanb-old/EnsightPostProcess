import numpy as np 
import matplotlib.pyplot as plt

# Compute average gas property snapshot
#def compute_wall_normal_stats(arr_data):
#  snapshots = {}
#
#  # Reshape velocity data
#  vel_data = arr_data['V']
#  dimensions = vtk_data.GetDimensions()
#  vel_data_res = vel_data.reshape(shape[::-1]).transpose()
#
#  shape = tuple(dimensions)
#
#  # Extract variables
#  fields = {}
#  fields[array_name] =  array_data.reshape(shape[::-1]).transpose()
#
#
#  vel_data = vel_data.reshape((32,96,48,3))
#  vel_data = vel_data.transpose(2,1,0,3) 
#  print np.shape(vel_data)
#  mean_vel = np.mean(vel_data,(0,1))
#
#  # Check if wall-normal stats make sense
#  plt.plot(mean_vel[:,1])
#  plt.show()
#
#  print np.shape(mean_vel)
#  
#  return

#def compute_spalding_pdf(arr_data,nbins):
# Recover Spalding number from Sm
  
  

# Convert to histogram

def compute_turbulent_stokes_pdf(arr_data,nbins):
# Compute particle relaxation
  sgs_data = arr_data['KSGS']
  diam_data = arr_data['Diameter']

  rho_d = 1.372 
  mu_c = 1.49e-5
  rho_c = 43.9
  nu_c = mu_c/rho_c

  tau_p = rho_d * (diam_data ** 2)/(18 * mu_c)

# Compute local Kolmogorov time scale from KSGS
# and equilibrium assumption

  # Find cell data corresponding to particle locations
  

  tau_k = np.sqrt(nu_c/sgs_data)

  Stk = tau_p/tau_k

# Convert to histogram
  hist_data = np.histogram(Stk,nbins)   

  return hist_data

def compute_integrals(arr_data):
  integrals = {}

# Compute SMD, Mean and RMS velocities
  array_data = arr_data['Diameter']
  integrals['Mean_D'] = np.mean(array_data)
  integrals['Stdev_D'] = np.sqrt(np.mean(array_data**2) - np.mean(array_data)**2)
  integrals['SMD'] = np.sum( array_data**3 ) / np.sum( array_data**2 )

  array_data = arr_data['Velocity']
  RMS_vels = np.mean(array_data*array_data,0)
  integrals['RMS_Velocity'] = np.sqrt(np.sum(RMS_vels))
  integrals['wall_normal_RMS'] = np.sqrt(RMS_vels)[2]

  diameter_array = arr_data['Diameter']
  array_data = arr_data['Temperature']
  integrals['Mean_T'] = np.mean(array_data)
  integrals['Stdev_T'] = np.sqrt(np.mean(array_data**2) - np.mean(array_data)**2)
  integrals['weighted_TEMP'] = np.sum( diameter_array**3 * array_data ) / np.sum( diameter_array**3 )

  return integrals
