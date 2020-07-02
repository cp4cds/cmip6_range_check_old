
from local_pytest_utils import BaseClassTS, Check3, BaseClassCheck
import numpy, netCDF4, pytest, sys, os
from local_utilities import Sampler, VariableSampler, WGIPriority, get_new_ranges

BaseClassCheck.configure( 'cmip6', 'test_file', 'log0001' )

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
  sampler = Sampler(extremes=10, quantiles=[.1,.25,.5,.75,.9] )
  ar6 = WGIPriority()
  ranges_dict = get_new_ranges()

  def test_file(self) -> dict( ov='Test of Sampler object: expected attributes', id='tc101',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      tt = Check3( self.test_file )
      this_file = os.environ['CMIP_FILE']
      if not os.path.isfile( this_file ):
          tt( 'File not found: %s' % this_file )

      try:
          nc = netCDF4.Dataset( this_file )
      except:
          tt( 'Could not open netCDF4 Dataset' )

      try:
          fname = this_file.rpartition('/')[-1]
          vname, table = fname.split('_')[0:2]
          this_var = nc.variables[vname]
      except:
          tt( 'Could not find variable in netCDF4 Dataset' )

      try:
          if hasattr( this_var, '_FillValue' ):
            fill_value = this_var._FillValue
          else:
            fill_value = None
          vs = VariableSampler( this_var[:], self.sampler, fill_value=fill_value )
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
      data_min = min( [x[0] for x in basic] )
      data_max = max( [x[1] for x in basic] )
      data_ma_min = min( [x[2] for x in basic] )
      data_ma_max = max( [x[2] for x in basic] )
      nfv = sum( [x[3] for x in basic] )
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

      Check3( self.test_ranges)( all( [x[-1] for x in res] ) )


class ConcTestCmipFile(TestCmipFile):
    def __init__(self):
        pass

if __name__ == "__main__":
    t = ConcTestCmipFile()
    t.test_file()
