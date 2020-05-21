import logging, time, os, collections, json, inspect

NT_RangeValue = collections.namedtuple( "range_value", ["value","status"] )
NT_RangeSet = collections.namedtuple( "range_set", ["max","min","ma_max","ma_min"] )
null_range_value = NT_RangeValue( None, "NONE" )

def stn(x,nd=2):
  if type(x) in [type(''),type( u'')]:
    return x

  ax = abs(x)
  if ax > 1. and ax < 1000.:
    vv = '%7.1f' % x
  elif ax > 0.01 and ax < 1.0001:
    vv = '%7.4f' % x
  else:
    vv = '%9.2e' % x
    if len(vv) > 7 and vv[-8:] == '0.00e+00':
      vv = '0.0'
  return vv

class WGIPriority(object):
  def __init__(self,ifile="AR6_priority_variables_02.csv" ):
    ii = open( ifile ).readlines()
    self.ee = dict()
    self.ranges = dict()
    for l in ii:
      rec = l.split( "\t" )
      id, units = rec[:2]
      vt = rec[2:10]
      if not all( [vt[i] == "-" for i in [1,3,5,7]]):
        xx = []
        for i in [0,2,4,6]:
          if vt[i+1] not in ["-",""]:
            xx.append( NT_RangeValue(vt[i],vt[i+1]) )
          else:
            xx.append( null_range_value )
        self.ranges[id] = NT_RangeSet( xx[0], xx[1], xx[2], xx[3] )

      self.ee[id] = units

class CheckJson(object):
  def __init__(self):
    self.new = json.load( open( "data/new_limits.json", "r" ) )
    self.new_modified = set()

  def get_range(self,varid):
    xx = []
    this = self.new["data"][varid]["ranges"]
    for k in ["max","min","ma_max","ma_min"]:
      if k in this:
        xx.append( NT_RangeValue( this[k][0], this[k][1] ) )
      else:
        xx.append( null_range_value )
    return NT_RangeSet( xx[0], xx[1], xx[2], xx[3] )

  def set_range(self,varid, max=None, min=None, ma_max=None, ma_min=None ):
    """set a new range value or values in local instance"""
    self.sig = inspect.signature( self.set_range )
    ee = dict()
    args = list( self.sig.parameters.keys() )
    for k in args[1:]:
      val = locals()[k]
      if val != None:
        if type(val) == type( () ):
          ee[k] = val
        elif type(val) in [type( 1. ),type( 1 )]:
          ee[k] = (val,"provisional")
        else:
          print ("value for arg %s not recognised" % k )
          raise

    if varid in self.new["data"]:
      this = self.new["data"][varid]
      this["ranges"]
      for k in prev:
        if k not in ee:
          ee[k] = prev[k]
      this["ranges"] = ee
      hist = this["history"]
      hist.append( "Record updates %s" % time.ctime() )
      this["history"] = this
    else:
      this = {"ranges":ee, "history":"Record created %s" % time.ctime() }

    self.new["data"][varid] = this
    if len( ee.keys() ) > 0:
      self.new_modified.add( varid )
     
   
  def __call__(self, table,ipath=None,var=None,verbose=True):
    if ipath == None:
      assert var !=None, "check_json: either ipath or var must be set"
      ipath = "json_ranges/%s/%s_historical_consol-var.json" % (table,var)

    assert os.path.isfile( ipath ), "check_json: file %s not found" % ipath

    ifile = ipath.rpartition("/")[-1]
    var = ifile.split("_")[0]
    wg1 =  WGIPriority()
    varid = "%s.%s" % (table,var)
    if verbose: print( "check_json",table, ipath, varid )
    ee = json.load( open( ipath, "r" ) )
    data = ee["data"]
    percentiles = ee["info"]["tech"]["percentiles"]
    assert len(percentiles) == 13,  "This code assumes 13 percentiles"
    models = sorted( list( data.keys() ) )
    p0 = data[models[0]]["percentiles"]
    isDict = type(p0) == type( {} )
    if isDict:
      pmx = [max( [data[m]["percentiles"]["0"][j] for m in models] ) for j in range(len(percentiles)) ]
      pmn = [min( [data[m]["percentiles"]["0"][j] for m in models] ) for j in range(len(percentiles)) ]
    else:
      pmx = [max( [data[m]["percentiles"][j] for m in models] ) for j in range(len(percentiles)) ]
      pmn = [min( [data[m]["percentiles"][j] for m in models] ) for j in range(len(percentiles)) ]
    pctcomp = [pmx[i+1] < pmn[i] for i in range(4,8) ] 
    if verbose:
      print ( pctcomp, pmx[5:9], pmn[4:8] )
      print ("pmx", pmx)
      print ("pmn", pmn)
    clean = all( pctcomp )
    if clean:
      distmsg = "COMPACT DISTRIBUTION"
    else:
      distmsg =  "overlapping distributions"
    if verbose:
      print (distmsg)
    agg_this = dict()

    for m in sorted( list( data.keys() ) ):
        errs = []
        if isDict:
          this = data[m]["summary"]["0"]
        else:
          this = data[m]["summary"]
        agg_this[m] = this

    if varid not in wg1.ranges and varid not in self.new["data"]:
      if verbose:
        print ( "No range information for %s" % varid )
      rangemsg = "No Range Set"
    else:
      if varid in self.new["data"]:
        ranges = self.get_range( varid )
      else:
        ranges = wg1.ranges[varid]
      rsum = dict()
      for m in sorted( list( data.keys() ) ):
        errs = []
        this = agg_this[m]
        
        range_error_max = this[0] > float(ranges.max.value)
        range_error_min = this[2] < float(ranges.min.value)
        try:
          range_error_ma_max = (ranges.ma_max != null_range_value) and this[3] > float(ranges.ma_max.value)
        except:
          print (ranges.ma_max)
          raise
        try:
          range_error_ma_min = (ranges.ma_min != null_range_value) and this[4] < float(ranges.ma_min.value)
        except:
          print (ranges.ma_min)
          raise

        if not any( [range_error_max,range_error_min, range_error_ma_max, range_error_ma_min] ):
           res = (True,"OK")
        else:
          if verbose:
            print( m, [range_error_max,range_error_min, range_error_ma_max, range_error_ma_min] )
          for k in range(4):
            if [range_error_max,range_error_min, range_error_ma_max, range_error_ma_min][k]:
              elab = ["Max","Min","MA Max","MA Min"][k]
              ##targ = [float(ranges.max.value), float(ranges.min.value), float(ranges.ma_max.value), float(ranges.ma_min.value)][k]
              targ = [ranges.max.value, ranges.min.value, ranges.ma_max.value, ranges.ma_min.value][k]
              msg = "%s: %s -- %s" % (elab, this[k+1], targ)
              errs.append( msg)
          res = (False,"; ".join( errs ))
              
        if verbose:
          print ("%s:: %s/%s" % (m,res,errs) )
        rsum[m] = res

      bad = [k for k,v in rsum.items() if not v[0]]
      if verbose:
        for k in bad:
           print ("ERROR: %s:: %s" % (k,rsum[k][1]) )
        print ("Targets:", [ranges.max.value, ranges.min.value, ranges.ma_max.value, ranges.ma_min.value] )
      if len( bad) == 0:
         rangemsg = "All models in range"
      else:
         rangemsg = "Range errors: %s [of %s]" % (len(bad),len(rsum.keys()))
    if verbose:
        maxval = max( [x[1] for k,x in agg_this.items()] )
        minval = min( [x[2] for k,x in agg_this.items()] )
        ma_maxval = max( [x[3] for k,x in agg_this.items()] )
        ma_minval = min( [x[4] for k,x in agg_this.items()] )
        print ( "Actual: ",[maxval,minval,ma_maxval,ma_minval] )
    print (var,distmsg,rangemsg)

