import shelve, json, os, sys, glob, collections, time

import utils_walk

def apply_to_list( f, ll, if_empty):
  """Applies function *f* to list if it is not empty, otherwise returns *if_empty*"""
  if len(ll) == 0:
    return if_empty
  else:
    return f(ll)

class JsonAggregate(object):
  def __init__(self, input_files ):
    self.data = dict()
    for f in input_files:
      ee = json.load( open( f, 'r' ) )
      print (f, ee.keys(), ee['data'].keys() )
      key = f.rpartition( '/' )[-1]
      self.data[key] = {k:ee[k] for k in ['consol','header']}
      for k in ['tech','info']:
        this = ee['data'][k]
        if type( this ) == type( [] ):
          self.data[key][k] = this[0]
        else:
          self.data[key][k] = this

  def json_dump(self,input_label,json_file='test.json'):
    oo = open( json_file, 'w' )
    json.dump( {'header':{'title':'Dump of results from %s' % input_label, 'source':'consol_to_json.py::JsonAggregate', 'time':time.ctime() },
                  'data':self.data}, oo, indent=4, sort_keys=True )
    oo.close()



class ShToJson(object):
  def __init__(self,input_file):
    self.w = utils_walk.Walker()
    self.sh = shelve.open( input_file )
    self.info = self.sh['__info__']
    self.ks = [k for k in self.sh.keys() if k[0] != '_']
    self.tech_import()
    self.data_import()
    self.first = True

  def tech_import(self,append=False):

      this = self.sh['__tech__'].copy()
      finfo = this['file_info']
      finfo['fill_value'] = float( finfo['fill_value'] )
      finfo['shape'] = tuple( [int(x) for x in finfo['shape']] )
      if 'time_intervals' in finfo:
        finfo['time_intervals'] = tuple( [float(x) for x in finfo['time_intervals'] ] )
      this['file_info'] = finfo
      if append:
        self.tech.append( this )
      else:
        self.tech = this

  def append(self,input_file):

      if self.first:
        self.info = [self.info,]
        self.tech = [self.tech,]
      self.first = False

      self.sh = shelve.open( input_file )
      self.ks = [k for k in self.sh.keys() if k[0] != '_']
      self.info.append( self.sh['__info__'] )
      self.tech_import(append=True)
      self.data.update( self.w(self.sh) )
    
  def data_import(self):
      self.data = self.w( self.sh )

  def data_import_00(self):
    SKIPPED = []
    self.data = {}
    for k in self.ks:
      this = {}
      for k1 in self.sh[k].keys():
        frag = self.sh[k][k1]
        print( "%s: %s" % (k1, frag) )
        if k1 == 'basic':
#
# basic: 3 floats and an integer: min, max, mean absolute, count of missing data.
#
          this['basic'] = (*[float(x) for x in frag[:3]],  int(frag[3]) )
        elif k1 == 'quantiles':
#
# quantiles: a list of quantiles
#
          this[k1] = [float(x) for x in frag]
        elif k1 == 'extremes':
#
# extreme values (number set by "nextremes" , deafault 10). The extremes and locations are provided (as index values)
#
          res = []
          for trip in frag:
            res.append( [trip[0], trip[1], [float(x) for x in trip[2]]] )
          this[k1] = res
        elif k1 == 'mask_ok':
#
# mask_ok: information about masking: consistency between data variable and mask variable
#
#     list: string followed by a sequence of integers
#
          this[k1] = [frag[0],*[int(x) for x in frag[1:]]]
        elif k1 == 'fraction':
#
# fraction: information about the "fraction" field which potentially provides masking information
#     list: string followed by a sequenc of floats
#
          this[k1] = [frag[0],*[float(x) for x in frag[1:]]]
      ###this[k1] = frag

        elif k1 == 'empty':
