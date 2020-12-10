
import json, glob, os


def summary(ee):
  oo = dict()
  oo['header'] = ee['header']
  oo['data'] = dict( headers=ee['data']['headers'], summary=ee['data']['summary'] )
  return oo

def sum_file(ifile,odir):
    od = summary( json.load( open( ifile, 'r' ) ) )
    ifn = ifile.rpartition('/')[-1]
    istem = ifn.rpartition( '.' )[0]
    ofile  = '%s/%s_sum.json' % (odir,istem)
    oo = open( ofile,'w')
    json.dump( {'info':{"title":"Simulation-table-variable summary"}, 'data':od}, oo, indent=4, sort_keys=True )
    oo.close()


def sum_dir( idir, odir ):
    files = glob.glob( '%s/*.json' % idir )
    for f in files:
      sum_file( f, odir )

if __name__ == "__main__":
  import sys
  if sys.argv[1] == "-f":
    ifile = sys.argv[2]
    odir = sys.argv[3]
    sum_file( ifile, odir )
  elif sys.argv[1] == "-d":
    idir = sys.argv[2]
    odir = sys.argv[3]
    sum_dir( idir, odir )
  elif sys.argv[1] == "-a":
    iroot = sys.argv[2]
    oroot = sys.argv[3]
    for d in glob.glob( '%s/*' % iroot ):
      dd = d.rpartition( '/' )[-1]
      odir = '%s/%s' % (oroot,dd)
      if not os.path.isdir( odir ):
        os.mkdir( odir )
      sum_dir( d, odir )
  
    
  else:
    assert False, "should not be here"
