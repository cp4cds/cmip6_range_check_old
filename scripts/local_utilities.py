import logging, time, os, collections

NT_RangeValue = collections.namedtuple( "range_value", ["value","status"] )
NT_RangeSet = collections.namedtuple( "range_set", ["max","min","ma_max","ma_min"] )
null_range_value = NT_RangeValue( None, "NONE" )

class WGIPriority(object):
  def __init__(self,ifile="AR6_priority_variables_02.csv" ):
    ii = open( ifile ).readlines()
    self.ee = dict()
    self.ranges = dict()
    for l in ii:
      rec = l.split( "\t" )
      id, units = rec[:2]
      vt = rec[2:10]
      if not all( [vt[i] == "-" for i in [1,3,5,7]]):
        xx = []
        for i in [0,2,4,6]:
          if vt[i+1] != "-":
            xx.append( NT_RangeValue(vt[i],vt[i+1]) )
          else:
            xx.append( null_range_value )
        self.ranges[id] = NT_RangeSet( xx[0], xx[1], xx[2], xx[3] )

      self.ee[id] = units

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

    log = logging.getLogger(name)
    fHdlr = logging.FileHandler(self.log_file,mode=mode)
    fileFormatter = logging.Formatter('%(message)s')
    fHdlr.setFormatter(fileFormatter)
    log.addHandler(fHdlr)
    log.setLevel(logging.INFO)
    self.logs[name] = log
    if warnings:
      np_log = logging.getLogger("py.warnings")
      np_log.setLevel(logging.WARN)
      np_log.addHandler(fHdlr)
      self.logs["py.warnings"] = np_log
      if hasattr( logging, "captureWarnings" ):
        logging.captureWarnings(True)
    return log

  


if __name__ == "__main__":
   wg1 = WGIPriority()
   print ( wg1.ranges.keys() )
   k = wg1.ranges.keys().pop()
   print ( k, wg1.ranges[k] )
