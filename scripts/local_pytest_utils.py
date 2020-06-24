import pytest, os
import warnings

RAISE_NO_CALLBACK_EXCEPTION =False

class NoCallback(Exception):
   def __init__(self,item,rep):
       self.item = item
       self.rep = rep

class BaseClassISOReports(object):
    pass

class TestReporter(BaseClassISOReports):
    def __init__(self,report_file="pytest_line_log"):
        self.report_file = report_file

    def __call__(self, pytest_report=None,test_case=None,sfx=None, cls=None):
        if pytest_report != None and hasattr( pytest_report, 'failed' ) and pytest_report.failed in [True,False]:
           tag = {True:'OK', False:'ERROR'}[not pytest_report.failed]
        else:
           tag = '-'

        if cls != None:
            cid = '%s' % cls.id
        else:
            cid = ''

        mode = "a" if os.path.exists("pytest_line_log") else "w"
        with open("pytest_line_log", mode) as f:
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
            f.write( '%s\n' %  self.report_line  )
 ##           f.write( ', '.join( dir(item.cls) ) )
        return self.report_line

line_reporter = TestReporter()

def get_user_warning(data):
    class HERE(UserWarning):
        pass
    setattr( HERE, 'data', data )
    return HERE
    
class BaseClassTS(object):
    pass
    
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
