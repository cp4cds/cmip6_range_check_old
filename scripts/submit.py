import collections, json, glob


def filter_listings( ddir, frequency=None, experiment="historical", listing_group = "x1" ):
  fl = glob.glob( "%s/%s_*_latest.txt" %  (ddir, listing_group) )
  cc = collections.defaultdict( set )
  fnl = [f.rpartition( "/" )[-1] for f in fl]
  assert frequency == None, "Frequency option not yet confiured"
  for f in fnl:
    table, var = f.split( "_" )[1:3]
    cc[table].add( var )
  ee = dict()
  for tab in sorted( list( cc.keys() ) ):
    ee[tab] = sorted( list( cc[tab] ) )
  oo = open( "%s/table_var_summary.json" % ddir, "w" )
  json.dump( {'info':{"title":"Table-variable summary"}, 'data':ee}, oo, indent=4, sort_keys=True )


def batch_submit(table):
  ee = json.load( open( "%s/table_var_summary.json" % ddir, "r" ) )
  assert table in ee, "Table name not recognised: %s" % table
  vars = ee[table]
  nv = len(vars)
  ii = ''.join( open( "batch_scan_template.txt", "r" ).readlines() )
  res = ii % (nv, " ".join(vars), table )
  oo = open( "batch_scan_latest.txt", "w" )
  oo.write(res)
  oo.close()
  ##os.popen( "bsub < batch_scan_latest.txt" ).read()

if __name__ == "__main__":
  import sys
  if sys.argv[1] == "-p":
    filter_listings( "inputs/byvar" )
  elif sys.argv[1] == "-s":
    ddir, table = sys.argv[2:4]
    batch_submit( ddir, table )