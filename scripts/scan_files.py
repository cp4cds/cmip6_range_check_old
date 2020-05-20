import netCDF4, glob, numpy, shelve, os, traceback, sys, random, time
import collections, traceback
from exceptions_lib import *

__version__ = "0.1.03"

##from config import *

class ScanFile(object):
  def __init__(self,thisfile,sh, mode, vn='tas', checkSpecial=False,maskAll=False,maxnt=10000, with_time=True):
    if maskAll:
      checkSpecial=False
    self.version = "00.01.02"
    self.version_message = "Extended percentiles, adding processing and grid info"
    self.mode = mode
    self.with_time = with_time
    self.sh = sh
    self.checkSpecial = checkSpecial
    self.maskAll = maskAll
    self.maxnt = maxnt
    self.percentiles = [99.9,99.5,99.,95.,90,75.,50.,25.,10.,5.,1.,.5,.1] 
    self.sh["__tech__"] = {  "percentiles":self.percentiles }

    self.shp1 = self.scan1( thisfile, vn )


  def scan1(self,f, vn):
    fname = f.split( '/' )[-1]
    nc = netCDF4.Dataset( f )
    v = nc.variables[vn]
    shp1 = v.shape[:]

    units = v.units
    tid = nc.tracking_id
    hasfv =  '_FillValue' in v.ncattrs()
    hardLowerBnd = None
    specFnd = False

    fill_value = None
    if hasfv:
      fill_value = v._FillValue
    else:
      fvcount = 0

    maskerr = 0
    maskok = False
    maskout = False
    vm = None
    maskrange = None

    tech_info = {"file":(tid,fname),
             "variable":(vn,units,v.dimensions, shp1),
                 "fill":(hasfv, fill_value),
              "masking":(maskout, maskout, maskok,maskrange,maskerr,self.maskAll)  }

    if self.mode in ['shape','shp2']:
      nc.close()
      return shp1

    if self.maskAll:
      if vn != 'sic':
        fm = f.replace( '%s_' % vn, 'sic_' )
        fm = fm.replace( '/%s/' % vn, '/sic/' )
        if not os.path.isfile( fm ):
          print ( 'ERROR.009.00001: mask not found for ',f )
          maskerr = 1
        else:
          print ( 'ERROR.009.00002: mask supported ',f )
          ##ncm = cdms2.open( fm )
          ##tm = ncm.getAxis('time') 
          ##tm1 = tm.getValue()
          ##vmsk = ncm.variables['sic']
          ##if vmsk.shape != v.shape:
            ##print 'ERROR.009.00002: Mask shape mismatch %s -- %s: %s' % (str(v.shape),str(vmsk.shape),f)
            ##maskerr = 2
          ##else:
            ##maskok = True
       
    dt0 = None
    dt1 = None
    nt = 0
    if self.with_time:
      t = nc.variables['time'] 
      if t.shape[0] != v.shape[0]:
        print ( 'Unexpected shapes for variable and time' )
        print ( v.shape,t.shape, f )
        raise BasicFileStructureException

      t_array = t[:]
      if len(t_array) > 1:
        dt = t_array[1:] - t_array[:-1]
        dt0 = numpy.mean( dt )
        dt1 = numpy.max( dt )

      nt =len(t_array)

      if self.mode == 'firstTimeValue':
        nt = min( [12,len(t_array)] )
        v = numpy.array( v[:nt,:,:] )
        if self.maskAll and maskok:
          vmsk = numpy.array( vmsk[:nt,:,:] )
      elif self.mode == 'sampled' and nt > 20:
        isamp = sorted( random.sample( range(nt), 20 ) )
        v = numpy.array( v[isamp,:,:] )
      elif self.mode in ['sampledonepercent','sampledtenpercent','sampledoneperthou'] and nt > 20:
        nsamp = nt//{'sampledonepercent':100, 'sampledtenpercent':10, 'sampledoneperthou':1000}[self.mode]
        isamp = sorted( random.sample( range(nt), nsamp ) )
        if len( isamp ) == 0:
          isamp = [0,]
      
        v = numpy.array( v[isamp,:,:] )
      elif self.maxnt > 0 and self.maxnt < len(t_array):
        nt = self.maxnt
        v = numpy.array( v[:nt,:,:] )

    print( "INFO.001.00020: ", fname, v.shape, nt )
     

    if len( v.shape ) == 3 or (not self.with_time and len(v.shape) == 2):
      tt, am, ap = self.processFeature( v, vm, hasfv, maskout, maskrange, fill_value, hardLowerBnd, specFnd)
      med,mx,mn,mamx,mamn,fvcount = tt

      self.sh[fname] = (True,self.version, time.ctime(), tech_info, (self.checkSpecial,specFnd,maskerr), (med,mx,mn,mamx,mamn,dt0,dt1,fvcount),am, ap)

    elif len( v.shape ) == 4:
      for l in range( v.shape[1]):
        tt, am, ap = self.processFeature( v[:,l,:,:], vm, hasfv, maskout, maskrange, fill_value, hardLowerBnd, specFnd)
        med,mx,mn,mamx,mamn,fvcount = tt

        self.sh["%s:l=%s" % (fname,l)] = (True,self.version, time.ctime(), tech_info, (self.checkSpecial,specFnd,maskerr), (med,mx,mn,mamx,mamn,dt0,dt1,fvcount),am, ap)
        
    nc.close()
    if maskok:
      ncm.close()
    return shp1

  def processFeature( self, v, vm, hasfv,maskout,  maskrange, fill_value, hardLowerBnd, specFnd):
    """Process a series of horizontal fields"""
    am = []
    ap = []
    meds = []
    mxs = []
    mns = []

    if hasfv or hardLowerBnd != None or (self.maskAll and maskok):
      if hasfv:
        if maskout:
          vm = numpy.ma.masked_outside( v, maskrange[0], maskrange[1] )
        else:
          vm = numpy.ma.masked_values( v, fill_value )

        if hardLowerBnd != None:
          vm = numpy.ma.masked_less( vm, hardLowerBnd, copy=False )
        elif self.maskAll and maskok:
          vm = numpy.ma.masked_where( vmsk < 0.1, vm )
      elif hardLowerBnd != None:
          vm = numpy.ma.masked_less( v, hardLowerBnd )
      elif self.maskAll and maskok:
          vm = numpy.ma.masked_where( vmsk < 0.1, v )
        
      if type( v.size ) == type( 1 ):
        fvcount = v.size - vm.count()
      else:
        fvcount = v.size() - vm.count()
 
      if len(v.shape) == 3:
        for k in range( v.shape[0] ):
          am.append( numpy.ma.mean( numpy.ma.abs( vm[k,:] ) ) )
          x = vm[k,:].ravel().compressed()
          if len(x) > 0:
            ap.append( numpy.percentile( x, self.percentiles ) )
          else:
            print ( 'WARN.005.00005: layer contains only missing data: %s' % k )
          meds.append( numpy.ma.median( vm[k,:] ) )
          mxs.append( numpy.ma.max( vm[k,:] ) )
          mns.append( numpy.ma.min( vm[k,:] ) )
      else:
        am.append( numpy.ma.mean( numpy.ma.abs( vm ) ) )
        x = vm.ravel().compressed()
        if len(x) > 0:
            ap.append( numpy.percentile( x, self.percentiles ) )
        else:
            print ( 'WARN.005.00005: layer contains only missing data: %s' % k )
        meds.append( numpy.ma.median( vm ) )
        mxs.append( numpy.ma.max( vm ) )
        mns.append( numpy.ma.min( vm ) )

    else:
      if len(v.shape) == 3:
        for k in range( v.shape[0] ):
          am.append( numpy.mean( numpy.abs( v[k,:] ) ) )
          ap.append( numpy.percentile( v[k,:], self.percentiles ) )
          meds.append( numpy.median( v[k,:] ) )
          mxs.append( numpy.max( v[k,:] ) )
          mns.append( numpy.min( v[k,:] ) )
      else:
          am.append( numpy.mean( numpy.abs( v ) ) )
          ap.append( numpy.percentile( v, self.percentiles ) )
          meds.append( numpy.median( v ) )
          mxs.append( numpy.max( v ) )
          mns.append( numpy.min( v ) )

    if self.checkSpecial:
      m1 = numpy.median( [x[4] for x in ap] )
      m0 = numpy.median( [x[0] for x in ap] )
      m9 = numpy.median( [x[8] for x in ap] )
      if (m0 == m1 or m0 == m9) and not specFnd:
        print ( 'WARN.001.0001: constant area not indicated in metadata: ',f )
        print ( [ numpy.median( [x[i] for x in ap] ) for i in range(9) ] )
    ##counts,bins = numpy.histogram( v, range=(mn,mx) )
    mamx = numpy.max( am )
    mamn = numpy.min( am )
    med = numpy.median( meds )
    mx = max( mns )
    mn = max( mns )
    return  (med,mx,mn,mamx,mamn,fvcount), am, ap


