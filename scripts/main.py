import glob, shelve, os, traceback, sys, random, time
import collections, traceback
from exceptions_lib import *
import local_utilities as lu

__version__ = "0.2.0"

##from config import *

def filter_listings( ddir, table="Amon", frequency=None, experiment="historical", listing_group = "x1" ):
  fl = glob.glob( "%s/%s_*_latest.txt" %  (ddir, listing_group) )
  fnl = [f.rpartition( "/" )[-1] for f in fl]
  assert frequency == None, "Frequency option not yet confiured"
  mode = "by_table"
  if mode == "by_table":
    tabstring = "_%s_" % table
    return [f for f in fnl if f.find( tabstring ) != -1]


if __name__ == "__main__":
  import sys
  mode = 'all'
  mode = 'sampledonepercent'
  default_mode = 'sampledonepercent'
  mode_config = {"Amon":"all","day":'sampledonepercent'}
##
## set up logs
##
  log_factory =lu.LogFactory(dir="./logs")
  log_global = log_factory( "global", mode="a", logfile="log_global_202004" )
  log_workflow = log_factory( "workflow", mode="a", warnings=True )

  if sys.argv[1] == "--sample":
    input_file = "../../cmor/inputs/byvar/x1_day_prsn_latest.txt"
    odir_tag = "sel02"
    sbv = scan_files.ShrinkByVar(mode)
    sbv.run(input_file,odir_tag,max_files=0)

  elif sys.argv[1] == "--listingByTable":
##
## run over a set of listing files
## 
    table, ddir, shelve_tag = sys.argv[2:]
    fl = filter_listings( ddir, table=table )
    log_global.info( "Main: Starting filtered listing:: %s" % sys.argv[1:] )
    print ( "INFO.001.00030: file list: ",fl )
    import scan_files 

    if table not in mode_config:
      log_global.warn( "warn.001.00010: table not in mode_config: " % table )
    mode = mode_config.get( table, default_mode )

    for f in fl[3:]:
      log_global.info( "Starting ExecuteByVar %s" %  [shelve_tag, f] )
      ebv = scan_files.ExecuteByVar(mode, log=log_workflow)
      input_file = "%s/%s" % (ddir,f)
      print (" --> ebv.run: ",input_file)
      ebv.run(input_file,shelve_tag,max_files=0)

  elif sys.argv[1] == "--exptvar":
    assert len(sys.argv) == 4
    log_global.info( "Starting ExecuteByVar %s" % sys.argv[1:] )
    shelve_tag, input_file = sys.argv[2:]
    import scan_files 
    ebv = scan_files.ExecuteByVar(mode, log=log_workflow)
    ebv.run(input_file,shelve_tag,max_files=0)
  elif sys.argv[1] == "--single":
    assert len(sys.argv) in  [4,5]
    shelve_file, data_file = sys.argv[2:4]
    sh = shelve.open( shelve_file )
    sh["__info__"] = {"title":"Scanning single data file: %s" % data_file, "source":"cmip6_range_check.main.ScanFile", "time":time.ctime(), "script_version":__version__}
    vn = data_file.split( "_" )[0].split('/')[-1]
    import scan_files 
    s = scan_files.ScanFile(data_file,sh, mode, vn=vn, checkSpecial=False,maskAll=False,maxnt=10000)
    if len( sys.argv ) == 5:
       data_file = sys.argv[4]
       s = scan_files.ScanFile(data_file,sh, mode, vn=vn, checkSpecial=False,maskAll=False,maxnt=10000)
    sh.close()
