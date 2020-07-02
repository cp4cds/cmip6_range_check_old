# iso 29119-3 requires/suggests for each test case:
# overview, identifier, objective, priority, traceability, preconditions, inputs, expected results, actual results, test results
#
# these can be grouped within a coverage with:
# overview, identifier, description, priority, traceability.
#
# Implement overview as title, identifier as code word, priority as MUST, SHOULD, traceability as version, date, link to repo.
#
# ISO is assuming string expressions for expected and actual test results. 
#
# pytest gives silence or text to stdout. i.e. the "expected" for pytest test functions is completion without an exception.
# need an iso test within the pytest -- so that the pytest function becomes execute stuff followed by assert conformance -- where conformance is 
## equality for a string, float or int, or TestConformance( expected ).conforms( actual ) for TestConformanceSpec instance. 
#
# 
#
# e.g. expected = 'TCS:regex:^a.*' ... result conforms if it starts with an a.
#
# preconditions:
#
# this is not used ... too cumbersome .. instead use hook in conftest.py
"""Scope01: initial suite of tests ... with specifications aligned to ISO 29119-3 (experimental)"""

import time, operator, warnings
import pytest
import collections
from local_pytest_utils import BaseClassTS, maketest

NT__scope = collections.namedtuple( 'scope', ['overview','identifier','description','priority','traceability'] )
NT__test_case_spec = collections.namedtuple( 'test_case_spec', ['overview', 'identifier', 'objective', 'priority', 'traceability', 'preconditions', 'inputs', 'expected_results'])
NT__test_case_spec = collections.namedtuple( 'test_case_spec', ['ov', 'id', 'obj', 'p', 'tr', 'prec', 'i', 'expected'])
NT__test_case = collections.namedtuple( 'test_case', ['spec', 'actual_results'])

__overview__ = "Testing the local utilities module"
__identifier__ = "scope01"
__description__ = """Test of local utilities module, local_utilities.py, which contains functions and classes used in other modules"""
__priority__ = "MUST"
__traceability__ = "documentation is tbd"

class TC_base_match__UNUSED(NT__test_case_spec):
    def conforms(self,result):
        assert self.re_expected.match(result) != None, 'Result [%s] does not match expected regex [%s]' % (result, self.expected)

class TC_base_equals__UNUSED(NT__test_case_spec):
    def conforms(self,result):
        self.fail_msg = 'Result [%s] does not match expected [%s]' % (result, self.expected)
        self.result = result
        return result == self.expected
    def __call__(self):
        return 'default'
      

##tc05_spec = TC_base_equals( ov='test of TCBuild workflow', id='tc05', obj='test test', p='SHOULD', tr='tbd', prec='None', i='None', expected='hello' )
##def tc05_code() -> tc05_spec:
    ##return 'hello'

##tc05 = TCBuild( tc05_code )
##def test_005() -> tc05:
    ##assert tc05.conforms( tc05() ), tc05.fail_msg

