import collections, json, glob, os, time
from utils import table_list, mode_by_table



def exec_bsub(table, comment):
  if os.path.isfile( ".bsub_log" ):
    os.unlink( ".bsub_log" )
  os.popen( "bsub < BS/batch_scan_%s.txt > .bsub_log" % table ).read()
  ii = open( ".bsub_log" ).readlines()
  words = ii[0].split()
  jobid = words[1][1:-1]
  print ("batch_scan_%s.txt run as job %s" % (table,jobid) )
  oo = open( "batch_scan_log.txt", "a" )
  oo.write( "%s: batch_scan_%s.txt run as job %s: %s\n" % (time.ctime(),table,jobid,comment) )
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
  elif sys.argv[1] == "-x":
    table, comment = sys.argv[2:4]
    if table in table_list:
      exec_bsub( table, comment )
    elif table == "ALL":
      for table in table_list:
        exec_bsub( table, comment )
    else:
      print( "ERROR: table not recognised: %s" % table )
  elif sys.argv[1] == "-s":
    ddir, table = sys.argv[2:4]
    if table in table_list:
      batch_submit( ddir, table )
    elif table == "ALL":
      for table in table_list:
        batch_submit( ddir, table )
    else:
      print( "ERROR: table not recognised: %s" % table )
