import pytest
import collections
from local_pytest_utils import MakeTest, TCBuild, TestReporter, Check3
import _pytest
from _pytest.runner import TestReport as TstReport


project = 'rt001'
scope_id = 'sc001'

##
## session .... does this apply to module?
##
@pytest.fixture(scope="session", autouse=True)
def log_global_env_facts(record_testsuite_property):
    record_testsuite_property('SCOPE_ID','scope101')

class Check(object):
    def __init__(self,record_property,**kwargs):
        self.ee = dict()
        for k,v in kwargs.items():
            record_property(k,v)
            self.ee[k] = v
    def __call__(self,value):
        assert value == self.ee['expected']

class Check2(object):
    def __init__(self,record_property,func,sfx='Check2'):
        self.ee = dict()
        self.function = func
        fid = func.__name__
        self.test_name = fid
        tr = '%s:%s:%s' % (project,scope_id,fid)
        defaults = {'prec':'None', 'i':'None', 'tr':tr, 'id':fid }
        ret = func.__annotations__['return']
        for k,v in defaults.items():
            if k not in ret:
                ret[k] = v
        func.__annotations__['tc'] = TCBuild( func, TestReporter('test01',sfx=sfx), ret=ret )
        self.rp = record_property
        for k in ['ov','obj','p','tr','prec','i','expected','id']:
            v = ret.get(k, defaults.get(k) )
            record_property('%s.%s' % (fid,k),v)
            self.ee[k] = v

    def __call__(self,value):
        self.rp( 'result', value )
        self.function.__annotations__['tc'].result = value
        assert value == self.ee['expected'], '%s: result [%s] does not match expected [%s]' % (self.test_name,value,self.ee['expected'])

class Check3_xx(object):
    def __init__(self,func,sfx='Check3'):
        self.ee = dict()
        self.function = func
        fid = func.__name__
        self.test_name = fid
        tr = '%s:%s:%s' % (project,scope_id,fid)
        defaults = {'prec':'None', 'i':'None', 'tr':tr, 'id':fid }
        ret = func.__annotations__['return']
        for k,v in defaults.items():
            if k not in ret:
                ret[k] = v
        func.__annotations__['tc'] = TCBuild( func, TestReporter('test01',sfx=sfx), ret=ret )
        for k in ['ov','obj','p','tr','prec','i','expected','id']:
            v = ret.get(k, defaults.get(k) )
            record_property('%s.%s' % (fid,k),v)
            self.ee[k] = v

    def __call__(self,value):
        self.function.__annotations__['tc'].result = value
        assert value == self.ee['expected'], '%s: result [%s] does not match expected [%s]' % (self.test_name,value,self.ee['expected'])

class MKK(object):
    def __init__(self,rp):
        self.rp = rp

    def __call__(self,f):
      def g(*args):
        Check( self.rp, **f.__annotations__['return'] )( f(*args) )
      return g

def mk(f):
    def g(*args):
      Check( record_property, **f.__annotations__['return'] )( f(*args) )
    return g

##@pytest.mark.incremental
class TestTest:
  id = 'scope101'

  @MakeTest()
  def test_pass01(self) -> dict( ov='Test of testing framewrk', id='tc101',
                              obj='Evaluate wrapping code', p='MUST', tr='tbd', prec='None', i='None', expected=True ):
      return True

  @pytest.mark.xfail
  @MakeTest()
  def test_fail01(self) -> dict( ov='Test of testing framewrk', id='tc102',
                              obj='Evaluate wrapping code', p='MUST', tr='tbd', prec='None', i='None', expected=True ):
      return False

  @MakeTest()
  def test_pass02(self) -> dict( ov='Test of making a report', id='tc103',
                              obj='Evaluate wrapping code', p='MUST', tr='tbd', prec='None', i='None', expected=True ):
      rep = TstReport('this_node', '/tmp', ['CMIP','test'],'failed','longrepr','call')
      return rep.failed

  @MakeTest()
  def test_fail02(self) -> dict( ov='Test of making a report', id='tc104',
                              obj='Evaluate wrapping code', p='MUST', tr='tbd', prec='None', i='None', expected=True ):
      return False

  def test_fail03(self) -> dict( ov='Test of making a report', id='tc105',
          obj='Evaluate wrapping code', p='MUST', tr='tbd', prec='None', i='None', expected=True ):
      Check3( self.test_fail03 )(
       False
       )

  def test_fail04(self) -> dict( ov='Test of making a report', 
                              obj='Evaluate wrapping code', p='MUST',  expected=True ):
      Check3( self.test_fail04 )(
       False
      )

  def test_pass03(self) -> dict( ov='Test of making a report', 
                              obj='Evaluate wrapping code', p='MUST',  expected=True ):
      tt = Check3( self.test_pass03 )
      x = 3
      y = 4
      z = 5
      tt( x**2 + y**2 == z**2 + 1 )

##
## the record_property fixture is not picked up in this format ...
## 
## needs to be placed in method, as above. [in fail03]
##
  ##@MKK( record_testsuite_property )
  ##def test_fail05(self) -> dict( ov='Test of making a report', id='tc105',
          ##obj='Evaluate wrapping code', p='MUST', tr='tbd', prec='None', i='None', expected=True ):
      ##return False
