import numpy, json, shelve, os, glob, time
import collections
from exceptions_lib import *
import local_utilities

__TODO__ = """ADD DRS and TIME RECORDS to INFO"""

sh_ex01 = "sh_ranges/Emon/hus/hus_AS-RCEC_TaiESM1_historical_00-03"

print( __TODO__ )

log_factory =local_utilities.LogFactory(dir="./logs")


class ConsolidateVar(object):
  def __init__(self,lax=True, logid=None):
    self.lax = lax
    if logid != None:
      self.log_global = log_factory( "global", mode="a", logfile="log_review_%s_202005" % logid )
      self.log_workflow = log_factory( "review_workflow_%s" % logid, mode="a", warnings=True )
      self.logging = True
    else:
      self.logging = False

  def run(self,idir):
    if self.logging:
      self.log_workflow.info( "%s:: ConsolidateVar ( idir = %s )" % (time.ctime(),idir) )
    assert os.path.isdir(idir), "Directory not found: %s" % idir
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
          tab,var_xx,inst,model,experiment,grid,this_version = this["info"]["drs"]
          assert var == var_xx
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
       print( "ERROR.cons.00010: model count [%s] sub-critical for %s" % (len(ks),drs["var"]) )
       return
    elif len( ks ) < 12:
       print( "WARNING: model count [%s] low for %s" % (len(ks),drs["var"]) )
       
    
    medians = {k:x["percentiles"][4] for k,x in data.items()}
    interquartiles = {k:abs(x["percentiles"][3] - x["percentiles"][5]) for k,x in data.items()}
    self.medians = medians
    self.intequartiles = interquartiles
    self.this = numpy.percentile( [x for k,x in medians.items()], [75.,50.,25.] )
    self.thisiq = numpy.percentile( [x for k,x in interquartiles.items()], [75.,50.,25.] )
    median_interquartile0 = self.thisiq[1]
    h,m,l = self.this[:]
    median_interquartile1 = abs(h-l)
    out = [k for k,x in medians.items() if abs( x-m) > 4*median_interquartile1 ]
    if len(out) > 0:
      for k in out:
        print ("ERROR.cons.00100: Median outside expected range: %s, %s, %s" % (k,medians[k], self.this[:]) )
      if len(out) > len(ks)/10:
        print ("ERROR.cons.00110: more than 10%% of models have median out of range" )
        return

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
  def __init__(self, logid=None):
    if logid != None:
      self.log_global = log_factory( "global", mode="a", logfile="log_review_%s_202005" % logid )
      self.log_workflow = log_factory( "review_workflow_%s" % logid, mode="a", warnings=True )
      self.logging = True
    else:
      self.logging = False

  def loadShelve(self,file):
    sh = shelve.open( file, 'r' )
    if self.logging:
      self.log_workflow.info( "%s:: loadShelve ( file = %s )" % (time.ctime(),file) )

### percentiles
    if "__tech__" in sh.keys():
      self.input_tech = sh["__tech__"]
      self.npct = len( self.input_tech["percentiles"] )
    else:
      print( "WARNING: no __tech__ in %s" % file )
      print (sh.keys() )
      self.input_tech = None
      self.npct = 13

    if "__info__" in sh.keys():
      try:
        self.info = sh["__info__"]
      except:
        self.info = {"title":"From %s" % file, "WARNING":"Could not read __info__ record from %s" % file }
        print ("WARNING:Could not read __info__ record from %s" % file )
    else:
      self.info = {"title":"From %s" % file }

    ks = [k for k in sh.keys() if k[0] != "_"]
    assert len(ks) > 0, "no data records in %s" % file

    self.withLevels = ":l=" in ks[0]
    if self.withLevels:
      lindx = collections.defaultdict( dict )
      lindy = collections.defaultdict( dict )
      ss = set()
      for x in ks:
        a,xxx,b = x.rpartition(":")
        ib = int( b.rpartition("=")[-1] )
        lindx[a][ib] = x
        lindy[ib][a] = x
        ss.add(b)
      sfn = sorted( list( lindx.keys() ) )

      nl = len(ss)
      self.levels = [int( x.rpartition("=")[-1] ) for x in sorted( list (ss) )]
      print ("LEVELS: ",self.levels,ss)

      nlevels = len(ss)
      nfiles = len(sfn)
    else:
      nfiles = len(ks)

    ixsum = 5
    ixabs = 6
    ixpct = 7

    
    self.file_summary = []

    if self.withLevels:
#
# extract numer of time steps available at each level
      ntime_by_levels = [ sum( [len(sh[v][ixabs]) for k,v in lindy[lev].items()] ) for lev in lindy.keys() ]

      ntime = max( ntime_by_levels )
      self.work = numpy.ma.zeros( (self.npct,ntime,nlevels) )
      self.work02 = numpy.ma.zeros( (5,nfiles,nlevels) )
      i = 0
      j = 0
