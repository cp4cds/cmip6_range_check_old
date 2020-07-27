
from types import MethodType


def  raisex(Ex): raise Ex
def verify(x,y): assert x == y

class Dec1(object):
    def __init__(self,dec):
        self.dec = dec
    def __call__(self,cls):
        """Obtain a list of all test methods in the class passed as argument and apply self.dec as a decorator"""

        method_list = [func for func in dir(cls) if callable(getattr(cls, func)) and func[:5] == 'test_']
        for m in method_list:
            this = getattr(cls, m)
            setattr( cls, m,  MethodType( self.dec( this), cls )  )

        method_list = [func for func in dir(cls) if callable(getattr(cls, func)) and func[:5] == 'x_']
        for m in method_list:
            this = getattr(cls, m)
        return cls

class Me(object):
    def __init__(self,f):
        setattr( self, '__me__', MethodType( f, self ) )
    def __call__(self):
        return self.__me__()
        

#
# Use of f to decorate test functions will enables pytest to work at a functional level ..
# but the output is low on meaningful content.
# the gain is ....
def f(m):
    def m2(self): 
        assert m(self) == m.__annotations__['return']
    return m2

def g(m):
    return lambda self: verify( m(self) , m.__annotations__['return'] )

#
# idea here is to return function, value and expected value as a tuple ..
#
def h(m):
    def m2(self): 
        res = m()
        return (m,res,m.__annotations__['return'] )
    return m2

class TestB(object):
    def test_bb(self) -> 4:
        x = 3
        y = 4
        return x

    def x_bb(self) -> 5:
        return 4

##
## Thinking: try to avoid out of band configuration and tricky code introspection used in pytest.
## put information in the method ...
## make it usable
##
def pq_get_testaables(cls) -> "list: list of methods in *cls* which are recognised as testable":
    """Return a list of methods in a class which have expected values and priority specified in the return annotation.
    These methods can be tested by the PQ library.
    Note that there are additional optional properties which may be placed in the return annotation to influence the
    behaviour of the PQ test.
    [there should be an option for testable input arguments here as well ....]
    """
    for func in dir(cls):
        this = getattr(cls, func)
        if callable(this) and hasattr( this, '__annotations__'):
            if 'return' in this.__annotations and all( [ x in this.__annotations__['return'] for x in ['expected','priority'] ] ):
                oo.append( func )
    return oo

class TestX(object):
    PQ_test_data = dict( exists_and_large_enough=dict(file=['testfile1.txt','testfile2.txt'] ) )

    def exists_and_large_enough(self,file -> 'str:posix file path', min_size=20) -> dict(expected=True, priority='MUST', index=1):
        return os.path.isfile(file) and (os.stat(file).st_size >= min_size)

    def test_bb(self) -> dict(expected=4, priority='MUST', index=1):
        x = 3
        y = 4
        return x

    def x_bb(self) -> 5:
        return 4

##TestB = Dec1(f)(TestB)

TestB = Dec1(f)(TestB)
