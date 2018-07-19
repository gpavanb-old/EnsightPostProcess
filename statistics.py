import numpy as np 

# Compute average gas property snapshot
def compute_wall_normal_stats(arr_data):
  snapshots = {}

  # Compute average number density profile
  nd_data = arr_data['ND']
  snapshots['ND'] = np.sum(nd_data,(0,1))

  # Compute wall normal velocity profiles
  vel_data = arr_data['V']
  vz_data = vel_data[:,:,:,2]
  snapshots['VZ'] = np.mean(vz_data,(0,1))
  snapshots['VZ_RMS'] = np.mean(vz_data*vz_data,(0,1))

  # Compute temperature profile
  temp_data = arr_data['TEMP']
  snapshots['TEMP'] = np.mean(temp_data,(0,1))

  # Compute mass fraction profile
  mf_data = arr_data['ZMIX']
  snapshots['ZMIX'] = np.mean(mf_data,(0,1))
  
  return snapshots

#def save_fig(snapList,timeList):
  

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
