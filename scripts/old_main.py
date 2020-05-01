import netCDF4, glob, numpy, shelve, os, traceback, sys, random, time
import collections, traceback
from exceptions_lib import *
import scan_files 

__version__ = "0.2.0"

##from config import *

<<<<<<< HEAD
class BasicFileStructureException(Exception):
    pass

base = '/badc/cmip5/data/cmip5/output1/'
##base = '/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/historical/mon/atmos/Amon/r1i1p1/latest/tasmax/'

class ScanFile(object):
  def __init__(self,thisfile,sh, mode, vn='tas', checkSpecial=False,maskAll=False,maxnt=10000):
    if maskAll:
      checkSpecial=False
    self.version = "00.01.00b1"
    self.mode = mode
    self.sh = sh
    self.checkSpecial = checkSpecial
    self.maskAll = maskAll
    self.maxnt = maxnt

    self.shp1 = self.scan1( thisfile, vn )


  def scan1(self,f, vn):
    print ( 'STARTING ',f )
    fname = f.split( '/' )[-1]
    nc = netCDF4.Dataset( f )
    v = nc.variables[vn]
    shp1 = v.shape[:]

    if self.mode in ['shape','shp2']:
      nc.close()
      return shp1

    maskerr = 0
    maskok = False
    mskout = False
    vm = None
    mskrange = None
    fill_value = None
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
       
    t = nc.variables['time'] 
    tid = nc.tracking_id
    if t.shape[0] != v.shape[0]:
      print ( 'Unexpected shapes for variable and time' )
      print ( v.shape,t.shape, f )
      raise BasicFileStructureException

    t_array = t[:]
    if len(t_array) > 1:
      dt = t_array[1:] - t_array[:-1]
      dt0 = numpy.mean( dt )
      dt1 = numpy.max( dt )
    else:
      dt0 = None
      dt1 = None

    hasfv =  '_FillValue' in v.ncattrs()
    hardLowerBnd = None
    specFnd = False
    units = v.units
    if hasfv:
      fill_value = v._FillValue
    else:
      fvcount = 0

    nt =len(t_array)
    if self.mode == 'firstTimeValue':
      nt = min( [12,len(t_array)] )
      v = numpy.array( v[:nt,:,:] )
      if self.maskAll and maskok:
        vmsk = numpy.array( vmsk[:nt,:,:] )
    elif self.mode == 'sampled' and nt > 20:
      isamp = sorted( random.sample( range(nt), 20 ) )
      v = numpy.array( v[isamp,:,:] )
    elif self.mode == 'sampledonepercent' and nt > 20:
      nsamp = nt//100
      isamp = sorted( random.sample( range(nt), nsamp ) )
      
      v = numpy.array( v[isamp,:,:] )
    elif self.maxnt > 0 and self.maxnt < len(t_array):
      nt = self.maxnt
      v = numpy.array( v[:nt,:,:] )
     

    if len( v.shape ) == 3:
      tt, am, ap = self.processFeature( v, vm, hasfv, mskout, mskrange, fill_value, hardLowerBnd, specFnd)
      med,mx,mn,mamx,mamn,fvcount = tt

      self.sh[fname] = (True,self.version, time.ctime(), (self.checkSpecial,specFnd,maskerr), (v.shape,med,mx,mn,mamx,mamn,fvcount,hasfv,dt0,dt1,units,tid),am, ap)
    elif len( v.shape ) == 4:
      for l in range( v.shape[1]):
        tt, am, ap = self.processFeature( v[:,l,:,:], vm, hasfv, mskout, mskrange, fill_value, hardLowerBnd, specFnd)
        med,mx,mn,mamx,mamn,fvcount = tt

        self.sh["%s:l=%s" % (fname,l)] = (True,self.version, time.ctime(), (self.checkSpecial,specFnd,maskerr), (v.shape,med,mx,mn,mamx,mamn,fvcount,hasfv,dt0,dt1,units,tid),am, ap)
        
    nc.close()
    if maskok:
      ncm.close()
    return shp1

  def processFeature( self, v, vm, hasfv,mskout,  mskrange, fill_value, hardLowerBnd, specFnd):
    """Process a series of horizontal fields"""

    if hasfv or hardLowerBnd != None or (self.maskAll and maskok):
      if hasfv:
        if mskout:
          vm = numpy.ma.masked_outside( v, mskrange[0], mskrange[1] )
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
      med = numpy.ma.median( vm )
      mx = numpy.ma.max( vm )
      mn = numpy.ma.min( vm )
      am = []
      ap = []
 
      for k in range( v.shape[0] ):
        am.append( numpy.ma.mean( numpy.ma.abs( vm[k,:] ) ) )
        x = vm[k,:].ravel().compressed()
        if len(x) > 0:
          ap.append( numpy.percentile( x, [99.9,99.,95.,75.,50.,25.,5.,1.,.1] ) )
        else:
          print ( 'WARN.005.00005: layer contains only missing data: %s' % k )

    else:
      med = numpy.median( v )
      mx = numpy.max( v )
      mn = numpy.min( v )
      am = []
      ap = []
      for k in range( v.shape[0] ):
        am.append( numpy.mean( numpy.abs( v[k,:] ) ) )
        ap.append( numpy.percentile( v[k,:], [99.9,99.,95.,75.,50.,25.,5.,1.,.1] ) )

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
    return  (med,mx,mn,mamx,mamn,fvcount), am, ap



