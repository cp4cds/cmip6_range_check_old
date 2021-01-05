import logging
from local_pytest_utils import BaseClassTS, Check3, BaseClassCheck, LogReporter
import numpy, netCDF4, pytest, sys, os, time
from local_utilities import Sampler, VariableSampler, WGIPriority, get_new_ranges, MaskLookUp
from utils import mode_by_table


examples_masks = {('E3SM-1-1-ECA','piControl','Lmon','mrsos','gr'):'../esgf_fetch/data_files_2/sftlf_fx_E3SM-1-1-ECA_piControl_r1i1p1f1_gr.nc'}
mlu = MaskLookUp(verify=True)
# mk = '.'.join( [vname,table,model,expt,grid] )
mlu_bb = dict()
for mk,p in mlu.items():
  vname,table,model,expt,grid = mk.split('.')
  mkb = '.'.join( [vname,table,model,grid] )
  mlu_bb[mkb] = p

LOG_NAME = 'log0001'
CMIP_FILE = os.environ['CMIP_FILE']

fname = CMIP_FILE.rpartition('/')[-1]
log_file_name = fname.replace('.nc','_qc-ranges.log')
vname, table, model, expt, vnt_id, grid = fname.rpartition('.')[0].split('_')[0:6]
SHELVE_FILE_NAME = 'sh/%s' % fname.replace('.nc','_qc-ranges')
BaseClassCheck.configure( 'cmip6', 'test_file', LOG_NAME, reporter=LogReporter(LOG_NAME, log_file=log_file_name) )

##
## setting a list of quantiles ... adpated from code setting "percentiles" with loose meaning of "percentile" 
N_QUANTILES=29
if N_QUANTILES == 13:
      QANTILES = [0.01*x for x in [99.9,99.5,99.,95.,90,75.,50.,25.,10.,5.,1.,.5,.1] ]
elif N_QUANTILES == 29:
      xx = [.001,.002,.005,.01,.02,.05,.1,.2,.5,1.,2.,5.]
      QUANTILES = [0.01*y for y in [100. - x for x in xx] + [90,75.,50.,25.,10.] + xx[::-1]]


def get_vs(data_file, sampler):
          nc = netCDF4.Dataset( data_file )
          fname = data_file.rpartition('/')[-1]
          vname = fname.split('_')[0]
          this_var = nc.variables[vname]
          if hasattr( this_var, '_FillValue' ):
            fill_value = this_var._FillValue
          else:
            fill_value = None
          print ("fill value = %s" % fill_value )
          vs = VariableSampler( this_var[:], sampler, fill_value=fill_value )
          vs.scan()
          vs.dump_shelve('test01',fname,mode='n')
          return (vs, this_var, nc )



class TestCmipFile:
  id = 'scope201'
  description = 'check the numpy sampler class from local_utilities module'
  sample_config = dict(extremes=10, quantiles=QUANTILES )
  ar6 = WGIPriority()
  ranges_dict = get_new_ranges()
  shdir = 'sh'

  def test_file(self) -> dict( ov='Test of Sampler object: expected attributes', id='tc101',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):

      this_file = os.environ['CMIP_FILE'].replace( '//', '/' )
      ##log = logging.getLogger( LOG_NAME )
      ##log.info(  'Starting: %s' % this_file )
      print( 'Starting: %s' % this_file ) 

      tt = Check3( self.test_file )
      self.sampler = Sampler(**self.sample_config)
      if not os.path.isfile( this_file ):
          tt( 'File not found: %s' % this_file )

      try:
          nc = netCDF4.Dataset( this_file )
      except:
          tt( 'Could not open netCDF4 Dataset' )

      pbase = '/badc/cmip6/data/CMIP6/'
      if this_file.find( pbase ) != 0:
          tt( 'DRS not in path: %s' % this_file )
      try:
          era = 'CMIP6'
          activity,inst,model,expt,variant_id,table,var,grid_id,version = this_file[len(pbase):].split('/')[:9]
      except:
          tt( 'Could not extract DRS' )

            ## http://esgdata.gfdl.noaa.gov/thredds/fileServer/gfdl_dataroot4/OMIP/NOAA-GFDL/GFDL-OM4p5B/omip1/r1i1p1f1/Omon/volcello/gn/v20180701/volcello_Omon_GFDL-OM4p5B_omip1_r1i1p1f1_gn_180801-182712.nc

      try:
         tid = nc.tracking_id
         if "contact" in nc.ncattrs():
           contact = nc.contact
         else:
           contact = None
      except:
          tt( 'Could not find required attributes' )

      try:
          fname = this_file.rpartition('/')[-1]
          vname, table, model, expt, vnt_id, grid = fname.rpartition('.')[0].split('_')[0:6]
