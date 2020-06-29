import pytest, os
import warnings, collections, operator, logging
import generic_utils

RAISE_NO_CALLBACK_EXCEPTION =False


NT__scope = collections.namedtuple( 'scope', ['overview','identifier','description','priority','traceability'] )
NT__test_case_spec = collections.namedtuple( 'test_case_spec', ['overview', 'identifier', 'objective', 'priority', 'traceability', 'preconditions', 'inputs', 'expected_results'])
NT__test_case_spec = collections.namedtuple( 'test_case_spec', ['ov', 'id', 'obj', 'p', 'tr', 'prec', 'i', 'expected'])
NT__test_case = collections.namedtuple( 'test_case', ['spec', 'actual_results'])

__overview__ = "Testing the local utilities module"
__identifier__ = "scope01"
__description__ = """Test of local utilities module, local_utilities.py, which contains functions and classes used in other modules"""
__priority__ = "MUST"
__traceability__ = "documentation is tbd"
test_scope = NT__scope( overview = __overview__, priority=__priority__,identifier=__identifier__, description=__description__, traceability=__traceability__)

class NoCallback(Exception):
   def __init__(self,item,rep):
       self.item = item
       self.rep = rep

class BaseClassISOReports(object):
    pass

class BaseClassTS(object):
    pass

class TestReporter(BaseClassISOReports):
    def __init__(self,log_name=__name__):
        self.log_name = log_name
        log_factory =generic_utils.LogFactory(dir="./logs")
        log_pytest = log_factory( log_name, mode="a", logfile="%s_2020" % log_name )

    def __call__(self, pytest_report=None,test_case=None,sfx=None, cls=None):
        if pytest_report != None and hasattr( pytest_report, 'failed' ) and pytest_report.failed in [True,False]:
           tag = {True:'OK', False:'ERROR'}[not pytest_report.failed]
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
                try:
                    self.report_line += ' {%s || %s}' % (test_case.spec.expected, test_case.result)
                except:
                    pass

        if sfx != None:
                self.report_line += sfx
        log = logging.getLogger( self.log_name )
        log.info( self.report_line )
            ## f.write( '%s\n' %  self.report_line  )
 ##           f.write( ', '.join( dir(item.cls) ) )
        return self.report_line

line_reporter = TestReporter()

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
    def __init__(self, function ):
      ret = function.__annotations__['return']
      if type(ret) == type(dict()):
        self.spec = NT__test_case_spec( **ret )
      elif isinstance(ret,NT__test_case_spec):
        self.spec = ret

      self.function = function
      expected = self.spec.expected
      if type(expected) == type('') and expected.find( 'regex:' ) == 0:
         self.conformance_mode = 'match'
      else:
         self.conformance_mode = 'equals'

      self.ov = self.spec.ov

    def __call__(self,*args,**kwargs):
        self.result = self.function(*args,**kwargs)
        return self.result


def maketest(f):
    """A decorator which converts a function into a pytest compatible test by appending an assertion checking the
    return value against an expected value.
    The expected value must be provided in the 'return' annotation of the function as part of a named tuple.
    """
    expected = f.__annotations__['return']['expected']
    def this(*args,**kwargs) -> TCBuild(f):
        this.__annotations__['return'].result = result = f(*args,**kwargs)
        assert matching(result, expected), 'Result [%s] does not match expected [%s]' % (result,expected)

    return this

    
    
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # we only look at actual failing test calls, not setup/teardown

    if rep.when == "call":
           lr = None
           if any( [x in item.function.__annotations__.keys() for x in ['return','tc']] ) or 'tc' in item.funcargs:
                if 'return' in item.function.__annotations__.keys():
                  ret = item.function.__annotations__['return']
                  src = 'return'
                elif 'tc' in item.function.__annotations__.keys():
                  src = 'tc'
                  ret = item.function.__annotations__['tc']
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
                    lr = line_reporter( pytest_report=rep, test_case=ret, cls=cls )

           if lr == None:
               if RAISE_NO_CALLBACK_EXCEPTION:
                 raise NoCallback(item,rep)
               lr = line_reporter( pytest_report=rep, sfx='{no spec: %s}' % item.function.__name__ )
               warnings.warn("Test function lacks specification: %s" % item.function.__name__, get_user_warning((item,rep) ) )
