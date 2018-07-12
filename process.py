import os
import imp
import numpy as np
import csv
import sys
import os
from vtk.util import numpy_support
import vtk
##############################################################

def main():
  itestep = 2
  current_path= os.getcwd()
  input_file = sys.argv[1]
  up = imp.load_source('user_param', current_path+'/'+input_file)
  print current_path
  output = open( up.output, 'w', 0 )
  writer = csv.writer(output, delimiter=' ',
                       quotechar='|', quoting=csv.QUOTE_MINIMAL)
  load_loop_integrate(up, writer,itestep)
  output.close()

def write_data(curTime,integrals,writer,headwrite):
#Collect and write
  to_write = [curTime]
  keys = integrals.keys()

  if headwrite:
    headwrite = False
    writer.writerow ( ['time'] + keys  )

  for key in keys:
    to_write.append( integrals[key] )
  writer.writerow( to_write )

  return

def load_loop_integrate(params,writer,itestep):
# Test if file is present
  assert(os.path.exists(params.path))
  print('read file %s' %  params.path)
  headwrite = True

# Load info with vtk
  reader = vtk.vtkGenericEnSightReader()
  reader.SetCaseFileName(params.path)
  reader.Update()
  timeset = reader.GetTimeSets()
  time = timeset.GetItem(0)
  if time is not None:
    timesteps = time.GetSize()
  else:
    timesteps = 1

  print 'Number of Time steps found: ', timesteps

  for tstep in range(0, timesteps, itestep):
    if time is not None:
      curTime = time.GetTuple(tstep)[0]
      print 'Processing time: ', curTime
    else:
      curTime = 0
# Setting time to current value
    reader.SetTimeValue(curTime)
    reader.Update()
#Get cell data
    vtk_data = reader.GetOutput()
#Block 0 is flow, block 1 is particles
    block_data_flow = vtk_data.GetBlock(0)
    block_data_part = vtk_data.GetBlock(1)
    point_data_flow = block_data_flow.GetPointData()
    point_data_part = block_data_part.GetPointData()

    integrals = {}
    arr_data = {} 

# Loop over all arrays to find the variables of interest
# Repeat for flow and particles
    for array_idx in range(point_data_flow.GetNumberOfArrays()):
      array_name = point_data_flow.GetArrayName(array_idx)
      arr_data[array_name] = \
                numpy_support.vtk_to_numpy(point_data_flow.GetArray(array_idx))

    for array_idx in range(point_data_part.GetNumberOfArrays()):
      array_name = point_data_part.GetArrayName(array_idx)
      arr_data[array_name] = \
                numpy_support.vtk_to_numpy(point_data_part.GetArray(array_idx))

      compute_integrals(array_name,arr_data,integrals)

# Write header for first timestep
    write_data(curTime,integrals,writer,tstep==0)

def compute_integrals(array_name,arr_data,integrals):
  array_data = arr_data[array_name]

# Compute SMD, Mean and RMS velocities
  if array_name=='Diameter':
    integrals['Mean_D'] = np.mean(array_data)
    integrals['Stdev_D'] = np.sqrt(np.mean(array_data**2) - np.mean(array_data)**2)
    integrals['SMD'] = np.sum( array_data**3 ) / np.sum( array_data**2 )

  if array_name=='Velocity':
    integrals['RMS_Velocity'] = np.sqrt(np.mean(np.sum(array_data*array_data,1)))

  if array_name in ['Temperature']:
    diameter_array = arr_data['Diameter']
    integrals['weighted_'+array_name] = np.sum( diameter_array**3 * array_data ) / np.sum( diameter_array**3 )

if __name__ == '__main__':
    main()
