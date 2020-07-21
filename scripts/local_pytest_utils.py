import pytest, os
import warnings, collections, operator, logging
import generic_utils

## see https://docs.pytest.org/en/latest/example/simple.html#incremental-testing-test-steps
from typing import Dict, Tuple

# store history of failures per test class name and per index in parametrize (if parametrize used)
##_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}
_test_failed_incremental = {}

RAISE_NO_CALLBACK_EXCEPTION = False


NT__scope = collections.namedtuple( 'scope', ['overview','identifier','description','priority','traceability'] )
NT__test_case_spec = collections.namedtuple( 'test_case_spec', ['overview', 'identifier', 'objective', 'priority', 'traceability', 'preconditions', 'inputs', 'expected_results'])
NT__test_case_spec = collections.namedtuple( 'test_case_spec', ['ov', 'id', 'obj', 'p', 'tr', 'prec', 'i', 'expected'])
NT__test_case = collections.namedtuple( 'test_case', ['spec', 'actual_results'])
NT__config = collections.namedtuple( 'config', ['project','scope','log_name'])

__overview__ = "Testing the local utilities module"
__identifier__ = "scope01"
__description__ = """Test of local utilities module, local_utilities.py, which contains functions and classes used in other modules"""
__priority__ = "MUST"
__traceability__ = "documentation is tbd"
test_scope = NT__scope( overview = __overview__, priority=__priority__,identifier=__identifier__, description=__description__, traceability=__traceability__)

project = 'rt001'
scope_id = 'sc001'

class BaseClassCheck(object):
    config = NT__config( project='default_project', scope='default_scope', log_name='test01' )
    reporter = None
    review_template = 'Failed tests: %s, passed tests: %s'

    @classmethod
    def configure(cls,project,scope,log_name,reporter=None):
        cls.config = NT__config( project=project, scope=scope, log_name=log_name )
        if reporter != None:
          cls.reporter = reporter
    
class Check3(BaseClassCheck):
    def __init__(self,func,sfx='',reset=False,blocking=False):
        self.ee = dict()
        self.function = func
        fid = func.__name__
        self.test_name = fid
        tr = '%s:%s:%s' % (self.config.project,self.config.scope,fid)
        defaults = {'prec':'None', 'i':'None', 'tr':tr, 'id':fid }
        ret = func.__annotations__['return']
        if BaseClassCheck.reporter == None:
            BaseClassCheck.reporter = LogReporter(self.config.log_name,sfx=sfx)

        for k,v in defaults.items():
            if k not in ret:
                ret[k] = v
        func.__annotations__['tc'] = TCBuild( func, BaseClassCheck.reporter, ret=ret )
        if blocking:
            func.__annotations__['tc'].is_blocking = True

        for k in ['ov','obj','p','tr','prec','i','expected','id']:
            v = ret.get(k, defaults.get(k) )
            self.ee[k] = v

        if reset:
            self._reset()
      ####  print ('FAIL COUNT: %s' % fid, self.reporter.fails )
      #### Note that the mark.incremental approach was tried,  but did not work with hooks implemented
        if self.reporter.blocking_fails > 0 and fid.find( 'wrapup' ) == -1:
            pytest.skip( 'blocking_fail count > 0' )

    @classmethod
    def _reset(cls):
         BaseClassCheck.reporter.fails = 0
         BaseClassCheck.reporter.passes = 0

    @classmethod
    def review(cls):
         return BaseClassCheck.review_template % (BaseClassCheck.reporter.fails,BaseClassCheck.reporter.passes)


    def __call__(self,value,cmt=None):
        self.function.__annotations__['tc'].result = (value,cmt)
        assert value == self.ee['expected'], '%s: result [%s] does not match expected [%s]' % (self.test_name,value,self.ee['expected'])

class NoCallback(Exception):
   def __init__(self,item,rep):
       self.item = item
       self.rep = rep

class BaseClassISOReports(object):
    pass

class BaseClassTS(object):
    pass
    

class LogReporter(BaseClassISOReports):
    def __init__(self,log_name,log_file=None,log_dir='./logs',sfx=None):
        self.log_name = log_name
        if log_file == None:
            log_file = "%s_2020" % log_name

        log_factory = generic_utils.LogFactory(dir=log_dir)
        log_pytest  = log_factory( log_name, mode="a", logfile=log_file )
        self.sfx = sfx
        self.fails = 0
        self.blocking_fails = 0
        self.passes = 0

    def __call__(self, pytest_report=None,test_case=None,sfx=None, cls=None):
        cmt = None
        if pytest_report != None and hasattr( pytest_report, 'outcome' ) and pytest_report.outcome in ['passed', 'failed', 'skipped']:
            tag = {'passed':'OK', 'failed':'FAIL', 'skipped':'SKIP'}[pytest_report.outcome]
        ##if pytest_report != None and hasattr( pytest_report, 'failed' ) and pytest_report.failed in [True,False]:
           ##tag = {True:'OK', False:'ERROR'}[not pytest_report.failed]
        else:
           tag = '-'

        if cls != None:
            cid = '%s' % cls.id
        else:
            cid = ''

        ##mode = "a" if os.path.exists("pytest_line_log") else "w"
        ##with open("pytest_line_log", mode) as f:
        if test_case == None:
                self.report_line =  '%s:%s..: ' % (tag, cid)   
        else:
                self.report_line =  '%s:%s.%s: %s' % (tag, cid, test_case.spec.id, test_case.spec.ov)   
                if hasattr( test_case, 'result' ):
                    if type( test_case.result ) == type( () ) and len( test_case.result ) == 2:
                        result, cmt  = [str( x) for x in test_case.result] 
                    else:
                        result = str( test_case.result )
                else:
                    result = "****"
                cmt_item = cmt if cmt != None else ''

                if tag == 'FAIL':
                  self.fails += 1
                  if test_case.is_blocking:
                     self.blocking_fails += 1
                elif tag == 'OK':
                  self.passes += 1
                self.report_line = '\t'.join( [tag] + [str( test_case.spec._asdict()[x] ) for x in ['id','expected']] + [result,cmt_item] )


        if sfx != None:
                self.report_line += sfx
        if self.sfx != None:
            self.report_line += ' ' + self.sfx

        log = logging.getLogger( self.log_name )
        log.info( self.report_line )
            ## f.write( '%s\n' %  self.report_line  )
 ##           f.write( ', '.join( dir(item.cls) ) )
        return self.report_line