##
## /badc/cmip6/data/CMIP6/CMIP/MOHC/UKESM1-0-LL/historical/r5i1p1f3/day/sfcWindmax/gn/latest
##
class ExecuteByVar(object):
  def __init__(self,mode):
    self.mode = mode
    self.shelve_template = "sh_ranges/%s/%s_%s_%s_%s_%s"
    self.shelve_dir_template = "sh_ranges/%s"
  def run(self,inputFile,shelve_tag,max_files=0):
    """
    Execute range extraction for a set of files identified by a listing of directories given in *inputFile*.
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
      shelve_dir = self.shelve_dir_template % var
      if not os.path.isdir (shelve_dir):
        os.mkdir( shelve_dir )
      shelve_file = self.shelve_template % (var,var,inst,source,expt,shelve_tag)
      sh = shelve.open( shelve_file )
      files = glob.glob( "%s/*.nc" % sss )
      print ( sss, len(files) )
      try:
        for data_file in files:
          try:
            s = ScanFile(data_file,sh, self.mode, vn=var, checkSpecial=False,maskAll=False,maxnt=10000)
          except:
            raise WorkflowException( "wfx.001.0001: Failed to scan file", file=data_file, script="main.py")
          nf += 1
          if max_files > 0 and nf+1 > max_files:
            sh.close()
            return

##
## deal with any workflow exceptions ...
      except WorkflowExcetpion as e:
         trace = traceback.format_exc()
         sh["__EXCEPTION__"] = ("WorkflowException",(e.msg,e.kwargs),trace)
         print( "EXCEPTION: WorkflowException: %s, %s" % (e.msg,e.kwargs) )
      sh.close()
=======
>>>>>>> 29675bc1466bbe5def34cbbd87925babefd27f07

if __name__ == "__main__":
  import sys
  mode = 'all'
  mode = 'sampledonepercent'
  if sys.argv[1] == "--exptvar":
    assert len(sys.argv) == 4
    shelve_tag, input_file = sys.argv[2:]
    ebv = scan_files.ExecuteByVar(mode)
    ebv.run(input_file,shelve_tag,max_files=0)
  elif sys.argv[1] == "--single":
    assert len(sys.argv) == 4
    shelve_file, data_file = sys.argv[2:]
    sh = shelve.open( shelve_file )
    sh["__info__"] = {"title":"Scanning single data file: %s" % data_file, "source":"cmip6_range_check.main.ScanFile", "time":time.ctime(), "script_version":__version__}
    vn = data_file.split( "_" )[0].split('/')[-1]
    s = scan_files.ScanFile(data_file,sh, mode, vn=vn, checkSpecial=False,maskAll=False,maxnt=10000)
