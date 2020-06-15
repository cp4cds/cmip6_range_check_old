# iso 29119-3 requires/suggests for each test case:
# overview, identifier, objective, priority, traceability, preconditions, inputs, expected results, actual results, test results
#
# these can be grouped within a coverage with:
# overview, identifier, description, priority, traceability.
#
# Implement overview as title, identifier as code word, priority as MUST, SHOULD, traceability as version, date, link to repo.
#
# preconditions:
#
#
# this is not used ... too cumbersome .. instead use hook in conftest.py
"""Scope01: initial suite of tests ... with specifications aligned to ISO 29119-3 (experimental)"""

import time
import pytest

__overview__ = "Testing the local utilities module"
__identifier__ = "scope01"
__description__ = """Test of local utilities module, local_utilities.py, which contains functions and classes used in other modules"""
__priority__ = "MUST"
__traceability__ = "documentation is tbd"

class TC01(object):
  version = '0.1'
  identifier = 'Test01'
  overview = 'Test that the local utilities module can load'
  prority = 'MUST'
  input_tuple = ()
  input_dict = {}
  expected = 'local_utilities'
  def __init__(self):
    self.objective = 'Testing my_test_function with arguments %s' % str(self.input_tuple)
    self.traceability = (__name__,self.identifier,self.version,time.ctime())
    self.preconditions = {}
    self.message = 'failed to load module'
    self.log_pass = '  OK: %s [%s] ' % (self.identifier,self.overview)
    self.log_fail = 'FAIL: %s [%s] ' % (self.identifier,self.overview)

  def __call__(self):
    try:
      import local_utilities
      return local_utilities.__name__
    except:
      return 'Failed to import'

class TC02(object):
  version = '0.1'
  identifier = 'Test02'
  overview = 'Test that the local utilities classes can instantiate'
  prority = 'MUST'
  input_tuple = ()
  input_dict = {}
  expected = "<class 'local_utilities.WGIPriority'>"
  def __init__(self):
    self.objective = 'Testing my_test_function with arguments %s' % str(self.input_tuple)
    self.traceability = (__name__,self.identifier,self.version,time.ctime())
    self.preconditions = {}
    self.message = 'failed to instantiate class'
    self.log_pass = '  OK: %s [%s] ' % (self.identifier,self.overview)
    self.log_fail = 'FAIL: %s [%s] ' % (self.identifier,self.overview)

  def __call__(self):
    import local_utilities
    ar6 = local_utilities.WGIPriority()
    return str( type( ar6 ) )

class TestTC03(object):
    def test_ee(self):
      import local_utilities
      self.ar6 = local_utilities.WGIPriority()

my_tests = [TC01(), TC02()]

## line_log_pass/fail are picked up by hook defined in conftest.py
## this approach produces rather opaque error messages in pytest output.

@pytest.mark.parametrize( 'test_function,args,expected,message,line_log_pass,line_log_fail', [(x,x.input_tuple, x.expected,x.message,x.log_pass,x.log_fail) for x in my_tests] )
def test_001(test_function,args,expected,message,line_log_pass,line_log_fail):
    assert  test_function(*args) == expected, message

##
## this is cleaner ... using annotation ...
##
def test_002(__test__: 'x') -> '%%4s: %s [%s]' % (TC02.identifier,TC02.overview):
    import local_utilities

def test_003():
    import local_utilities
    ar6 = local_utilities.WGIPriority()
