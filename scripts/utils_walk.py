#http://code.activestate.com/recipes/577982-recursively-walk-python-objects/

from collections.abc import Mapping, Set, Sequence

# dual python 2/3 compatability, inspired by the "six" library
string_types = (str, unicode) if str is bytes else (str, bytes)
iteritems = lambda mapping: getattr(mapping, 'iteritems', mapping.items)()


class Walker(object):
    """Walk an object and convert to json-ready objects (list, dict, float, int).
       Deals with sets (converted to ordered lists) and numpy floats and ints (converted to float and int respectively).

       Keys coerced to be one of: str, int, float, bool  (see https://docs.python.org/3/library/json.html)
       e.g. tuple as key ... is replaced by str(x)
    """

    def __init__(self,specials=dict(),key_specials=dict(),order_sets=True):
        self.met = set()
        self.key_types = set()
        self.yielded = set()
        self.specials = specials
        self.key_specials = key_specials
        self.order_sets = order_sets

    def __call__(self,obj,specials=dict()):
      self.met.add(type(obj))
      res = self._action(obj)
      self.yielded.add(type(res))
      return res

    def coerce_key_reset(self):
        self._new_keys = set()

    def coerce_key(self,k):
        if isinstance( k, (bool, int, str, float) ):
            return k
        self.key_types.add( type(k) )
        if type(k) in self.key_specials:
          newk = self.key_specials[ type(k) ](k)
        else:
          newk = str(k)

        assert newk not in self._new_keys, 'Key coersion results in duplication of key values: %s' % newk
        return newk

    def _action(self,obj):
      """Coerce 'obj' into an acceptable type, recursively calling 'self' for walkable objects.

         The approach here builds a new object in place ... rather than flattening to a list of objects as in os.walk
         -- 
      """

#
#   Return objects of approved type without change.
#
      if type(obj) in [type(x) for x in [1.,1,'x']]:
          return obj

#
#   The specials dictionary allows special treatment to be declared, e.g. for user-defined data types
#
      if type(obj) in self.specials:
          return self.specials[ type(obj) ](obj)

#
#   The 'tolist' attribute is used as a marker for numpy arrays ... (without incurring the dependency on numpy which
#   would result from having an explicit test).
#
#   The numpy tolist method can return a scalar if the numpy array object has unit length. Need to test for this here.
#
      if hasattr( obj, 'tolist' ):
          r1 = obj.tolist()
          if isinstance(obj, Sequence):
             return [self(v) for v in r1]
          else:
             return self(r1)

#
#   All mappings are transformed into dictionaries, with keys from a defined set of acceptable types.
#   The coerce_key method deals with key uniqueness
#
      elif isinstance(obj, Mapping):
          self.coerce_key_reset()
          return {self.coerce_key(k):self(v) for k,v in obj.items()}

#
# Sets are returned as lists ... optionally ordered
#
      elif isinstance(obj, (Set)) and self.order_sets and not isinstance(obj, string_types):
          return [self(v) for v in sorted( list( obj ) )]

#
# Sequences and sets returned as lists ... transformation applied recursively to each element
#
      elif isinstance(obj, (Sequence, Set)) and not isinstance(obj, string_types):
          return [self(v) for v in obj]


#
# for objects with are subclasses of string, float or integer, transform into primitive type (e.g. numpy floats are converted to float)
#
      elif isinstance(obj,str):
          return str(obj)
      elif isinstance(obj,float):
          return float(obj)
      elif isinstance(obj,int):
          return int(obj)
      else:
          return obj

if __name__ == "__main__":
    print( "Test1" )
    w = Walker()
    res = w( dict( a={1,2,3,4,3,3}, b=(4,5,dict(alpha='beta')) ) )
    print (res)
    print (sorted([str(x) for x in w.met]))
