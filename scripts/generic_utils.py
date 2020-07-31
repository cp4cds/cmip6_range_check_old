import logging, time, os, json, sys

class ShToJson(object):
  def __init__(self,input_file):
    self.sh = shelve.open( input_file )
    self.info = self.sh['__info__']
    self.ks = [k for k in self.sh.keys() if k[0] != '_']
    self.tech_import()
    self.data_import()

  def tech_import(self):

      this = self.sh['__tech__'].copy()
      finfo = this['file_info']
      finfo['fill_value'] = float( finfo['fill_value'] )
      finfo['shape'] = tuple( [int(x) for x in finfo['shape']] )
      if 'time_intervals' in finfo:
        finfo['time_intervals'] = tuple( [float(x) for x in finfo['time_intervals'] ] )
      this['file_info'] = finfo
      self.tech = this

  def data_import(self):
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

  def json_dump(self,json_file='test.json'):
    oo = open( json_file, 'w' )
    json.dump( {'A: header':'Dump of results from %s' % input_file, 'B: data':dict( info=self.info, tech=self.tech, data=self.data )}, oo, indent=4, sort_keys=True )
    oo.close()


class LogFactory(object):
  def __init__(self, dir='.'):
    """
    LogFactory instantiates to a callable which can generate logs from the logging module.
    """
    self.tstring2 = '%4.4i%2.2i%2.2i' % time.gmtime()[0:3]
    self.logdir = dir
    self.logs = dict()
    if not os.path.isdir( dir ):
      os.mkdir(dir )
      print ( 'Log: making a new directory fr log files: %s' % dir )

  def __call__(self,name,dir=None,logfile=None,mode="a", warnings=False):
    if dir == None:
      dir = self.logdir
    if logfile != None:
      self.log_file = '%s/%s' % (dir,logfile)
    else:
      self.log_file = '%s/log_%s_%s.txt' % (dir,name,self.tstring2)

    existing_log =  name in logging.root.manager.loggerDict
    log = logging.getLogger(name)
    if not existing_log:
      fHdlr = logging.FileHandler(self.log_file,mode=mode)
      fileFormatter = logging.Formatter('%(message)s')
      fHdlr.setFormatter(fileFormatter)
      log.addHandler(fHdlr)
      log.setLevel(logging.INFO)
      if warnings:
        np_log = logging.getLogger("py.warnings")
        np_log.setLevel(logging.WARN)
        np_log.addHandler(fHdlr)
        self.logs["py.warnings"] = np_log
        if hasattr( logging, "captureWarnings" ):
          logging.captureWarnings(True)
    self.logs[name] = log
    return log

if __name__ == "__main__":
  print ("Test run of ShToJson")
  input_file = sys.argv[1] 
  json_file = '%s.json' % input_file
  s = ShToJson( input_file )
  s.json_dump( json_file )

