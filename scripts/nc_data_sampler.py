import netCDF4, numpy, shelve, os, random, time
import traceback
from exceptions_lib import *

__version__ = "0.1.03"

##from config import *

class NcDataSampler(object):
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


  def scan1(self,f, vn, mask_file=None, mask_var=None):
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

    mask_info = None
    if mask_file != None:
      if not os.path.isfile( mask_file ):
        print ( 'ERROR.009.00001: mask not found for ',f )
        maskerr = 1
      else:
        nc = netCDF4.Dataset( mask_file )
        vmsk = nc.variables[mask_var]
        shpm = vmsk.shape[:]
        if vmsk.shape != v.shape:
            print ( 'ERROR.009.00002: Mask shape mismatch %s -- %s: %s' % (str(v.shape),str(vmsk.shape),f) )
            maskerr = 2
        else:
            maskok = True
        mask_info = (mask_var,vmsk.units,vmsk.dimensions, shpm)

    tech_info = {"file":(tid,fname),
             "variable":(vn,units,v.dimensions, shp1),
                 "fill":(hasfv, fill_value),
              "mask_info":maskinfo,   
              "masking":(maskout, maskout, maskok,maskrange,maskerr,self.maskAll)  }

    if self.mode in ['shape','shp2']:
      nc.close()
      return shp1

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
      tt, am, ap = self.processFeature( v, vmsk, hasfv, maskout, maskrange, fill_value, hardLowerBnd, specFnd)
      med,mx,mn,mamx,mamn,fvcount = tt

      self.sh[fname] = (True,self.version, time.ctime(), tech_info, (self.checkSpecial,specFnd,maskerr), (med,mx,mn,mamx,mamn,dt0,dt1,fvcount),am, ap)

    elif len( v.shape ) == 4:
      for l in range( v.shape[1]):
        tt, am, ap = self.processFeature( v[:,l,:,:], vmsk, hasfv, maskout, maskrange, fill_value, hardLowerBnd, specFnd)
        med,mx,mn,mamx,mamn,fvcount = tt

        self.sh["%s:l=%s" % (fname,l)] = (True,self.version, time.ctime(), tech_info, (self.checkSpecial,specFnd,maskerr), (med,mx,mn,mamx,mamn,dt0,dt1,fvcount),am, ap)
        
    nc.close()
    if maskok:
      ncm.close()
    return shp1

  def processFeature( self, v, vmsk, hasfv,maskout,  maskrange, fill_value, hardLowerBnd, specFnd):
    """Process a series of horizontal fields"""
    am = []
    ap = []
    meds = []
    mxs = []
    mns = []

    if hasfv or hardLowerBnd != None or (self.maskAll and maskok):
      if hasfv:
        if maskout:
          vmsk = numpy.ma.masked_outside( v, maskrange[0], maskrange[1] )
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
    mx = max( mxs )
    mn = max( mns )
    return  (med,mx,mn,mamx,mamn,fvcount), am, ap


##
## /badc/cmip6/data/CMIP6/CMIP/MOHC/UKESM1-0-LL/historical/r5i1p1f3/day/sfcWindmax/gn/latest
##

if __name__ == "__main__":
  import sys, argparse
  parser = argparse.ArgumentParser()
  parser.add_argument( '-v', '--version', action='version', version=__version__)
  parser.add_argument( 'shelve_file', type=str, help='file name (minus suffix) of shelve database')
  parser.add_argument( 'data_file', type=str, help='name of fileto be sampled' )
  this = parser.parse_args( sys.argv[1:] )
  mode = 'all'
  mode = 'sampledonepercent'
  sh = shelve.open( this.shelve_file )
  sh["__info__"] = {"title":"Scanning single data file: %s" % data_file, "source":"cmip6_range_check.main.ScanFile", "time":time.ctime(), "script_version":__version__}
  vn = this.data_file.split( "_" )[0].split('/')[-1]
  s = ScanFile(this.data_file,sh, mode, vn=vn, checkSpecial=False,maskAll=False,maxnt=10000)
