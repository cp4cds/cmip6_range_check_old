import collections, json, glob, os, time
from local_utilities import WGIPriority
from utils import table_list, mode_by_table


def filter_listings( ddir, frequency=None, experiment="historical", listing_group = "x1", bywg1=True ):
  fl = glob.glob( "%s/%s_*_latest.txt" %  (ddir, listing_group) )
  cc = collections.defaultdict( set )
  fnl = [f.rpartition( "/" )[-1] for f in fl]
  assert frequency == None, "Frequency option not yet confiured"

  if bywg1:
    wg1 = WGIPriority()
  for f in fnl:
    table, var = f.split( "_" )[1:3]
    if (not bywg1) or "%s.%s" % (table,var) in wg1.ee:
      cc[table].add( var )
  ee = dict()
  for tab in sorted( list( cc.keys() ) ):
    ee[tab] = sorted( list( cc[tab] ) )
  oo = open( "%s/table_var_summary.json" % ddir, "w" )
  json.dump( {'info':{"title":"Table-variable summary"}, 'data':ee}, oo, indent=4, sort_keys=True )

def exec_bsub(table, comment, is_file=False):
  if is_file:
    cfile = table
  else:
    cfile = "BS/batch_scan_%s.txt" % table

  if os.path.isfile( ".bsub_log" ):
    os.unlink( ".bsub_log" )
  cmd = "sbatch %s > .bsub_log" % cfile
  print ('Executing cmd: ',cmd )
  os.popen( cmd ).read()
  ii = open( ".bsub_log" ).readlines()
  words = ii[0].split()
  jobid = words[-1]
  print ("%s run as job %s" % (cfile,jobid) )
  oo = open( "batch_scan_log.txt", "a" )
  oo.write( "%s: %s: %s run: %s\n" % (jobid, time.ctime(),cfile,comment) )
  oo.close()
  

def batch_submit(ddir,table):
  ee = json.load( open( "%s/table_var_summary.json" % ddir, "r" ) )
  assert table in ee["data"], "Table name not recognised: %s" % table
  vars = ee["data"][table]
  mode = mode_by_table[table]
  nv = len(vars)
  ii = ''.join( open( "batch_scan_template.txt", "r" ).readlines() )
  tag = "%s_v2" % table
  res = ii % {"n":nv, "table":table, "mode":mode, "experiment":"historical", "vars":" ".join(vars), "tag":tag }
  oo = open( "BS/batch_scan_%s.txt" % table, "w" )
  oo.write(res)
  oo.close()
  ##os.popen( "bsub < batch_scan_latest.txt" ).read()

if __name__ == "__main__":
  import sys
  if sys.argv[1] == "-p":
    filter_listings( "inputs/historical/byvar" )
  elif sys.argv[1] in ["-x","-f"]:
    table, comment = sys.argv[2:4]
    if sys.argv[1] == '-f':
       exec_bsub( table, comment, is_file=True )
    else:
      if table in table_list or any( [table.find(x) == 0 for x in table_list] ) or table[:4] in ['Misc', 'Fixe']:
        exec_bsub( table, comment )
      elif table == "ALL":
        for table in table_list:
          exec_bsub( table, comment )
      else:
        print( "ERROR: table not recognised: %s" % table )
  elif sys.argv[1] == "-a":
    table, comment = sys.argv[2:4]
    exec_bsub( table, comment )

  elif sys.argv[1] == "-s":
    ddir, table = sys.argv[2:4]
    if table in table_list:
      batch_submit( ddir, table )
    elif table == "ALL":
      for table in table_list:
        batch_submit( ddir, table )
    else:
      print( "ERROR: table not recognised: %s" % table )
