import netCDF4, glob, numpy, shelve, os, traceback, sys, random, time
import collections, traceback
from exceptions_lib import *
import scan_files 
import local_utilities as lu

__version__ = "0.2.0"

##from config import *


if __name__ == "__main__":
  import sys
  mode = 'all'
  mode = 'sampledonepercent'
  log_factory =lu.LogFactory(dir="./logs")
  log_global = log_factory( "global", mode="a", logfile="log_global_202004" )
  log_workflow = log_factory( "workflow", mode="a", warnings=True )
  if sys.argv[1] == "--exptvar":
    assert len(sys.argv) == 4
    log_global.info( "Starting ExecuteByVar %s" % sys.argv[1:] )
    shelve_tag, input_file = sys.argv[2:]
    ebv = scan_files.ExecuteByVar(mode, log=log_workflow)
    ebv.run(input_file,shelve_tag,max_files=0)
  elif sys.argv[1] == "--single":
    assert len(sys.argv) == 4
    shelve_file, data_file = sys.argv[2:]
    sh = shelve.open( shelve_file )
    sh["__info__"] = {"title":"Scanning single data file: %s" % data_file, "source":"cmip6_range_check.main.ScanFile", "time":time.ctime(), "script_version":__version__}
    vn = data_file.split( "_" )[0].split('/')[-1]
    s = scan_files.ScanFile(data_file,sh, mode, vn=vn, checkSpecial=False,maskAll=False,maxnt=10000)