##line_reporter = LogReporter()

def get_user_warning(data):
    class HERE(UserWarning):
        pass
    setattr( HERE, 'data', data )
    return HERE


def matching( result, expected):
    """Check result against expected.
       Allows for encoding of lt/gt/le/ge in text strings.
       """
    if type(expected) == type('') and expected.find(':') != -1 and expected.split( ':' )[0] in ['lt','gt','le','ge']:
        exp = eval( expected[3:] )
        op = expected[:2]
        assert op in ['lt','gt','le','ge']
        return operator.__dict__[ op ](result,exp)
    else:
        return result == expected


class TCBuild(BaseClassTS):
    """
    BaseClassTS: brings in a standard report function which assumes a spec attribute which is an instance of NT__scope
    """
    scope = test_scope
    def __init__(self, function, reporter, ret=None):
      if ret == None:
        ret = function.__annotations__['return']
      self.reporter = reporter

      if type(ret) == type(dict()):
        self.spec = NT__test_case_spec( **ret )
      elif isinstance(ret,NT__test_case_spec):
        self.spec = ret
      print( 'TCBuild Instantiating: %s' % function.__name__ )

      self.function = function
      expected = self.spec.expected
      if type(expected) == type('') and expected.find( 'regex:' ) == 0:
         self.conformance_mode = 'match'
      else:
         self.conformance_mode = 'equals'

      self.ov = self.spec.ov
      self.is_blocking = False

    def report(self,*args,**kwargs):
        return self.reporter( *args,**kwargs)

    def __call__(self,*args,**kwargs):
        self.result = self.function(*args,**kwargs)
        return self.result


class MakeTest(object):
  """A decorator which converts a function into a pytest compatible test by appending an assertion checking the
    return value against an expected value.
    The expected value must be provided in the 'return' annotation of the function as part of a named tuple.
  """
  def __init__(self,reporter=None,log_file=None,log_name=None):
    if reporter != None:
        self.reporter = reporter
    elif BaseClassCheck.reporter != None:
        self.reporter = BaseClassCheck.reporter
    else:
        if log_name == None:
            log_name = __name__
        self.reporter = LogReporter(log_name,log_file=log_file)

  def __call__(self,f):
    expected = f.__annotations__['return']['expected']
    def this(*args,**kwargs) -> TCBuild(f,self.reporter):
        this.__annotations__['return'].result = result = f(*args,**kwargs)
        assert matching(result, expected), 'Result [%s] does not match expected [%s]' % (result,expected)

    return this

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    # we only look at actual failing test calls, not setup/teardown

    # execute all other hooks to obtain the report object

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
           lr = None
           if any( [x in item.function.__annotations__.keys() for x in ['return','tc']] ) or 'tc' in item.funcargs:
        
                if 'tc' in item.function.__annotations__.keys():
                  src = 'tc'
                  ret = item.function.__annotations__['tc']
                elif 'return' in item.function.__annotations__.keys():
                  ret = item.function.__annotations__['return']
                  src = 'return'
                else:
                  src = 'tc*'
                  ret = item.funcargs['tc']

                ##
                ##objective here is to compile an ISO ... record combining information about tests and results.
                ##
                if isinstance( ret, BaseClassTS ) and  hasattr( ret, 'spec' ):
                    if hasattr( item, 'cls' ):
                        cls = item.cls
                    else:
                        cls = None
                    lr = ret.report( pytest_report=rep, test_case=ret, cls=cls )
                elif not isinstance( ret, BaseClassTS ):
                   warnings.warn("Test function ret is not a BaseClassTS instance: %s" % item.function.__name__, get_user_warning((item,rep) ) )
                else:
                   warnings.warn("Test function lacks specification: %s" % item.function.__name__, get_user_warning((item,rep) ) )
           else:
               warnings.warn("Test function lacks hook: %s" % item.function.__name__, get_user_warning((item,rep) ) )

           if lr == None:
               if RAISE_NO_CALLBACK_EXCEPTION:
                 raise NoCallback(item,rep)
               ##lr = line_reporter( pytest_report=rep, sfx='{no spec: %s}' % item.function.__name__ )