@pytest.mark.incremental
class TestWGI:
  id = 'scope101'
  @maketest
  def test_attr(self) -> dict( ov='Test of WGIPriority object: expected attributes', id='tc101',
                              obj='test WGI attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      import local_utilities
      ar6 = local_utilities.WGIPriority()
      self.__class__.ar6 = ar6
      return all( [hasattr(ar6,a) for a in ['ee','masks','ranges']] )

  @maketest
  def test_tc102(self) -> dict( ov='Test of WGIPriority object: length of ee',
           id='tc102', obj='test workflow with gt operator', p='SHOULD', tr='tbd', prec='None', i='None', expected='gt:150' ):
      return len( self.ar6.ee.keys() )

  @maketest
  def test_tc103(self) -> dict( ov='Test of WGIPriority object: length of ranges',
           id='tc103', obj='test workflow with gt operator', p='SHOULD', tr='tbd', prec='None', i='None', expected='gt:25' ):
      return len( self.ar6.ranges.keys() )

  @maketest
  def test_tc104(self) -> dict( ov='Test of WGIPriority object: length of masks',
           id='tc104', obj='test workflow with gt operator', p='SHOULD', tr='tbd', prec='None', i='None', expected='gt:5' ):
      return len( self.ar6.masks.keys() )

@pytest.mark.incremental
class TestCJ:
  id = 'scope102'
  @maketest
  def test_attr(self) -> dict( ov='Test of CheckJson object: expected attributes', id='tc201',
                              obj='test CheckJson attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      import local_utilities
      cj = local_utilities.CheckJson()
      self.__class__.cj = cj
      return all( [hasattr(cj,a) for a in ['new','pid_lookup']] )

  @maketest
  def test_tc102(self) -> dict( ov='Test of CheckJson object: length of new',
           id='tc102', obj='test workflow with gt operator', p='SHOULD', tr='tbd', prec='None', i='None', expected='gt:10' ):
      return len( self.cj.new['data'].keys() )

##@pytest.mark.parametrize( 'test_function,args,expected,message,line_log_pass,line_log_fail', [(x,x.input_tuple, x.expected,x.message,x.log_pass,x.log_fail) for x in my_tests] )
##def test_001(test_function,args,expected,message,line_log_pass,line_log_fail):
    ##assert  test_function(*args) == expected, message

mask01_expected = 'mask_mismatch: valid points: ref %s; data %s; both %s; ref only %s; data only %s;' % (7,7,6,1,1)

@pytest.mark.incremental
class TestSampler:
  id = 'scope103'
  description = 'check the numpy sampler class from local_utilities module'
  @maketest
  def test_attr(self) -> dict( ov='Test of Sampler object: expected attributes', id='tc101',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      import local_utilities
      samp = local_utilities.Sampler()
      self.__class__.samp = samp
      return all( [hasattr(samp,a) for a in ['nextremes']] )

  @maketest
  def test_extr(self) -> dict( ov='Test of Sampler object: extremes', id='tc102',
                              obj='test Sampler attributes', p='SHOULD', tr='tbd', prec='None', i='None', expected=True ):
      import local_utilities, numpy
      test_data = numpy.zeros( (10,10), 'f' )
      samp = local_utilities.Sampler(extremes=2)
      target = ( ([2,4],[9,7],[-28.,-25.]), ([3,9],[1,3],[24.,12.]) )
      for k in range(2):
          for l in range(2):
              i = target[k][0][l]
              j = target[k][1][l]
              v = target[k][2][l]
              test_data[i,j] = v
      samp.load( test_data )
      rv = samp.get_extremes( )
      max_valid = sorted( rv[1][2] ) == sorted( target[1][2] )
      min_valid = sorted( rv[0][2] ) == sorted( target[0][2] )
      return max_valid and min_valid

  @maketest
  def test_mask(self) -> dict( ov='Test of Sampler object: check_mask', id='tc103',
                              obj='test Sampler check_mask', p='SHOULD', tr='tbd', prec='None', i='None', expected='masks_match' ):
      import local_utilities, numpy
      test_data0 = numpy.ma.zeros( (10,10), 'f' )
      test_data1 = numpy.ma.zeros( (10,10), dtype=int )
      target =  ([2,4],[9,7])
      for l in range(2):
              i = target[0][l]
              j = target[1][l]
              test_data0[i,j] = 999.0
              test_data1[i,j] = 1
      mask0 = numpy.ma.masked_equal( test_data0, 999.0 )
      mask1 = numpy.ma.masked_equal( test_data1, 1 )

      samp = local_utilities.Sampler()
      samp.load( mask1, ref_mask = mask0 )
      return samp.check_mask(  )

  @maketest
  def test_mask01(self) -> dict( ov='Test of Sampler object: check_mask (overlaps)', id='tc104',
          obj='test Sampler check_mask', p='SHOULD', tr='tbd', prec='None', i='None', expected='mask_mismatch: (7,7,6,1,1)' ):
      import local_utilities, numpy
      test_data0 = numpy.ma.array( [1,1,1,2,2,0,0,0,0,0], 'f' )
      test_data1 = numpy.ma.array( [1,1,0,2,2,2,0,0,0,1], 'f' )
      m01 = numpy.ma.masked_equal( test_data0, 1.0 )
      m11 = numpy.ma.masked_equal( test_data1, 1.0 )
      samp = local_utilities.Sampler()
      samp.load( m11, ref_mask = m01 )
      ret = samp.check_mask( )

      return '%s: (%s)' % (ret,','.join([str(x) for x in samp.mask_rep[1:]]) )
