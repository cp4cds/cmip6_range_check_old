import logging, time, os, json, sys, shelve, glob


class ComplexEncoder(json.JSONEncoder):
     def default(self, obj):
         if isinstance(obj, complex):
             return [obj.real, obj.imag]
         # Let the base class default method raise the TypeError
         return json.JSONEncoder.default(self, obj)

class ShToJson(object):
  def __init__(self,input_file):
    self.gathered = False
    self.append = False
    self.fname = input_file.rpartition('/')[-1]
    self.input_file = input_file
    self.files = [input_file,]
    self.sh = shelve.open( input_file )
    self.info = self.sh['__info__']
    self.ks = [k for k in self.sh.keys() if k[0] != '_']
    self.tech = dict()

    self.tech_import()
    self.data_import()

  def append_file(self,input_file):

    self.append = True
    self.input_file = input_file
    self.sh = shelve.open( input_file )
    self.info = self.sh['__info__']
    self.ks = [k for k in self.sh.keys() if k[0] != '_']

    self.tech_import()
    self.data_import()
    self.files.append( input_file )

  def tech_import(self):

      this = self.sh['__tech__'].copy()
      finfo = this['file_info']
      finfo['fill_value'] = float( finfo['fill_value'] )
      finfo['shape'] = tuple( [int(x) for x in finfo['shape']] )
      if 'time_intervals' in finfo:
        finfo['time_intervals'] = tuple( [float(x) for x in finfo['time_intervals'] ] )
      this['file_info'] = finfo

      self.tech[self.fname] = this


#################################################
  def gather_basic(self):
      """Consolidate results of scan to get max, min etc over the a full variable;
      NB ... does not yet deal with levels
      """

      self.gathered = True
      ks = sorted( list( self.data.keys() ) )
      basic = [ self.data[k]['basic'] for k in ks]
      masks_ok = [ self.data[k].get('mask_ok',None) for k in ks]
      fraction = [ self.data[k].get('fraction',None) for k in ks]
      data_min = min( [x[0] for x in basic] )
      data_max = max( [x[1] for x in basic] )
      data_ma_min = min( [x[2] for x in basic] )
      data_ma_max = max( [x[2] for x in basic] )
      self.range_comment = 'Data range: %s to %s; mean absolute range %s to %s' % (data_min,data_max,data_ma_min,data_ma_max)
      nfv = sum( [x[3] for x in basic] )

      drl = [data_min,data_max,data_ma_min,data_ma_max]
      ksx  = {x:x.rpartition(':')[-1] for x in ks}
      if all( [x.find('-') != -1 for  k,x in ksx.items()] ):
          ksi = {x:[int(y) for y in v.split('-')] for x,v in ksx.items()}
          basic0 = [ self.data[k]['basic'] for k,v in ksi.items() if v[1] == 0]
          data_min_l0 = min( [x[0] for x in basic0] )
          data_max_l0 = max( [x[1] for x in basic0] )
          drl += [data_min_l0,data_max_l0]
          self.range_comment = 'Data range: %s to %s (l0: %s to %s); mean absolute range %s to %s' % (data_min,data_max,data_min_l0,data_max_l0,data_ma_min,data_ma_max)
      else:
          ksi = {x:int(v) for x,v in ksx.items()}

      ## fraction report
      if all( [x == None for x in fraction] ):
        self.fraction_report = ['no report',None,None,None,None]
      else:
        cmt = set( [f[0] for f in fraction])
        min1 = min( [f[1] for f in fraction] )
        max1 = max( [f[1] for f in fraction] )
        min2 = min( [f[3] for f in fraction] )
        max2 = max( [f[4] for f in fraction] )
        self.fraction_report = [sorted( list(cmt)),min1,max1,min2,max2]

      self.mask_comment = ''
      if all( [x == None for x in masks_ok] ):
        self.mask_check = None
        self.mask_comment = 'No mask report'
      elif all( [x[0] == 'masks_match' for x in masks_ok] ):
        self.mask_check = True
        s1 = set( [x[1] for x in masks_ok] )
        assert len(s1) == 1, 'Unexpected variation in mask ....'
        n1 = s1.pop()
        self.mask_comment = 'Mask count = %s' % n1
      else:
        self.mask_check = False
      print ("MASK COMMENT: ",self.mask_comment, ' - check: ', self.mask_check )
      print (self.range_comment)
      self.gathered_dict = dict( drl=drl, mask_comment=self.mask_comment, mask_check=self.mask_check, 
                    fraction_report=self.fraction_report, range_comment=self.range_comment )
      ##for k,i in self.gathered_dict.items():
        ##print (k,type(i),i)

      self.basic = (drl,nfv)
      return (drl,nfv)


  def data_import(self):
    if not self.append:
      self.data = {}

    for k in self.ks:
      SKIPPED = []
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
          self.SKIPPED.append( k1 )

      if len(SKIPPED) != 0:
        this['SKIPPED'] = SKIPPED
        print('SKIPPED RECORDS: %s' % SKIPPED ) 

      self.data[k] = this

  def json_dump(self,json_file='test.json'):
    data = dict( info=self.info, tech=self.tech, data=self.data )

    if self.gathered:
      data['gathered'] = self.gathered_dict
      ##print ( self.gathered_dict )

    if len( self.files ) > 1:
      data['files'] = self.files

    oo = open( json_file, 'w' )
    json.dump( {'header':'Dump of results from %s' % self.input_file, 'results':data }, oo, indent=4, sort_keys=True )
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
  if len(sys.argv) == 3:
    k,v = sys.argv[1:]
    if k == '-f':
      print ("Test run of ShToJson")
      input_file = v
      json_file = '%s.json' % input_file
      s = ShToJson( input_file )
      tt = s.gather_basic( )
      s.json_dump( json_file )
      print (tt)
    elif k == '-c':
      print ("Test run of ShToJson over collection")
      input_file_stem = v
      json_file = '%s.json' % input_file_stem
      files = [f[:-4] for f in sorted( list( glob.glob( '%s*.dat' % input_file_stem ) ) ) ]
      s = ShToJson( files[0] )
      for input_file in files[1:]:
        s.append_file( input_file )
      print ( "ingested %s files" % len(files) )
      tt = s.gather_basic( )
      s.json_dump( json_file )
      print ( 'Dumped to %s' % json_file )
      print (tt)

