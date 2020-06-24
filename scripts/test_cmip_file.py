
from local_pytest_utils import BaseClassTS
import numpy, netCDF4, pytest, sys, os
from local_utilities import maketest, TCBuild, Sampler, VariableSampler, WGIPriority

def get_vs(data_file, sampler):
          nc = netCDF4.Dataset( data_file )
          vname = data_file.rpartition('/')[-1].split('_')[0]
          this_var = nc.variables[vname]
          if hasattr( this_var, '_FillValue' ):
            fill_value = this_var._FillValue
          else:
            fill_value = None
          print ("fill value = %s" % fill_value )
          vs = VariableSampler( this_var[:], sampler, fill_value=fill_value )
          vs.scan()
          return (vs, this_var, nc )

@pytest.mark.incremental
class TestCmipFile:
  id = 'scope201'
  description = 'check the numpy sampler class from local_utilities module'
  sampler = Sampler(extremes=10, quantiles=[.1,.25,.5,.75,.9] )
  ar6 = WGIPriority()
  @maketest
  def test_file(self) -> dict( ov='Test of Sampler object: expected attributes', id='tc101',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      this_file = os.environ['CMIP_FILE']
      if not os.path.isfile( this_file ):
          return 'File not found: %s' % this_file

      try:
          nc = netCDF4.Dataset( this_file )
      except:
          return 'Could not open netCDF4 Dataset'

      try:
          vname, table = this_file.rpartition('/')[-1].split('_')[0:2]
          this_var = nc.variables[vname]
      except:
          return 'Could not find variable in netCDF4 Dataset'

      try:
          if hasattr( this_var, '_FillValue' ):
            fill_value = this_var._FillValue
          else:
            fill_value = None
          vs = VariableSampler( this_var[:], self.sampler, fill_value=fill_value )
      except:
          return 'Could not instantiate scanner'

      try:
          vs.scan()
      except:
          return 'Could not scan variable'

      vid = '%s.%s' % (table,vname)
      if vid in self.ar6.ranges:
          self.__class__.ranges = self.ar6.ranges[vid]
      else:
          self.__class__.ranges = None

      self.__class__.vs = vs
      return True

  @maketest
  def test_ranges(self) -> dict( ov='Test of Sampler object: expected ranges', id='tc102',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      if self.__class__.ranges == None:
          return 'No ranges set'

      ranges = self.__class__.ranges
      ks = sorted( list( self.__class__.vs.sr_dict.keys() ) )
      basic = [ self.__class__.vs.sr_dict[k].basic for k in ks]

      res = []
      if ranges.min.status != 'NONE':
          data_min = min( [x[0] for x in basic] )
          res.append( ('min',data_min, float( ranges.min.value ), data_min >= float( ranges.min.value ) ) )

      if ranges.max.status != 'NONE':
          data_max = max( [x[0] for x in basic] )
          res.append( ('max',data_max, float( ranges.max.value ), data_max <= float( ranges.max.value ) ) )

      return all( [x[-1] for x in res] )


class ConcTestCmipFile(TestCmipFile):
    def __init__(self):
        pass

if __name__ == "__main__":
    t = ConcTestCmipFile()
    t.test_file()
