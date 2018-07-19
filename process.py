import os
import imp
import numpy as np
import csv
import sys
import os
from vtk.util import numpy_support
import vtk
from statistics import *
##############################################################

def main():
  itestep = 1
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

def create_case_grid(points):
  # Define grid
  NX = 48; NY = 96; NZ = 32
  XLO = 0; XHI = 0.00384
  DX = (XHI-XLO)/NX
  YLO = -0.0048; YHI = 0.0048
  DY = (YHI-YLO)/NY
  ZLO = 0; ZHI = 0.00256
  DZ = (ZHI-ZLO)/NZ

  for i in range(1,NX+1):
    for j in range(1,NY+1):
      for k in range(1,NZ+1):
        pt = [i*DX,YLO + j*DY,k*DZ]
        nextPoint1 = points.InsertNextPoint(pt)
  print "Created grid!"

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

# Flow block data is stored as an unstructured grid
# Convert block data to structured grid by querying at regular points
  points = vtk.vtkPoints() 
  polydata = vtk.vtkPolyData()
  create_case_grid(points)
  polydata.SetPoints(points)

  snapList = {}
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
    point_data_flow = block_data_flow.GetCellData()
    point_data_part = block_data_part.GetPointData()

# Set probe
    probe = vtk.vtkProbeFilter()
    probe.SetInputData(polydata)
    probe.SetSourceData(block_data_flow)
    probe.Update()
    result=probe.GetOutput()

    arr_data = {}
    # Get all scalars by probing
    for array_idx in range(point_data_flow.GetNumberOfArrays()):
      array_name = point_data_flow.GetArrayName(array_idx)
      arr_data[array_name] = numpy_support.vtk_to_numpy(result.GetPointData().GetArray(array_name))
      # Reshape data
      if (array_name == "V"):
        arr_data[array_name] = arr_data[array_name].reshape([48,96,32,3])
      else:
        arr_data[array_name] = arr_data[array_name].reshape([48,96,32])
    print "Read gas!"

# Loop over all arrays to find the variables of interest
# For particles, get directly from Ensight
    for array_idx in range(point_data_part.GetNumberOfArrays()):
      array_name = point_data_part.GetArrayName(array_idx)
      arr_data[array_name] = \
                numpy_support.vtk_to_numpy(point_data_part.GetArray(array_idx))
    print "Read particles!"
    
    if (params.statistics_type == 'integrals'):
      # Need to pass return as argument, because it is appended in each pass
      integrals = compute_integrals(arr_data)
      write_data(curTime,integrals,writer,tstep==0)
    elif (params.statistics_type == 'wall_normal'):
      snapList[tstep] = compute_wall_normal_stats(arr_data)
      np.save("snapList.npy",snapList) 
      print "Saved statistics"

  #if (params.statistics_type == 'wall_normal'): 
    #save_fig(timeList,snapList)

if __name__ == '__main__':
    main()