check_json = CheckJson()

class LogFactory(object):
  def __init__(self, dir='.'):
    """
    LogFactory instantiates to a callable which can generate logs from the logging module.
    """
    self.tstring2 = '%4.4i%2.2i%2.2i' % time.gmtime()[0:3]
    self.logdir = dir
    self.logs = dict()
    if not os.path.isdir( dir ):
      os.mkdir(dir )
      print ( 'Log: making a new directory fr log files: %s' % dir )

  def __call__(self,name,dir=None,logfile=None,mode="a", warnings=False):
    if dir == None:
      dir = self.logdir
    if logfile != None:
      self.log_file = '%s/%s' % (dir,logfile)
    else:
      self.log_file = '%s/log_%s_%s.txt' % (dir,name,self.tstring2)

    log = logging.getLogger(name)
    fHdlr = logging.FileHandler(self.log_file,mode=mode)
    fileFormatter = logging.Formatter('%(message)s')
    fHdlr.setFormatter(fileFormatter)
    log.addHandler(fHdlr)
    log.setLevel(logging.INFO)
    self.logs[name] = log
    if warnings:
      np_log = logging.getLogger("py.warnings")
      np_log.setLevel(logging.WARN)
      np_log.addHandler(fHdlr)
      self.logs["py.warnings"] = np_log
      if hasattr( logging, "captureWarnings" ):
        logging.captureWarnings(True)
    return log

  


if __name__ == "__main__":
   wg1 = WGIPriority()
   print ( wg1.ranges.keys() )
   k = wg1.ranges.keys().pop()
   print ( k, wg1.ranges[k] )