##
## /badc/cmip6/data/CMIP6/CMIP/MOHC/UKESM1-0-LL/historical/r5i1p1f3/day/sfcWindmax/gn/latest
##
class ShrinkByVar(object):
  def __init__(self,mode,log=None):
    self.mode = mode
    self.log = log

  def run(self,inputFile,odir_tag,max_files=0):
    """
    Execute file subsetting
    *inputFile* should contain a list of ESGF "latest" directories for a single data variable.
    """
    ii = open( inputFile ).readlines()
    cc = collections.defaultdict( lambda: collections.defaultdict( lambda: collections.defaultdict(set) ) )
    for l in ii:
      parts = l.strip().split("/")
      inst, source, expt, ense, tab, var, grid = parts[6:13]
      cc[(inst,source)][ense][grid].add( l.strip() )
    nf = 0
    for k in cc.keys():
      this = cc[k]
      k2 = sorted( list( this.keys() ) )[0]
      that = cc[k][k2]
      if "gn" in that.keys():
        sss = that["gn"].pop()
      else:
        k3 = sorted( list( that.keys() ) )[0]
        sss = that[k3].pop()
      inst,source = k
      ense = k2
      odir = odir_tag + var
      if not os.path.isdir (odir):
        os.mkdir( odir )
      files = glob.glob( "%s/*.nc" % sss )
      if max_files > 0 and max_files < len(files):
        files = files[:max_files]
      for f in files:
        fn = f.rpartition("/")[2]
        fnstem = fn.rpartition( "." )[0]
        cmd = "cdo samplegrid,10  %s %s/%s__sel.nc" % (f,odir,fnstem)
        print (cmd)
        os.popen( cmd ).read()

