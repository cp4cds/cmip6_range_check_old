import matplotlib.pyplot as plt
import numpy as np
import netCDF4

def plot( file,ofile=None):
  nc = netCDF4.Dataset( file )
  fn = file.rpartition("/")[-1]
  label = fn.split("_")[0]
  var = nc.variables[label]
  long_name = var.long_name
  units = var.units
  if len(var.shape) > 2:
    print ( var.dimensions )
    var = var[0,:,:]
  lat = nc.variables["lat"]
  lon = nc.variables["lon"]

  fig = plt.figure(figsize=(6,5))
  left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
  ax = fig.add_axes([left, bottom, width, height]) 

  X, Y = np.meshgrid(lon, lat )

  cp = plt.contourf(X[:], Y[:], var[:])
  plt.colorbar(cp)

  ax.set_title("%s: %s [%s]" % (label,long_name,units))
  ax.set_xlabel('Longitude')
  ax.set_ylabel('Latitude')
  if ofile != None:
    plt.savefig( ofile )
  else:
    plt.show()

if __name__ == "__main__":
  import sys
  if len(sys.argv) == 1:
    plot( "../esgf_fetch/data_files/sftlf_fx_MIROC-ES2L_historical_r1i1p1f2_gn.nc" )
  else:
    file = sys.argv[1]
    ofile = None
    if len(sys.argv) == 3:
      ofile = sys.argv[2]
      plot ( file, ofile=ofile )
