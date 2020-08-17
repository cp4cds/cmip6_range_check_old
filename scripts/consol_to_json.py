import shelve, json, os, sys, glob, collections

import utils_walk

class ShToJson(object):
  def __init__(self,input_file):
    self.w = utils_walk.Walker()
    self.sh = shelve.open( input_file )
    self.info = self.sh['__info__']
    self.ks = [k for k in self.sh.keys() if k[0] != '_']
    self.tech_import()
    self.data_import()

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

      self.sh = shelve.open( input_file )
      self.ks = [k for k in self.sh.keys() if k[0] != '_']
      self.info = [self.info,]
      self.tech = [self.tech,]
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
      """Concolidate results of scan to get max, min etc over the a full variable;
      NB ... does not yet deal with levels
      """
      
      ks = sorted( [k for k in self.data.keys() if k[0] != '_'] )
      basic = [ self.data[k]['basic'] for k in ks ]
      masks_ok = [ self.data[k].get('mask_ok',None) for k in ks]
      fraction = [ self.data[k].get('fraction',None) for k in ks]
      data_min = min( [x[0] for x in basic] )
      data_max = max( [x[1] for x in basic] )
      data_ma_min = min( [x[2] for x in basic] )
      data_ma_max = max( [x[2] for x in basic] )
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
          data_min_l0 = min( [x[0] for x in basic0] )
          data_max_l0 = max( [x[1] for x in basic0] )
          drl += [data_min_l0,data_max_l0]
          self.range_comment = 'Data range: %s to %s (l0: %s to %s); mean absolute range %s to %s' % (data_min,data_max,data_min_l0,data_max_l0,data_ma_min,data_ma_max)



  def json_dump(self,input_label,json_file='test.json'):
    oo = open( json_file, 'w' )
    json.dump( {'A: header':'Dump of results from %s' % input_label, 'B: data':dict( info=self.info, tech=self.tech, data=self.data )}, oo, indent=4, sort_keys=True )
    oo.close()


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
      json_file = '%s.json' % k
      s = ShToJson( input_files[0] )
      for f in input_files[1:]:
        s.append(f)
      s._gather_basic()
      print (k)
      print (s.range_comment )
      s.json_dump( input_files[0] + '...', json_file=json_file )