##
## /badc/cmip6/data/CMIP6/CMIP/MOHC/UKESM1-0-LL/historical/r5i1p1f3/day/sfcWindmax/gn/latest
##
class ExecuteByVar(object):
  def __init__(self,mode,log=None):
    self.mode = mode
    self.shelve_template = "sh_ranges/%s/%s/%s_%s_%s_%s_%s"
    self.shelve_dir_template = "sh_ranges/%s/%s"
    self.log = log

  def run(self,inputFile,shelve_tag,max_files=0):
    """
    Execute range extraction for a set of files identified by a listing of directories given in *inputFile*.
    *inputFile* should contain a list of ESGF "latest" directories for a single data variable.
    """
    ii = open( inputFile ).readlines()
    cc = collections.defaultdict( lambda: collections.defaultdict( lambda: collections.defaultdict(set) ) )
    for l in ii:
      fpath = l.strip().split()[8]
      parts = fpath.strip().split("/")
      inst, source, expt, ense, tab, var, grid = parts[6:13]
      cc[(inst,source)][ense][grid].add( fpath.strip() )

    with_time = tab not in ["Ofx", "fx"]
    nf = 0
    for k in cc.keys():
      this = cc[k]
      k2 = sorted( list( this.keys() ) )[0]
      that = cc[k][k2]
      if "gn" in that.keys():
        sss = that["gn"].pop()
      else:
        k3 = sorted( list( that.keys() ) )[0]
        sss = that[k3].pop()
      inst,source = k
      ense = k2
      shelve_dir = self.shelve_dir_template % (tab,var)
      if not os.path.isdir (shelve_dir):
        os.makedirs( shelve_dir )
      shelve_file = self.shelve_template % (tab,var,var,inst,source,expt,shelve_tag)
      sh = shelve.open( shelve_file )
      files = glob.glob( "%s/*.nc" % sss )
      sh["__info__"] = {"title":"Scanning set of data files: %s, %s" % (len(files),[tab,var,inst,source,expt]), "source":"cmip6_range_check.scan_files.ExecuteByVar", "time":time.ctime(), "script_version":__version__}
      print ( sss, len(files) )
      try:
        for data_file in files:
          if self.log != None:
             self.log.info( 'STARTING %s ' % data_file )
          else:
             print ( 'STARTING ',data_file )

          try:
            s = ScanFile(data_file,sh, self.mode, vn=var, checkSpecial=False,maskAll=False,maxnt=10000,with_time=with_time)
          except:
            raise WorkflowException( "wfx.001.0001: Failed to scan file", file=data_file, script="main.py")
          nf += 1
          if max_files > 0 and nf+1 > max_files:
            sh.close()
            return

