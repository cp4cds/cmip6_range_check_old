import logging, time, os

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
      if hasattr( logging, "capture" ):
        logging.captureWarnings(True)
    return log

  