#
# loop over levels present
#
      self.ntl = dict()
      for ilev in range(nlevels):
        lev = self.levels[ilev]
        i = 0
        for k in range(nfiles):
          fn = sfn[k]
          if fn in lindy[lev].keys():
            kk = lindy[lev][fn]
            rec = sh[kk]
            self.work02[:,k,ilev] = rec[ixsum][:5]

            dt0, dt1 = [float(x) for x in rec[ixsum][5:7]]
            fvcount = int( rec[ixsum][7] )
            self.file_summary.append( [dt0, dt1, fvcount] )
#
# loop over time slices
#
            for this in rec[ixpct]:
                print (fn,lev,i,max(this),min(this))
                self.work[:,i,ilev] = this
                i += 1
        self.ntl[lev] = i

    else:
      ntime = sum( [len(sh[k][ixabs]) for k in ks] )
      print ( "INFO: nt=%s [nf=%s]" % (ntime,nfiles ) )
      self.work = numpy.ma.zeros( (self.npct,ntime) )
      self.work02 = numpy.ma.zeros( (5,nfiles) )
      i = 0
      j = 0
      for k in sorted( ks ):
        for l in sh[k][ixpct]:
          self.work[:,i] = l
          i += 1

        rec = sh[k]
        self.work02[:,j] = rec[ixsum][:5]
        dt0, dt1 = [float(x) for x in rec[ixsum][5:7]]
        fvcount = int( rec[ixsum][7] )
        self.file_summary.append( [dt0, dt1, fvcount] )
        j += 1
    sh.close()

  def loadJson(self,file):
    ee = json.load( open( file, 'r' ) )

    self.info = ee['info']
    dd = ee['data']
    nt = sum( [len(dd[k][5]) for k in dd.keys() ] )
    nf = len( dd.keys() )
    print (nt)
    self.work = numpy.ma.zeros( (self.npct,nt) )
    self.work02 = numpy.ma.zeros( (5,nf) )
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
      os.makedirs( odir )

    tech = {"percentiles":self.input_tech["percentiles"], "summary":["median","max","min","mean absolute max","mean absolute min"]}
  
    if not self.withLevels:
      summary = [0.]*5
      percentiles = [0.]*self.npct
      for k in range(self.npct):
        percentiles[k] = numpy.median( self.work[k,:] )

      summary[0] = numpy.median( self.work02[0,:] )
      summary[1] = numpy.max( self.work02[1,:] )
      summary[2] = numpy.min( self.work02[2,:] )
      summary[3] = numpy.max( self.work02[3,:] )
      summary[4] = numpy.min( self.work02[4,:] )
      tech["with_levels"] = False
    else:
      tech["with_levels"] = True
      tech["levels"] = self.levels
      nl = len(self.levels)
      summary = dict()
      percentiles = dict()
      for l in range(nl):
        lev = self.levels[l]
        summy = [0.]*5
        perc = [0.]*self.npct
##
## set upper limit ... to account for the fact that there may be mssing layers
##
        for k in range(self.npct):
          perc[k] = numpy.median( self.work[k,:self.ntl[lev],l] )

        summy[0] = numpy.median( self.work02[0,:,l] )
        summy[1] = numpy.max( self.work02[1,:,l] )
        summy[2] = numpy.min( self.work02[2,:,l] )
        summy[3] = numpy.max( self.work02[3,:,l] )
        summy[4] = numpy.min( self.work02[4,:,l] )
        summary[lev] = summy
        percentiles[lev] = perc

    self.file_summary_brief = [numpy.mean( [x[0] for x in self.file_summary] ),
                               max( [x[1] for x in self.file_summary] ),
                               sum(  [x[1] for x in self.file_summary] ) ]

    self.this = {'percentiles':percentiles, "summary":summary, "file_summary":self.file_summary_brief}
    oo = open( ofile, 'w' )
    self.info["tech"] = tech
    json.dump( {'info':self.info, 'data':self.this}, oo, indent=4, sort_keys=True )
    oo.close()

## l0: ['ok','shape','median','mx','mn','mamx','mamn','nfv','hasfv','dt0','dt1','units','tid']
## l0: ['median','mx','mn','mamx','mamn','dt0','dt1',"nfv"]


if __name__ == "__main__":
  import sys
  print (sys.argv)
  if sys.argv[1] == "-c":
    ##
    ## consolidates a set of model-experiment-variable json files into a single experiment-variable file
    ##
    c = ConsolidateVar( logid="test2" )
    try:
      c.run( sys.argv[2] )
    except WorkflowException as e:
      print (e.msg)
      print (e.kwargs)
      raise
    except:
      raise

  elif sys.argv[1] == "-d":
    ##
    ## takes shelves files generated by the file scan and creates a consolidated json file for each model-experiment-variable series
    ##
    r = Review( logid="test" )
    idir = sys.argv[2]
    fl = glob.glob( "%s/*.dat" % idir )
    for f in sorted( fl ):
      print ("START: %s" % f )
      r.run( f[:-4] )
  else:
    ifile = sys.argv[1]
    r.run( ifile )
    ##r.run( 'hurs_AS-RCEC_TaiESM1_historical_00-01.json' )