##
## deal with any workflow exceptions ...
      except WorkflowException as e:
         trace = traceback.format_exc()
         sh["__EXCEPTION__"] = ("WorkflowException",(e.msg,e.kwargs),trace)
         if self.log != None:
           self.log.error( "WorkflowException: %s {%s}\n%s" % (e.msg,e.kwargs,trace) )
         print( "EXCEPTION: WorkflowException: %s, %s" % (e.msg,e.kwargs) )
         print( trace )
      sh.close()

if __name__ == "__main__":
  import sys
  mode = 'all'
  mode = 'sampledonepercent'
  if len(sys.argv) == 4:
    xxx, shelve_tag, input_file = sys.argv[1:]
    ebv = ExecuteByVar(mode)
    ebv.run(input_file,shelve_tag,max_files=0)
  else:
    if len(sys.argv) == 3:
      if sys.argv[1] == "--json":
        import os, json
        shf = sys.argv[2]
        assert os.path.isfile( "%s.dat" % shf ), "File %s.dat not found" % shf
        sh = shelve.open( shf, "r" )
        this = {}
        for k in sh.keys():
          if k[0] == "_":
            this[k] = sh[k]
          else:
            #
            # Need to convert numpy float32 data to python float in order to serialise as json
            #
            Flag,version, time, checks, res0, res1, res2 = sh[k]
            l0 = list(res0)
            l0[1:6] = [float(x) for x in res0[1:6] ]
            l0[8:10] = [float(x) for x in res0[8:10] ]
            l2 = [ [float(x) for x in ll] for ll in res2]
            l1 = [float(x) for x in res1]
            this[k] = (Flag,version, time, checks, l0, l1, l2)
        sh.close()
        oo = open( "%s.json" % shf , 'w' )
        json.dump( {'info':{'title':'From shelve file %s' % shf}, 'data':this}, oo, indent=4, sort_keys=True )
        oo.close()
      else:
        shelve_file, data_file = sys.argv[1:]
        sh = shelve.open( shelve_file )
        sh["__info__"] = {"title":"Scanning single data file: %s" % data_file, "source":"cmip6_range_check.main.ScanFile", "time":time.ctime(), "script_version":__version__}
        vn = data_file.split( "_" )[0].split('/')[-1]
        s = ScanFile(data_file,sh, mode, vn=vn, checkSpecial=False,maskAll=False,maxnt=10000)
