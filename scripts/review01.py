import numpy, json, shelve, os, glob
import collections
from exceptions_lib import *

__TODO__ = """ADD DRS and TIME RECORDS to INFO"""

print( __TODO__ )


class ConsolidateVar(object):
  def __init__(self,lax=True):
    self.lax = lax

  def run(self,idir):
    assert os.path.isdir(idir)
    (root,x,var) = idir.strip('/').rpartition('/')
    fl = glob.glob( "%s/*.json" % idir )
    ee = dict()
    tech= dict()
    cc = collections.defaultdict( set )
    for f in fl:
      fn = f.rpartition('/')[-1]
      this = json.load( open( f, 'r' ) )
      for k in ['summary','percentiles']:
        cc[k].add( tuple( this['info']['tech'][k] ) )
      if "drs" not in this["info"].keys():
        if not self.lax:
          raise WorkflowException( "drs record not found in header", file=f, directory=idir)
        else:
          inst, model, experiment = fn.split( '_' )[1:4]
      else:
          raise WorkflowException( "not programmed to handle drs record", class_name="ConsolidateVar", module="review01.py")
      ee['%s_%s_%s' % (inst,model,experiment)] = this['data']

    for k in ['summary','percentiles']:
      assert len(cc[k]) == 1
      tech[k] = cc[k].pop()
  
    self.root = root
    self.drs = {"experiment":experiment,"var":var}
    self.res = {"data":ee, "info":{"tech":tech, "title":"aggregation across %s" % idir, "drs":self.drs } }
    oo = open( "%s/%s_%s_consol-var.json" % (root,var,experiment), "w" )
    json.dump( self.res, oo, indent=4, sort_keys=True )
    oo.close()
    print( tech )

  def checkConsol(self):
    data = self.res['data']
    drs = self.res['info']['drs']
    ks = sorted( list( data.keys() ) )
    if len( ks ) < 6:
       print( "WARNING: model count [%s] low for %s" % (len(ks),drs["var"]) )
    elif len( ks ) < 12:
       print( "ERROR: model count [%s] sub-critical for %s" % (len(ks),drs["var"]) )

    
    medians = {k:x["percentiles"][4] for k,x in data.items()}
    interquartiles = {k:abs(x["percentiles"][3] - x["percentiles"][5]) for k,x in data.items()}
    self.this = numpy.percentile( [x for k,x in medians.items()], [75.,50.,25.] )
    self.thisiq = numpy.percentile( [x for k,x in interquartiles.items()], [75.,50.,25.] )
    median_interquartile0 = self.thisiq[1]
    h,m,l = self.this[:]
    median_interquartile1 = abs(h-l)
    out = [k for k,x in medians.items() if abs( x-m) > 4*median_interquartile1 ]
    if len(out) > 0:
      for k in out:
        print ("ERROR: median outside expected range: %s, %s, %s" % (k,medians[k], self.this[:]) )
    self.medians = medians
    self.intequartiles = interquartiles

  def dumpCsv(self,ofile=None):
    if ofile == None:
      ofile = "%(var)s_%(experiment)s_consol-var.csv" % self.drs 
    oo = open( ofile, "w" )
    data = self.res["data"]
    headings = ["Model","Maximum","Minimum",] +  [str(x) for x in self.res["info"]["tech"]["percentiles"]]
    oo.write( "\t".join( headings ) + "\n" )
    for k in sorted( list( data.keys() ) ):
      inst,model,expt = k.split( '_')
      rec = ['%s %s' % (inst,model),] + [str(x) for x in (data[k]["summary"][1:3] + data[k]["percentiles"]) ]
      oo.write( "\t".join( rec ) + "\n" )
    oo.close()
      
    
class Review(object):
  def __init__(self):
    pass

  def loadShelve(self,file):
    sh = shelve.open( file, 'r' )

    self.info = {"title":"From %s" % file }
    ks = [k for k in sh.keys() if k[0] != "_"]
    nt = sum( [len(sh[k][5]) for k in ks ] )
    nf = len( ks )
    print (nt)
    self.work = numpy.zeros( (9,nt) )
    self.work02 = numpy.zeros( (5,nf) )
    i = 0
    j = 0
    for k in sorted( ks ):
      for l in sh[k][6]:
        self.work[:,i] = l
        i += 1
      self.work02[:,j] = sh[k][4][1:6]
      j += 1
    sh.close()

  def loadJson(self,file):
    ee = json.load( open( file, 'r' ) )

    self.info = ee['info']
    dd = ee['data']
    nt = sum( [len(dd[k][5]) for k in dd.keys() ] )
    nf = len( dd.keys() )
    print (nt)
    self.work = numpy.zeros( (9,nt) )
    self.work02 = numpy.zeros( (5,nf) )
    i = 0
    j = 0
    for k in sorted( list( dd.keys() ) ):
      for l in dd[k][6]:
        self.work[:,i] = l
        i += 1
      self.work02[:,j] = dd[k][4][1:6]
      j += 1

  def run(self,file):
    assert os.path.isfile( file ) or  os.path.isfile( "%s.dat" % file ), "File not found: %s" % ifile
    if file[-5:] == ".json":
      self.loadJson(file)
      ofile = file.replace( ".json", "_summary.json" ).replace('sh_ranges','json_ranges')
    else:
      self.loadShelve(file)
      ofile = file + "_summary.json"
      ofile = ofile.replace('sh_ranges','json_ranges')
    odir = ofile.rpartition( '/' )[0]
    if not os.path.isdir( odir ):
      os.mkdir( odir )
  

    summary = [0.]*5
    percentiles = [0.]*9
    for k in range(9):
      percentiles[k] = numpy.median( self.work[k,:] )

    summary[0] = numpy.median( self.work02[0,:] )
    summary[1] = numpy.max( self.work02[1,:] )
    summary[2] = numpy.min( self.work02[2,:] )
    summary[3] = numpy.max( self.work02[3,:] )
    summary[4] = numpy.max( self.work02[4,:] )

    print ( percentiles, summary )

    this = {'percentiles':percentiles, "summary":summary}
    oo = open( ofile, 'w' )
    info_out = {'title':self.info['title'], "tech":{"percentiles":[99.9,99.,95.,75.,50.,25.,5.,1.,.1], "summary":["median","max","min","mean absolute max","mean absolute min"]}}
    json.dump( {'info':info_out, 'data':this}, oo, indent=4, sort_keys=True )
    oo.close()

## l0: ['ok','shape','median','mx','mn','mamx','mamn','nfv','hasfv','dt0','dt1','units','tid']

      

r = Review()


if __name__ == "__main__":
  import sys
  print (sys.argv)
  if sys.argv[1] == "-c":
    c = ConsolidateVar()
    try:
      c.run( sys.argv[2] )
    except WorkflowException as e:
      print (e.msg)
      print (e.kwargs)
      raise
    except:
      raise
    c.dumpCsv()
  elif sys.argv[1] == "-d":
    idir = sys.argv[2]
    fl = glob.glob( "%s/*.dat" % idir )
    for f in sorted( fl ):
      print ("START: %s" % f )
      r.run( f[:-4] )
  else:
    ifile = sys.argv[1]
    r.run( ifile )
    ##r.run( 'hurs_AS-RCEC_TaiESM1_historical_00-01.json' )
