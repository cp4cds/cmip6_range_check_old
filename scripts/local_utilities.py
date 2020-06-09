import logging, time, os, collections, json, inspect
import csv

NT_RangeValue = collections.namedtuple( "range_value", ["value","status"] )
NT_RangeSet = collections.namedtuple( "range_set", ["max","min","ma_max","ma_min"] )
null_range_value = NT_RangeValue( None, "NONE" )

class Dq(object):
  def __init__(self):
    from dreqPy import dreq
    self.dq = dreq.loadDreq()

    self.CMORvar_by_id = dict()
    for i in self.dq.coll["CMORvar"].items:
      self.CMORvar_by_id["%s.%s" % (i.mipTable,i.label) ] = i

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
    ii = csv.reader( open( ifile ), delimiter='\t' )
    try:
      dq = Dq()
    except:
      dq = None

    self.ee = dict()
    self.title = dict()
    self.ranges = dict()
    for l in ii:
      rec = l[2:]
      id, units = rec[:2]
      if dq != None:
        self.title[id] = dq.CMORvar_by_id[id].title
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
    self.pid_lookup = dict()
    self.known_errors = collections.defaultdict( set )

    for fn in ['datasets_with_checksum_errs.txt', 'datasets_with_missing_files.txt', 'master_issues.txt']:
      ii = open( 'data/%s' % fn )
      for l in ii.readlines():
          this = l.strip()
          if this != '':
              self.known_errors[this].add( fn )
      ii.close()
    
    ii = open( "../esgf_fetch/lists/wg1subset-r1-datasets-pids-clean.csv", 'r' )
    for l in ii.readlines()[1:]:
       esgf_id,pid = [x.strip() for x in l.split(',') ]
       self.pid_lookup[esgf_id] = pid

    ii = open( "data/new_limits.csv", "r", encoding = "ISO-8859-1" )
    for l in ii.readlines()[1:]:
      words = l.strip().split('\t')
      if len(words) >3:
        tab,var,directive = [x.strip() for x in words[:3]]
        directive = directive.lower()
        if directive != '':
          id = "%s.%s" % (tab,var)
          if directive[:5] == "valid":
            this = self.new["data"].get( id, {"ranges":{}} )
            if words[3] != '':
              this["ranges"]["max"] = (float( words[3] ), words[6] )
            if words[4] != '':
              this["ranges"]["min"] = (float( words[4] ), words[6] )
            self.new["data"][id] = this
          elif directive[:4] == "mean":
            this = self.new["data"].get( id, {"ranges":{}} )
            if words[3] != '':
              this["ranges"]["ma_max"] = (float( words[3] ), words[6] )
            if words[4] != '':
              this["ranges"]["ma_min"] = (float( words[4] ), words[6] )
            self.new["data"][id] = this
    ii.close()

  def range_merge(self, a, b):
    this = list( a )
    
    for k in range(4):
      if this[k] == null_range_value and b[k] != null_range_value:
        this[k] = b[k]
    return NT_RangeSet( this[0], this[1], this[2], this[3] )

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
    models = sorted( list( data.keys() ) )
    p0 = data[models[0]]["percentiles"]
    isDict = type(p0) == type( {} )

    if len(percentiles) == 13:
  ## "This code assumes 13 percentiles"
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
    else:
      distmsg =  "__na__"
    agg_this = dict()

    metam = dict()
    for m in sorted( list( data.keys() ) ):
        errs = []
        minfo = data[m]["model_info"]
        table,var,inst,model,expt,variant_id,grid_id,version = minfo["drs"]
        ##CMIP6.OMIP.NOAA-GFDL.GFDL-OM4p5B.omip1.r1i1p1f1.Omon.volcello.gn.v20180701
        if expt != "historical":
            print ("need to add some code here ...")
            raise
        esgf_ds_id = "CMIP6.CMIP.%s.%s.%s.%s.%s.%s.%s.%s" % (inst,model,expt,variant_id,table,var,grid_id,version)
        pid = self.pid_lookup.get(esgf_ds_id,'__not_found__')
        contact = ";".join( minfo["contact"] )
        known_error = self.known_errors.get( esgf_ds_id, 'none')
        metam[m] = (esgf_ds_id, pid, contact, known_error)
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
        if varid in wg1.ranges:
          ranges = self.range_merge( ranges, wg1.ranges[varid] )
      else:
        ranges = wg1.ranges[varid]
      rsum = dict()
      for m in sorted( list( data.keys() ) ):
        this = agg_this[m]
        
        range_error_max = (ranges.max != null_range_value) and this[1] > float(ranges.max.value)
        range_error_min = (ranges.min != null_range_value) and this[2] < float(ranges.min.value)
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

          errs = []
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
         oo = open( "test.md", 'w')
         oo.write( "ERROR SUMMARY\n=============\n\n" )
         for m in sorted( list( rsum.keys() ) ):
            if not rsum[m][0]:
                esgf_ds_id, pid, contact, known = metam[m]
                pid_link = "[%s](http://hdl.handle.net/%s)" % (pid,pid[4:])
                oo.write( '%s :: %s\n' % (m,contact) )
                if known != 'none':
                    oo.write( 'Known errors: see %s\n' % known )
                oo.write( '%s\n' % rsum[m][1] )
                oo.write( '%s -- %s\n\n' % (esgf_ds_id,pid_link) )
         oo.close()

    if verbose:
        maxval = max( [x[1] for k,x in agg_this.items()] )
        minval = min( [x[2] for k,x in agg_this.items()] )
        ma_maxval = max( [x[3] for k,x in agg_this.items()] )
        ma_minval = min( [x[4] for k,x in agg_this.items()] )
        print ( "Actual: ",[maxval,minval,ma_maxval,ma_minval] )

    print (var,distmsg,rangemsg)


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
   check_json = CheckJson()
   wg1 = WGIPriority()
   print ( wg1.ranges.keys() )
   k = wg1.ranges.keys().pop()
   print ( k, wg1.ranges[k] )