#
# empty: boolean value, indicating all data missing in this layer
#
          this[k1] = frag
        else:
          SKIPPED.append( k1 )

      if len(SKIPPED) != 0:
        this['SKIPPED'] = SKIPPED
        print('SKIPPED RECORDS: %s' % SKIPPED ) 

      self.data[k] = this

  def _gather_basic(self):
      """Consolidate results of scan to get max, min etc over the a full variable;
      NB ... does not yet deal with levels
      """
      
      ks = sorted( [k for k in self.data.keys() if k[0] != '_'] )
      basic = [ self.data[k]['basic'] for k in ks ]
      masks_ok = [ self.data[k].get('mask_ok', None) for k in ks ]
      fraction = [ self.data[k].get('fraction', None) for k in ks ]
      data_min = apply_to_list( min, [x[0] for x in basic if x[0] != None], None )
      data_max = apply_to_list( max, [x[1] for x in basic if x[1] != None], None )
      data_ma_min = apply_to_list( min, [x[2] for x in basic if x[2] != None], None )
      data_ma_max = apply_to_list( max, [x[2] for x in basic if x[2] != None], None )
      self.range_comment = 'Data range: %s to %s; mean absolute range %s to %s' % (data_min,data_max,data_ma_min,data_ma_max)
      nfv = sum( [x[3] for x in basic] )

      drl = [data_min,data_max,data_ma_min,data_ma_max]
      ks2 = [k for k in ks if k.rpartition(':')[-1].find( '-' ) != -1]
      levs = dict()
      if len(ks2) == len(ks):
        with_levels = True
        for k in ks:
          levs[k] = [int( x ) for x in k.rpartition(':')[-1].split( '-' )]
          
      elif len(ks2) == 0:
        with_levels = False
        for k in ks:
          levs[k] = int( k.rpartition(':')[-1] )
      else:
        print ("Does not match all with levels or all without")
        print ("len ks: %s, len ks2: %s" % (len(ks),len(ks2)))
        raise

      if with_levels:
          basic0 = [ self.data[k]['basic'] for k in ks if levs[k][1] == 0 ]
          data_min_l0 = apply_to_list( min, [x[0] for x in basic0 if x[0] != None], None )
          data_max_l0 = apply_to_list( max, [x[1] for x in basic0 if x[1] != None], None )
          drl += [data_min_l0,data_max_l0]
          self.range_comment = 'Data range: %s to %s (l0: %s to %s); mean absolute range %s to %s' % (data_min,data_max,data_min_l0,data_max_l0,data_ma_min,data_ma_max)

      consol = dict( basic=drl, nfv=nfv )

      if all( [x == None for x in fraction] ):
        consol['fraction_report'] = ('no report',None,None,None,None)
      else:
        cmt = set( [f[0] for f in fraction])
        min1 = apply_to_list( min, [f[1] for f in fraction if f[1] != None], None )
        max1 = apply_to_list( max, [f[2] for f in fraction if f[2] != None], None )
        min2 = apply_to_list( min, [f[3] for f in fraction if f[3] != None], None )
        max2 = apply_to_list( max, [f[4] for f in fraction if f[4] != None], None )
        consol['fraction_report'] = (cmt,min1,max1,min2,max2)


      mask_comment = ''
      if all( [x == None for x in masks_ok] ):
        mask_check = None
        mask_comment = 'No mask report'
      elif all( [x[0] == 'masks_match' for x in masks_ok] ):
        mask_check = True
        s1 = set( [x[1] for x in masks_ok] )
        assert len(s1) == 1, 'Unexpected variation in mask ....'
        n1 = s1.pop()
        mask_comment = 'Mask count = %s' % n1
      else:
        mask_check = False

      consol['mask_info'] = (mask_check,mask_comment)
      self.consol = self.w( consol )


  def json_dump(self,input_label,json_file='test.json'):
    oo = open( json_file, 'w' )
    json.dump( {'header':{'title':'Dump of results from %s' % input_label, 'source':'consol_to_json.py', 'time':time.ctime() },
                  'consol':self.consol,
                  'data':dict( info=self.info, tech=self.tech, data=self.data )}, oo, indent=4, sort_keys=True )
    oo.close()


def ssort_02( ll ):
  oo = collections.defaultdict( list )
  for f in ll:
    fn = f.rpartition( '/' )[-1]
    a,b = fn.split( '_' )[:2]
    oo['%s_%s' % (a,b) ].append( f )
  return oo
    
def ssort( ll ):
  oo = collections.defaultdict( list )
  for f in ll:
    fn = f.rpartition( '/' )[-1]
    a,x,b = fn.rpartition( '_' )
    oo[a].append( f )
  return oo
    
def fnfilt( ll ):
  oo = []
  for f in ll:
    if f[-4:] == '.dat':
      oo.append( f[:-4] )
    else:
      oo.append(  f )
  return oo


if __name__ == "__main__":
  if sys.argv[1] == '-f':
    input_file = sys.argv[2] 
    json_file = '%s.json' % input_file
    s = ShToJson( input_file )
    s.json_dump( input_file, json_file=json_file )
  elif sys.argv[1] == '-a':
    input_files = sorted( glob.glob( '%s*.json' % sys.argv[2]  ) )
    agg = JsonAggregate(input_files)
    agg.json_dump( sys.argv[2] )
  elif sys.argv[1] == '-ad':
    input_files = glob.glob( '%s/*.json' % sys.argv[2]  )
    ee = ssort_02( input_files )
    for k,ll in ee.items():
      print( k )
      agg = JsonAggregate(sorted(ll))
      agg.json_dump( k, 'json_agg_02/%s.json' % k )
  elif sys.argv[1] == '-l':
    input_files = fnfilt( sys.argv[2:]  )
    json_file = '%s.json' % input_files[0]
    s = ShToJson( input_files[0] )
    for f in input_files[1:]:
      s.append(f)
    s._gather_basic()
    print (s.range_comment )
    s.json_dump( input_files[0] + '...', json_file=json_file )
  elif sys.argv[1] == '-d':
    input_files = sorted( glob.glob( '%s/*.dat' % sys.argv[2]  ) )
    d1 = ssort( input_files )
    print( d1.keys() )
    for k in sorted( list( d1.keys() ) ):
      input_files = sorted( fnfilt( d1[k] ) )
      json_file = 'json_02/%s.json' % k
      s = ShToJson( input_files[0] )
      for f in input_files[1:]:
        s.append(f)
      s._gather_basic()
      print (k)
      print (s.range_comment )
      s.json_dump( input_files[0] + '...', json_file=json_file )
