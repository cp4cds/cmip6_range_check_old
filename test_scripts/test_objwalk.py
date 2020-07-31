
import numpy

from objwalk import Walker

z = numpy.zeros( 5 )
obj1 = dict( a=numpy.zeros( (5,5) ), b=numpy.array( range(4) ), c=set(['a','v','b']), z=z[0] )

w = Walker()
res = w(obj1)

print (res )
print (w.met)
print (w.yielded)


class MyClass(object):
    def __init__(self,a,b):
        self.a = a
        self.b = b


x = type( MyClass('a',1) )
specials = { x:lambda x:dict( a=x.a, b=x.b) }

w = Walker(specials=specials)

obj2 = dict( a=MyClass( 'name', 'fred' ) )
res = w(obj2)

print (res )
print (w.met)
print (w.yielded)
print (w.specials.keys())
