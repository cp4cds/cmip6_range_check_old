
import logging
from local_pytest_utils import BaseClassTS, Check3, BaseClassCheck
import numpy, netCDF4, pytest, sys, os
from local_utilities import Sampler, VariableSampler, WGIPriority, get_new_ranges, MaskLookUp

LOG_NAME = 'log0001'

BaseClassCheck.configure( 'cmip6', 'test_file', LOG_NAME )

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

examples_masks = {('E3SM-1-1-ECA','piControl','Lmon','mrsos','gr'):'../esgf_fetch/data_files_2/sftlf_fx_E3SM-1-1-ECA_piControl_r1i1p1f1_gr.nc'}
mlu = MaskLookUp(verify=True)
# mk = '.'.join( [vname,table,model,expt,grid] )
mlu_bb = dict()
for mk,p in mlu.items():
  vname,table,model,expt,grid = mk.split('.')
  mkb = '.'.join( [vname,table,model,grid] )
  mlu_bb[mkb] = p

class TestCmipFile:
  id = 'scope201'
  description = 'check the numpy sampler class from local_utilities module'
  sample_config = dict(extremes=10, quantiles=[.1,.25,.5,.75,.9] )
  ar6 = WGIPriority()
  ranges_dict = get_new_ranges()

  def test_file(self) -> dict( ov='Test of Sampler object: expected attributes', id='tc101',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):

      this_file = os.environ['CMIP_FILE']
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

      try:
          fname = this_file.rpartition('/')[-1]
          vname, table, model, expt, vnt_id, grid = fname.rpartition('.')[0].split('_')[0:6]
# rsdt_Amon_MIROC6_historical_r1i1p1f1_gn_195001-201412.nc
          this_var = nc.variables[vname]
      except:
          tt( 'Could not find variable in netCDF4 Dataset' )

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

      try:
          vs.scan()
      except:
          tt( 'Could not scan variable' )

      try:
          vs.dump_shelve('test02',fname,mode='n')
      except:
          tt( 'could not dump variable' )

      self.__class__.vs = vs
      vid = '%s.%s' % (table,vname)

      if vid in self.ranges_dict:
          self.__class__.ranges = self.ranges_dict[vid]
          self._gather_basic(vs)
      else:
          self.__class__.ranges = None

      tt( True )

  def _gather_basic(self,vs):
      """Concolidate results of scan to get max, min etc over the a full variable;
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

      self.__class__.basic = (data_min,data_max,data_ma_min,data_ma_max,nfv)

  def test_ranges(self) -> dict( ov='Test of Sampler object: expected ranges', id='tc102',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      if self.__class__.ranges == None:
          return 'No ranges set'

      ranges = self.__class__.ranges
      print ( 'ranges: ', ranges )
      ks = sorted( list( self.__class__.vs.sr_dict.keys() ) )
      basic = [ self.__class__.vs.sr_dict[k]['basic'] for k in ks]

      data_min,data_max,data_ma_min,data_ma_max,nfv = self.__class__.basic
      res = []
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

  def test_masks(self) -> dict( ov='Test of Sampler object: expected mask extend', id='tc103',
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

class ConcTestCmipFile(TestCmipFile):
    def __init__(self):
        pass

if __name__ == "__main__":

    t = ConcTestCmipFile()
    t.test_file()