# rsdt_Amon_MIROC6_historical_r1i1p1f1_gn_195001-201412.nc
          this_var = nc.variables[vname]
      except:
          tt( 'Could not find variable in netCDF4 Dataset' )

      if table not in ["fx","Ofx"]:
        try:
          time_var = nc.variables['time']
          time_units = time_var.units
          dt = time_var[1:] - time_var[:-1]
          dt0 = numpy.mean( dt )
          dt1 = numpy.max( dt )
        except:
          tt( 'Could not find time axis information' )
      else:
        dt0 = None

      try:
         shp = this_var.shape[:]
         units = this_var.units
         dimensions = this_var.dimensions
      except:
         tt( 'Could not find required variable properties' )

      self.__class__.with_mask = False
      try:
          if hasattr( this_var, '_FillValue' ):
            fill_value = this_var._FillValue
          else:
            fill_value = None

          kwargs = dict( fill_value=fill_value )
          tt1 = (model,expt,table,vname,grid)
          mk = '.'.join( [vname,table,model,expt,grid] )
          mkb = '.'.join( [vname,table,model,grid] )

          if table in mode_by_table:
            kwargs['mode'] = mode_by_table[table]

          if mk in mlu:
            kwargs['ref_mask_file'] = mlu[mk]
            self.__class__.with_mask = True
            print ('USING MASK')
          elif mkb in mlu_bb:
            kwargs['ref_mask_file'] = mlu_bb[mkb]
            self.__class__.with_mask = True
            print ('USING MASK [different expt]')
          vs = VariableSampler( this_var[:], self.sampler, **kwargs )

      except:
          tt( 'Could not instantiate scanner' )

      drs = (table,var,inst,model,activity,expt,variant_id,grid_id,version)
      self.file_info = dict( tid=tid, contact=contact, shape=shp, units=units, dimensions=dimensions, fill_value=fill_value, drs=drs )
      if dt0 != None:
        self.file_info['time_units'] = time_units
        self.file_info['time_intervals'] = (dt0,dt1)

      try:
          vs.scan()
      except:
          tt( 'Could not scan variable' )

      try:
          fstem = fname.rpartition( '.' )[0]
          vs.dump_shelve('%s/%s' % (self.shdir,fstem) ,fname,mode='n', file_info=self.file_info)
      except:
          tt( 'Could not dump variable' )

      self.__class__.vs = vs
      vid = '%s.%s' % (table,vname)

      if vid in self.ranges_dict:
          self.__class__.ranges = self.ranges_dict[vid]
          self._gather_basic(vs)
      else:
          self.__class__.ranges = None

      tt( True )

  def _gather_basic(self,vs):
      """Consolidate results of scan to get max, min etc over the a full variable;
      NB ... does not yet deal with levels
      """
      
      ks = sorted( list( self.__class__.vs.sr_dict.keys() ) )
      basic = [ self.__class__.vs.sr_dict[k]['basic'] for k in ks]
      masks_ok = [ self.__class__.vs.sr_dict[k].get('mask_ok',None) for k in ks]
      fraction = [ self.__class__.vs.sr_dict[k].get('fraction',None) for k in ks]
      data_min = min( [x[0] for x in basic] )
      data_max = max( [x[1] for x in basic] )
      data_ma_min = min( [x[2] for x in basic] )
      data_ma_max = max( [x[2] for x in basic] )
      self.__class__.range_comment = 'Data range: %s to %s; mean absolute range %s to %s' % (data_min,data_max,data_ma_min,data_ma_max)
      nfv = sum( [x[3] for x in basic] )
 
      drl = [data_min,data_max,data_ma_min,data_ma_max]
      if all( [type(k)==type(()) for k in ks] ):
          basic0 = [ self.__class__.vs.sr_dict[k]['basic'] for k in ks if k[1] == 0]
          data_min_l0 = min( [x[0] for x in basic0] )
          data_max_l0 = max( [x[1] for x in basic0] )
          drl += [data_min_l0,data_max_l0]
          self.__class__.range_comment = 'Data range: %s to %s (l0: %s to %s); mean absolute range %s to %s' % (data_min,data_max,data_min_l0,data_max_l0,data_ma_min,data_ma_max)

      ## fraction report
      if all( [x == None for x in fraction] ):
        self.__class__.fraction_report = ('no report',None,None,None,None)
      else:
        cmt = set( [f[0] for f in fraction])
        min1 = min( [f[1] for f in fraction] )
        max1 = max( [f[1] for f in fraction] )
        min2 = min( [f[3] for f in fraction] )
        max2 = max( [f[4] for f in fraction] )
        self.__class__.fraction_report = (cmt,min1,max1,min2,max2)

      self.__class__.mask_comment = ''
      if all( [x == None for x in masks_ok] ):
        self.__class__.mask_check = None
        self.__class__.mask_comment = 'No mask report'
      elif all( [x[0] == 'masks_match' for x in masks_ok] ):
        self.__class__.mask_check = True
        s1 = set( [x[1] for x in masks_ok] )
        assert len(s1) == 1, 'Unexpected variation in mask ....'
        n1 = s1.pop()
        self.__class__.mask_comment = 'Mask count = %s' % n1
      else:
        self.__class__.mask_check = False
      print ("MASK COMMENT: ",self.__class__.mask_comment, ' - check: ', self.__class__.mask_check )

      self.__class__.basic = (drl,nfv)

  def test_ranges(self) -> dict( ov='Test of Sampler object: expected ranges', id='tc102',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      if self.__class__.ranges == None:
          return 'No ranges set'

      ranges = self.__class__.ranges
      print ( 'ranges: ', ranges )
      ks = sorted( list( self.__class__.vs.sr_dict.keys() ) )
      basic = [ self.__class__.vs.sr_dict[k]['basic'] for k in ks]

      drl,nfv = self.__class__.basic
      data_min,data_max,data_ma_min,data_ma_max = drl[:4]
      data_min_l0 = data_max_l0 = None
      if len(drl) == 6:
          data_min_l0,data_max_l0 = drl[-2:]

      res = []
      if hasattr( ranges, 'min_l0' ) and ranges.min_l0.status != 'NONE':
          min_valid = float( ranges.min_l0.value )
          res.append( ('min',data_min_l0, min_valid, data_min_l0 >= min_valid ) )

      if hasattr( ranges, 'max_l0' ) and ranges.max_l0.status != 'NONE':
          max_valid = float( ranges.max_l0.value )
          res.append( ('max',data_max_l0, max_valid, data_max_l0 <= max_valid  ) )

      if ranges.min.status != 'NONE':
          min_valid = float( ranges.min.value )
          res.append( ('min',data_min, min_valid, data_min >= min_valid ) ) 

      if ranges.max.status != 'NONE':
          max_valid = float( ranges.max.value )
          res.append( ('max',data_max, max_valid, data_max <= max_valid  ) )

      if ranges.ma_max.status != 'NONE':
          ma_max_valid = float( ranges.ma_max.value )
          res.append( ('ma_max',data_ma_max, ma_max_valid, data_ma_max <= ma_max_valid  ) )

      if ranges.ma_min.status != 'NONE':
          ma_min_valid = float( ranges.min.value )
          res.append( ('ma_min',data_ma_min, ma_min_valid, data_ma_min >= ma_min_valid ) ) 


      Check3( self.test_ranges)( all( [x[-1] for x in res] ), cmt=self.__class__.range_comment )

  def test_masks(self) -> dict( ov='Test of Sampler object: expected mask extent', id='tc103',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected='OK' ):
      if self.__class__.mask_check in [True,None]:
         res = 'OK'
      else:
         res = 'Mask Error'

      Check3( self.test_masks )( res, cmt=self.__class__.mask_comment )

  def test_fraction(self) -> dict( ov='Test of Sampler object: looking at area fraction values', id='tc104',
                              obj='Test whether missing values in data are assigned consistently', p='SHOULD', tr='tbd', prec='None', i='None', expected='OK' ):

      rep = self.__class__.fraction_report
      if rep[0] == 'no report':
         res = 'OK'
         cmt = 'no report'
      elif len( rep[0] ) > 1:
         res = 'ERROR'
         cmt = 'confused report'
      else:
         if rep[1] > rep[4]:
           res = 'OK'
           cmt = 'Min unmasked [%s] > max masked [%s]' % (rep[1],rep[4])
         else:
           res = 'Area Fraction Error'
           cmt = 'Min unmasked [%s] < max masked [%s]' % (rep[1],rep[4])

      Check3( self.test_fraction )( res, cmt=cmt )

  @pytest.mark.wrapup
  def test_wrapup(self) -> dict( ov='Summary of tests', id='tc900',
                                  obj='Provide quick overview', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      Check3( self.test_wrapup )( True, cmt=Check3.review() )

class ConcTestCmipFile(TestCmipFile):
    def __init__(self):
        pass

NO_REPEAT_TEST = True

if __name__ == "__main__":
##
##
## hacked version to avoid parallel read conflict
##
## also easier for debugging
##
##

#vname, table, model, expt, vnt_id, grid = fname.rpartition('.')[0].split('_')[0:6]
    import generic_utils
    group = 3
    log_dir = 'logs_%2.2i' % group
    log_factory = generic_utils.LogFactory(dir=log_dir)

    date_ymd = '%s%2.2i%2.2i' % time.gmtime()[:3] 
    log_name = '%s.%s' % (table,vname)
    log_file = '%s.%s' % (log_name, date_ymd)
    log_wf  = log_factory( '%s.%s' % (table,vname), mode="a", logfile=log_file, warnings=True )
    log_wf.info( 'STARTING test_cmip_file.py WORKFLOW, %s, %s' % ( time.ctime(), fname)  )

    t = ConcTestCmipFile()
    fstem = fname.rpartition( '.' )[0]
    od1 = 'out_%2.2i/%s.%s' % (group,table,vname)
    od2 = 'sh_%2.2i/%s.%s' % (group,table,vname)
    if not os.path.isdir( od1 ):
      os.mkdir(od1)
    if not os.path.isdir( od2 ):
      os.mkdir(od2)
    t.shdir = od2
    of1 = '%s/%s' % (od1,fstem)
    if os.path.isfile( of1 ) and NO_REPEAT_TEST: 
      print( 'Test for %s already complete' % fstem )
    else:
      oo1 = open( of1, 'w' )
      oo1.write( '#FILE: %s\n' % CMIP_FILE )
      oo1.write( '#DATE: %s\n' % time.ctime() )
      oo1.write( '#SOURCE: %s\n' % 'test_cmip_file.py: as script' )
      cmt = None
      wcmt = ''
    ##RAISE_FIRST = True
      RAISE_FIRST = False
      for m in [t.test_file, t.test_ranges, t.test_masks, t.test_fraction, t.test_wrapup]:
         ret = m.__annotations__['return']
         try:
           m()
           res = 'OK'
         except:
           res='FAIL'
           if RAISE_FIRST:
              oo1.write( '%s: %s: %s \n' % (res,ret['id'],ret['ov'] ) )
              oo1.write( 'ABANDON TESTS\n' )
              oo1.close()
              raise
         res2 = None
         if 'tc' in m.__annotations__:
           tc = m.__annotations__['tc']
           if hasattr( tc, 'result' ):
             res2 = tc.result
         if res2 == None:
           msg = '--NO RESULT FOUND--'
         else:
           try:
             msg,cmt = res2
           except:
             msg = str(res2 )
       
         if cmt != None:
           wcmt = ' | %s' % cmt
         print ( '%s: %s: %s -- %s%s' % (res,ret['id'],ret['ov'], msg, wcmt ) )
         oo1.write( '%s: %s: %s -- %s%s\n' % (res,ret['id'],ret['ov'], msg, wcmt ) )
         res2 = None
      oo1.close()
    ##t.test_file()
