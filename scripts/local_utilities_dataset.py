import logging, time, os, collections, json, inspect, glob, warnings, numpy, shelve, re, os
import csv
from local_pytest_utils import BaseClassTS
from generic_utils import LogFactory
try:
  import hddump
except:
  print ("FAILED TO IMPORT hddump")

__version__ = '0.1.0'
pid_input_june = "../esgf_fetch/lists/wg1subset-r1-datasets-pids-clean.csv"
pid_input_oct = "../esgf_fetch/lists/c3s34g_pids_qcTest_Oct2020.txt"

NT__scope = collections.namedtuple( 'scope', ['overview','identifier','description','priority','traceability'] )
NT__test_case_spec = collections.namedtuple( 'test_case_spec', ['ov', 'id', 'obj', 'p', 'tr', 'prec', 'i', 'expected'])

NT_RangeValue = collections.namedtuple( "range_value", ["value","status"] )
NT_RangeSet = collections.namedtuple( "range_set", ["max","min","ma_max","ma_min"] )
null_range_value = NT_RangeValue( None, "NONE" )

__overview__ = "Testing the local utilities module"
__identifier__ = "scope01"
__description__ = """Test of local utilities module, local_utilities.py, which contains functions and classes used in other modules"""
__priority__ = "MUST"
__traceability__ = "documentation is tbd"
test_scope = NT__scope( overview = __overview__, priority=__priority__,identifier=__identifier__, description=__description__, traceability=__traceability__)


def matching( result, expected):
    if type(expected) == type('') and expected.find(':') != -1 and expected.split( ':' )[0] in ['lt','gt','le','ge']:
        exp = eval( expected[3:] )
        op = expected[:2]
        assert op in ['lt','gt','le','ge']
        return operator.__dict__[ op ](result,exp)
    else:
        return result == expected


def get_quantiles_and_summary(ddk):
     this = ddk["percentiles"]
     thissum = ddk["summary"]

     isDict = type(this) == type( {} )
     if isDict:
       this = this["0"]

     isDict = type(thissum) == type( {} )
     if isDict:
       thissum = thissum["0"]
     return this, thissum



class TCBuild(BaseClassTS):
    """
    BaseClassTS: brings in a standard report function which assumes a spec attribute which is an instance of NT__scope
    """
    scope = test_scope
    def __init__(self, function ):
      ret = function.__annotations__['return']
      if type(ret) == type(dict()):
        self.spec = NT__test_case_spec( **ret )
      elif isinstance(ret,NT__test_case_spec):
        self.spec = ret

      self.function = function
      expected = self.spec.expected
      if type(expected) == type('') and expected.find( 'regex:' ) == 0:
         self.conformance_mode = 'match'
      else:
         self.conformance_mode = 'equals'

      self.ov = self.spec.ov

    def __call__(self,*args,**kwargs):
        self.result = self.function(*args,**kwargs)
        return self.result

    def conforms( self, result ):
      self.result = result
      if self.conformance_mode == 'equals':
          return self.equals( )

    def equals(self):
        self.fail_msg = 'Result [%s] does not match expected [%s]' % (self.result, self.spec.expected)
        return self.result == self.spec.expected

def maketest(f):
    def this(*args,**kwargs) -> TCBuild(f):
        result = f(*args,**kwargs)
        this.__annotations__['result'] = result
        if not hasattr(this.__annotations__['return'], "spec" ):
                warnings.warn("Test-case function lacks specification of expected: %s" % f.__name__,UserWarning)
        expected = this.__annotations__['return'].spec.expected
        assert matching(result, expected), 'Result [%s] does not match expected [%s]' % (result,expected)

    return this


def get_mask( table, var, source,expt,grid):
          import netCDF4, numpy
          this_mask = None
          if table in ['fx','Ofx']:
              fp = '%s_%s_%s_%s*_%s.nc' % (var,table,source,expt,grid)
              fcands = glob.glob( '../esgf_fetch/data_files/%s' % fp )
              if len( fcands ) == 0:
                   print ('ERROR: maskfile matching %s not found' % fp )
              else:
                mask_file_path = fcands[0]
                ncm = netCDF4.Dataset( mask_file_path, 'r' )
                vm = ncm.variables[var]
                if var in ['sftlf','sftof','sftif']:
                     this = numpy.ma.masked_equal( vm, 0. )
                     this_mask = this.mask
          else:
              print ( "NOT READY FOR THIS YET ... varying mask" )
          return this_mask


class SampleReturn(object):
    pass

def get_sample_from_mode(mode,nt,maxnt):
      if mode == 'firstTimeValue':
        nt1 = min( [12,nt] )
        isamp = range(nt1)

      elif mode == 'sampled' and nt > 20:
        isamp = sorted( random.sample( range(nt), 20 ) )
        
      elif (mode in ['sampledonepercent','sampledtenpercent','sampledoneperthou']) and nt > 20:
        nsamp = nt//{'sampledonepercent':100, 'sampledtenpercent':10, 'sampledoneperthou':1000}[mode]
        isamp = sorted( random.sample( range(nt), nsamp ) )
        if len( isamp ) == 0:
          isamp = [0,]

      elif maxnt > 0 and maxnt < nt:
        isamp = range(maxnt)

      else:
        isamp = range(nt)

      return isamp

re2 = re.compile( '<location(.*?)/>' )
re_href = re.compile( '%s="(.*?)"' % 'href' )


class DatasetReview(object):
    def __init__(self,dsid):
        self.id = dsid
        self.current_mask_file=None
        self.current_mask_error=None
        self.obsolete = None
        self.errors = []


class CMIPDatasetSample(object):
    def __init__(self, id_mode='hdl', drs_base='/badc/cmip6/data/CMIP6/'):
        self.id_mode = id_mode
        self.drs_base = drs_base
        self.ar6 = WGIPriority()
        self.ar6.review_masks()

    def review(self, dsids, ctag):
        self.nobs = 0
        self.kk = 0
        oo = open('hdl-reviewed_datasets_%s.csv' % ctag,'w')
        oo2 = open('summary-reviewed_datasets_%s.csv' % ctag,'w')
        for ds, eid, ev in dsids:
            self.dsr = DatasetReview(ds)
            h = hddump.Open( ds )
            drs_id, err = self.review_handle_record(oo, h, ds, eid, ev )
            self.review_masks(drs_id)

            eflag = 'OK' if err == None else err
            mflag = 'OK' if self.dsr.current_mask_error == None else 'mask_error'
            mcmt = self.dsr.current_mask_file if self.dsr.current_mask_error == None else self.dsr.current_mask_error
            oo2.write( '\t'.join( [drs_id,ev,eflag,mflag,mcmt] ) + '\n' )

        oo.close()
        oo2.close()

        print ('%s reviewed, %s obsolete' % (len(dsids),self.nobs))

    def review_masks(self, drs_id):
        era,activity,inst,model,expt,variant,table,var,grid = drs_id.split('.')
        var_id = '%s.%s' % (table,var)
        this_mask = self.ar6.masks.get(var_id, '' )
        if this_mask == '':
            self.dsr.current_mask_file='na'
        elif this_mask not in self.ar6.mask_pool:
            self.dsr.current_mask_file='not recognised: %s' % this_mask
            self.dsr.current_mask_error = 'not recognised'
        else:
            this = self.ar6.mask_pool[this_mask]
            if model not in this:
                print ( 'ERROR: %s has no mask %s' % (model, var_id) )
                self.dsr.current_mask_error = 'model misses required mask' 
            else:
                ss = [f for f in this[model] if '_' + grid in f]
                if len(ss) == 0:
                    print ( 'ERROR: %s has no mask in required grid (%s) : %s' % (model, grid, var_id) )
                    self.dsr.current_mask_error = 'model misses required mask at specified grid' 
                else:
                    self.dsr.current_mask_file = ss.pop()

    def review_handle_record(self,oo, h, ds, eid, ev):
            h.get()
            drs_id = h.rec['DRS_ID']
            era,activity,inst,model,expt,variant,table,var,grid = drs_id.split('.')
            fncomps = [var,table,model,expt,variant,grid]
            err = None
            ## CMIP6.CMIP.AS-RCEC.TaiESM1.historical.r1i1p1f1.Lmon.mrso.gn
            ## http://esgdata.gfdl.noaa.gov/thredds/fileServer/gfdl_dataroot4/OMIP/NOAA-GFDL/GFDL-OM4p5B/omip1/r1i1p1f1/Omon/volcello/gn/v20180701/volcello_Omon_GFDL-OM4p5B_omip1_r1i1p1f1_gn_180801-182712.nc
            if h.obsolete:
                print ( 'ERROR.ds.0900: %s: ds %s is obsolete [%s]' % (self.kk,ds,h.rec['DRS_ID']) )
                oo.write( '\t'.join( [ds,drs_id,ev,'OBSOLETE'] ) + '\n' )
                self.nobs += 1
                err = 'ERROR.ds.0900: Dataset obsolete: %s' % ds
                self.obsolete = True
            else:
                self.obsolete = False
                err = None
                vns = set()
                fns = set()
                cc = collections.defaultdict( set  )
                ccl = collections.defaultdict( set  )
                for f in h.rec['HAS_PARTS']:
                  f.get()
                  if 'URL_ORIGINAL_DATA' not in f.rec:
                        print ('ERROR.ds.0040: URL_ORIGINAL_DATA missing from file hdl record %s :: %s' % (drs_id,f.rec.get('URL','__NO__URL__')))
                        err = 'ERROR.ds.0040: URL_ORIGINAL_DATA missing from file hdl record: %s' % ds
                        self.dsr.errors.append( err )
                  else:    
                    this = f.rec['URL_ORIGINAL_DATA']
                    locs = re2.findall( this )
                    vnss = set()
                    fnss = set()
                    for loc in locs:
                      href = re_href.findall( loc )[0]
                      vn,fn = href.split( '/' )[-2:]
                      vnss.add(vn)
                      fnss.add(fn)
                    if len( fnss ) != 1:
                       print ('ERROR.ds.0030: multiple files in file record: (%s) %s' % (fnss,f.rec['URL']) )
                       err = 'ERROR.ds.0030: %s: multiple files in file record' % ds
                       self.dsr.errors.append( err )
                    fn = fnss.pop()
                    if ev not in vnss:
                       print ('ERROR.ds.0020: expected version not in file record original data: (%s) %s' % (vnss,f.rec['URL']) )
                       err = 'ERROR.ds.0020: %s: expected version not in file record original data' % ds
                       self.dsr.errors.append( err )
                       vn = vnss.pop()
                    else:
                       vn = ev
                    tt = fn.rpartition('.')[0].split('_')
                    cc['l'].add( len(tt) )
                    ccl[len(tt)].add( fn )
                    for k in range(len(tt)):
                        cc[k].add(tt[k])
                    vns.add(vn)
                    fns.add(fn)

                if len(cc.keys()) == 0:
                    print ('ERROR.ds.0101: no files found (empty cc) %s' % (drs_id) )
                    if err == None:
                        err = 'ERROR.ds.0101: %s: no files found (empty cc)' % ds
                        self.dsr.errors.append( err )
                elif len(cc['l']) == 0:
                    print ('ERROR.ds.0901: empty cc["l"] %s' % (drs_id) )
                    if err == None:
                        err = 'ERROR.ds.0901: %s: empty cc["l"]' % ds
                        self.dsr.errors.append( err )
                else:
                  eblock = False
                  if len(cc['l']) > 1:
                    print ('ERROR.ds.0001: Too many file naming patterns in dataset: (%s) %s' % (fns,drs_id) )
                    l0 = min( list(ccl.keys()), key=lambda x: len(ccl[x]) )
                    print ('ERROR.ds.0001.01: %s: %s' % (l0,ccl[l0]) )
                    err = 'ERROR.ds.0001: %s: Too many file naming patterns in dataset' % ds
                    self.dsr.errors.append( err )
                    eblock = True

                  if len(vns) != 1:
                    print ('ERROR.ds.0002: Too many versions in dataset: (%s) %s' % (vns,drs_id) )
                    err = 'ERROR.ds.0002: %s: Too many versions in dataset' % ds
                    self.dsr.errors.append( err )

                  if ev not in vns:
                    print( 'ERROR.ds.0002b: version inconsistency: %s - %s : %s' % (ev,vns,drs_id) )
                    err = 'ERROR.ds.0002b: %s: version inconsistency' % ds
                    self.dsr.errors.append( err )
                  version = ev

              
                  if not eblock:
                    l = cc['l'].pop()
                    is_fixed =  table in ['Ofx','fx']
                    if not is_fixed:
                      l += -1

                    for k in range(l):
                      if len(cc[k]) != 1:
                        print ('ERROR.ds.0003: Too many elements at %s in file name: (%s) %s' % (k,cc[k],drs_id) )
                        err = 'ERROR.ds.0003: Too many elements at %s in file name' % k
                        self.dsr.errors.append( err )

                    for k in range(l):
                      this = cc[k].pop()
                      if k > len(fncomps) -1 :
                        print ('ERROR.ds.0005: file name element inconsistency [%s]: (%s) %s' % (this,fns,drs_id) )
                        err = 'ERROR.ds.0005: file name element inconsistency'
                        self.dsr.errors.append( err )
                      elif this != fncomps[k]:
                        print ('ERROR.ds.0004: file name element inconsistency [%s]: (%s) %s' % (this,fns,drs_id) )
                        err = 'ERROR.ds.0004: file name element inconsistency'
                        self.dsr.errors.append( err )

                if err != None:
                  oo.write( '\t'.join( [ds,drs_id,ev,err] ) + '\n' )
                elif is_fixed:
                  oo.write( '\t'.join( [ds,drs_id,ev,'OK',] ) + '\n' )
                else:
                  oo.write( '\t'.join( [ds,drs_id,ev,'OK',str(len(fns)),str(sorted(list(cc[l]))) ] ) + '\n' )

            self.kk += 1
            return (drs_id,err)

class CMIPFileSample(object):
    def __init__(self,files,input_dir=None,mode='all',sh_file=None):
        ##
        ## TODO : add check on files, loop over files, extraction of variable and call to VariableSampler
        ##
        if type(files) == type(''):
            files = [files,]
        if input_dir != None:
            assert os.path.isdir( input_dir ), 'Input directory not found: %s' % input_dir
            if input_dir[-1] == '/':
                input_dir = input_dir[:-1]
            files = ['%s/%s' % (input_dir, f) for f in files]
        self.files = sorted( files )

    def get_samples(self,sampler,var_name_mode='CMIP'):
        """
        Sample a list of files
        """
        assert var_name_mode == 'CMIP', 'Currently only supporting one variable name identification mode: CMIP'
        self.samples = {}
        for data_path in self.files:
            fn = data_path.rpartition('/')[-1]
            if var_name_mode == 'CMIP':
               var_name = fn.split( '_' )[0]

            nc = netCDF4.Dataset( data_path )
            this_var = nc.variables[vname]
            if hasattr( this_var, '_FillValue' ):
              fill_value = this_var._FillValue
            else:
              fill_value = None
            print ("fill value = %s" % fill_value )
            vs = VariableSampler( this_var[:], sampler, fill_value=fill_value )
            vs.scan()
        return (vs, this_var, nc )



class VariableSampler(object):
    def __init__(self,var,sampler,mode='all',with_time=True,ref_mask=None,fill_value=None,maxnt=10000,ref_mask_file=None):
        """
          var : numpy array object
          sampler : Sampler instance
        """
        assert isinstance( var, numpy.ndarray), 'Expected instance of numpy.ndarray, got %s' % type( var )

        self.var = var
        self.ref_mask = ref_mask
        self.ref_mask_file = ref_mask_file
        self.fill_value = fill_value
        self.maxnt = maxnt
        self.sampler = sampler
        self.rank = len(var.shape)
        self.mode = mode
        self.with_time = with_time
        self.sr_dict = dict()

    def dump_shelve(self,sname,kprefx,mode='c',context=None):

        ### might be better to move this up to calling object .....

        tech = {'extremes':self.sampler.nextremes, 'quantiles':self.sampler.quantiles, 'with_time':self.with_time, 'fill_value':float(self.fill_value), 'shape':self.var.shape }
        info = {"title":"Scanning set of data files", "source":"local_utilities.VariableSampler", "time":time.ctime(), "script_version":__version__}
        if context != None:
            info['context'] = context
        if self.ref_mask != None:
            if self.ref_mask_file != None:
                tech['ref_mask_file'] = self.ref_mask_file
            else:
                tech['ref_mask_file'] = 'UNKNOWN'
        sh = shelve.open( sname, flag=mode )
        sh['__tech__'] = tech
        sh['__info__'] = info
        l1 = len( str( self.kmax ) )
        l2 = len( str( self.klmax ) )
        fmt1 = '%s:%' + '%si' % l1
        fmt2 = '%s:%' + ( '%si' % l2 ) + '-' + '%si' % l2
        for k,rec in self.sr_dict.items():
            if type(k) == type( 'x' ):
                ko = k
            elif type(k) == type( 1 ):
                ko = fmt1 % (kprefx,k)
            elif type(k) == type( () ):
                ko = fmt2 % (kprefx,k[0],k[1])
            sh[ko] = rec
        sh.close()

    def scan(self,isamp=None):


        self.kmax = 0
        self.klmax = 0
        kl = set()
        kl2 = set()
        if self.rank == 2:
            self.sampler.load( self.var, fill_value=self.fill_value, ref_mask=self.ref_mask )
            self.sampler.apply(  )
            self.sr = self.sampler.sr

        else:
            if isamp == None:
                isamp = get_sample_from_mode( self.mode, self.var.shape[0], self.maxnt )
            if self.rank == 3:
              for k in isamp:
                self.sampler.load( self.var[k,:], fill_value=self.fill_value, ref_mask=self.ref_mask)
                self.sampler.apply( )
                self.sr_dict[k] = self.sampler.sr
                kl.add(k)
            elif self.rank == 4:
              for k in isamp:
                  kl2.add(k)
                  for l in range(self.var.shape[1] ):
                     kl2.add(l)
                     self.sampler.load( self.var[k,l,:], fill_value=self.fill_value, ref_mask=self.ref_mask)
                     self.sampler.apply( )
                     self.sr_dict[(k,l)] = self.sampler.sr
        if len(kl) > 0:
          self.kmax = max( kl )
        if len(kl2) > 0:
          self.klmax = max( kl2 )

class XXXSampler(object):
    def __init__(self,extremes=0,quantiles=None):
        import numpy 

        self.nextremes=extremes
        self.quantiles=quantiles
        self.q = quantiles != None
        self.ext = extremes > 0

    def load(self,array,fill_value=None,ref_mask=None):
        self.ref_mask=ref_mask
        self.fill_value=fill_value

        self.has_fv = fill_value != None

        self.has_msk = type( self.ref_mask ) != type( None )
        if self.has_msk:
            assert hasattr( self.ref_mask, 'mask' )

        if self.has_fv:
            self.get_basic = self._get_basic_ma
            self.array = numpy.ma.masked_equal( array, fill_value )

            if self.ext or self.q:
                self.farray = self.array.ravel().compressed()
        else:
            self.get_basic = self._get_basic
            self.array=array
            if self.ext or self.q:
                self.farray = self.array.ravel()

    def apply(self,as_dict=True):
        if as_dict:
          self.sr = dict()
          self.sr['basic'] = self.get_basic()
          if self.q: self.sr['quantiles'] = self.get_quantiles()
          if self.ext: self.sr['extremes'] = self.get_extremes()
          if self.has_msk: self.sr['mask_ok'] = self.check_mask()
        else:
          self.sr = SampleReturn()
          self.sr.basic = self.get_basic()
          if self.q: self.sr.quantiles = self.get_quantiles()
          if self.ext: self.sr.extremes = self.get_extremes()
          if self.has_msk: self.sr.mask_ok = self.check_mask()

    def check_mask(self):
        import numpy

        n1 = self.ref_mask.count()
        if not hasattr( self.array, 'mask' ):
            self.mask_rep = ('no_mask_defined',n1,0,0,0,0)
        elif not self.array.shape == self.ref_mask.shape:
            self.mask_rep = ('mask_has_wrong_shape',n1,self.ref_mask.shape,self.array.shape,0,0)
        elif numpy.array_equal( self.ref_mask.mask, self.array.mask):
            self.mask_rep = ('masks_match',n1,n1,n1,0,0)
        else:
            n1 = self.ref_mask.count()
            n2 = self.array.count()
            c0 = numpy.count_nonzero( ~self.ref_mask.mask & ~self.array.mask )
            c1 = numpy.count_nonzero( ~self.ref_mask.mask & self.array.mask )
            c2 = numpy.count_nonzero( self.ref_mask.mask & ~self.array.mask )
            self.mask_rep = ('mask_mismatch',n1,n2,c0,c1,c2)
        return self.mask_rep[0]

    def _get_basic_ma(self):
        """Return min, max, mean absolute value and number of filled values for masked array"""
        import numpy
        basic = (numpy.ma.min( self.array ),
                 numpy.ma.max( self.array ),
                 numpy.ma.mean( numpy.ma.abs( self.array ) ),
                 self.array.size - self.array.count() )
        return basic

    def _get_basic(self):
        """Return min, max, mean absolute value and number of filled values for unmasked array"""
        basic = (numpy.min( self.array ),
                 numpy.max( self.array ),
                 numpy.mean( numpy.abs( self.array ) ),
                 0 )
        return basic

    def get_quantiles(self):
        """Return quantiles specified in self.quantiles.
           Array is first flattened and then stripped of missing values"""
        import numpy
        return numpy.quantile( self.farray, self.quantiles ).tolist()

    def get_extremes(self):
        """
        For a masked array, the negation has to be conditional .. or perhaps done before the ravel ...
        Passing "-x" to argpartition results in fillValues being identifed as extreme data, as numpy.partition is not
        recognising the mask.
        """
        import numpy

        # ravel to flatten.
        # masked set to large positive ....
        if self.has_fv:
            x = numpy.where( self.array.mask, 1.e20, self.array ).ravel()
            xm = numpy.where( self.array.mask, 1.e20, -self.array ).ravel()
        else:
            x = self.farray
            xm = -x

        if len(x) > 0:
            if self.nextremes > 0:
              flat_indices_min = numpy.argpartition(x, self.nextremes-1)[:self.nextremes]
              flat_indices_max = numpy.argpartition(xm, self.nextremes-1)[:self.nextremes]

              row_indices_min, col_indices_min = numpy.unravel_index(flat_indices_min, self.array.shape)
              min_elements = self.array[row_indices_min, col_indices_min]

              row_indices_max, col_indices_max = numpy.unravel_index(flat_indices_max, self.array.shape)
              max_elements = self.array[row_indices_max, col_indices_max]

              self.extremes = ((row_indices_min.tolist(), col_indices_min.tolist(), min_elements.tolist()),
                               (row_indices_max.tolist(), col_indices_max.tolist(), max_elements.tolist()) )
              return self.extremes


class Dq(object):
  def __init__(self):
    from dreqPy import dreq
    self.dq = dreq.loadDreq()

    self.CMORvar_by_id = dict()
    for i in self.dq.coll["CMORvar"].items:
      self.CMORvar_by_id["%s.%s" % (i.mipTable,i.label) ] = i

def stn(x,nd=2):
  if type(x) in [type(''),type( u'')]:
    return x

  ax = abs(x)
  if ax > 1. and ax < 1000.:
    vv = '%7.1f' % x
  elif ax > 0.01 and ax < 1.0001:
    vv = '%7.4f' % x
  else:
    vv = '%9.2e' % x
    if len(vv) > 7 and vv[-8:] == '0.00e+00':
      vv = '0.0'
  return vv

class WGIPriority(object):
  known_masks = ['fx.sftlf', 'Ofx.sftof', 'Simon.siconc', 'fx.sftgif']
  def __init__(self,ifile="AR6_priority_variables_02.csv" ):
    ii = csv.reader( open( ifile ), delimiter='\t' )
    try:
      dq = Dq()
    except:
      dq = None

    self.ee = dict()
    self.title = dict()
    self.ranges = dict()
    self.masks = dict()
    for l in ii:
      rec = l[2:]
      id, units = rec[:2]
      if dq != None:
        self.title[id] = dq.CMORvar_by_id[id].title
      vt = rec[3:11]
      if rec[2].strip() != '':
          self.masks[id] = rec[1].strip()

      if not all( [vt[i] == "-" for i in [1,3,5,7]]):
        xx = []
        for i in [0,2,4,6]:
          if vt[i+1] not in ["-",""]:
            xx.append( NT_RangeValue(float(vt[i]),vt[i+1]) )
          else:
            xx.append( null_range_value )
        self.ranges[id] = NT_RangeSet( xx[0], xx[1], xx[2], xx[3] )

      self.ee[id] = units

  @staticmethod
  def _has_mask(fpath):
      fn = fpath.rpartition( '/')[-1]
      var,tab = fn.split('_')[:2]
      return '%s.%s' % (tab,var) in self.known_masks

  def review_masks(self,data_dir='../esgf_fetch/data_files_2/'):
      fl = [f for f in glob.glob( '%s/*.nc' ) if self._has_mask(f) and os.stat(f).st_size > 100]
      fl = glob.glob( '%s/*.nc' % data_dir )
      print ('mask review ... ',len(fl) )
      self.mask_pool = collections.defaultdict( lambda: collections.defaultdict( set ) )

      for fpath in fl:
          fn = fpath.rpartition( '/')[-1]
          var,tab,model = fn.split('_')[:3]
          var_id = '%s.%s' % (tab,var)
          if var_id in self.known_masks:
              self.mask_pool[var_id][model].add( fpath )

def range_merge(a, b):
    this = list( a )

    for k in range(4):
      if this[k] == null_range_value and b[k] != null_range_value:
        this[k] = b[k]
    return NT_RangeSet( this[0], this[1], this[2], this[3] )


def get_new_ranges( input_json="data/new_limits.json", input_csv = "data/new_limits.csv", merge=True ):
    ee = json.load( open( input_json, "r" ) )
    new_data = ee['data']
    ii = open( input_csv, "r", encoding = "ISO-8859-1" )
    for l in csv.reader( ii.readlines()[1:] ):
      ##words = l.strip().split('\t')
      words = l
      if len(words) >3:
        tab,var,directive = [x.strip() for x in words[:3]]
        directive = directive.lower()
        if directive != '':
          id = "%s.%s" % (tab,var)
          print (directive, id)
          if directive[:5] == "valid":
            this = new_data.get( id, {"ranges":{}} )
            if words[3] != '':
              this["ranges"]["max"] = NT_RangeValue(float( words[3] ), words[6] )
            if words[4] != '':
              this["ranges"]["min"] = NT_RangeValue(float( words[4] ), words[6] )
            new_data[id] = this
          elif directive[:4] == "mean":
            this = new_data.get( id, {"ranges":{}} )
            if words[3] != '':
              this["ranges"]["ma_max"] = NT_RangeValue(float( words[3] ), words[6] )
            if words[4] != '':
              this["ranges"]["ma_min"] = NT_RangeValue(float( words[4] ), words[6] )
            new_data[id] = this

    if merge:
        ar6 = WGIPriority()
        md = ar6.ranges
        for id in md:
            if id in new_data:
                ntr = NT_RangeSet( *[new_data[id]["ranges"].get(x,null_range_value) for x in ['max','min','ma_max','ma_min']] )
                new_data[id] = range_merge( md[id], ntr  )
            else:
                new_data[id] = md[id]

        for id in new_data.keys():
            if id not in md:
                ntr = NT_RangeSet( *[new_data[id]["ranges"].get(x,null_range_value) for x in ['max','min','ma_max','ma_min']] )
                new_data[id] = ntr
            
    return new_data

class CheckJson(object):
  def __init__(self):
    self.new = json.load( open( "data/new_limits.json", "r" ) )
    self.new_modified = set()
    self.pid_lookup = dict()
    self.known_errors = collections.defaultdict( set )

    for fn in ['datasets_with_checksum_errs.txt', 'datasets_with_missing_files.txt', 'master_issues.txt']:
      ii = open( 'data/%s' % fn )
      for l in ii.readlines():
          this = l.strip()
          if this != '':
              self.known_errors[this].add( fn )
      ii.close()
    
    ii = open( pid_input_oct, 'r' )
    for l in ii.readlines()[1:]:
       esgf_id,pid = [x.strip() for x in l.split(',') ]
       self.pid_lookup[esgf_id] = pid

    ii = open( "data/new_limits.csv", "r", encoding = "ISO-8859-1" )
    nd = self.new["data"]
    for l in csv.reader( ii.readlines()[1:] ):
      ##words = l.strip().split('\t')
      words = l
      if len(words) >3:
        tab,var,directive = [x.strip() for x in words[:3]]
        directive = directive.lower()
        if directive != '':
          id = "%s.%s" % (tab,var)
          print ('xxx012: ',directive, id)
          if directive[:5] == "valid":
            this = self.new["data"].get( id, {"ranges":{}} )
            if words[3] != '':
              this["ranges"]["max"] = (float( words[3] ), words[6] )
            if words[4] != '':
              this["ranges"]["min"] = (float( words[4] ), words[6] )
            self.new["data"][id] = this
          elif directive[:4] == "mean":
            this = self.new["data"].get( id, {"ranges":{}} )
            if words[3] != '':
              this["ranges"]["ma_max"] = (float( words[3] ), words[6] )
            if words[4] != '':
              this["ranges"]["ma_min"] = (float( words[4] ), words[6] )
            nd[id] = this
    self.new["data"] = nd
    ii.close()

  def range_merge(self, a, b):
    this = list( a )
    
    for k in range(4):
      if this[k] == null_range_value and b[k] != null_range_value:
        this[k] = b[k]
    return NT_RangeSet( this[0], this[1], this[2], this[3] )

  def get_range(self,varid):
    xx = []
    this = self.new["data"][varid]["ranges"]
    for k in ["max","min","ma_max","ma_min"]:
      if k in this:
        xx.append( NT_RangeValue( this[k][0], this[k][1] ) )
      else:
        xx.append( null_range_value )
    return NT_RangeSet( xx[0], xx[1], xx[2], xx[3] )

  def set_range(self,varid, max=None, min=None, ma_max=None, ma_min=None ):
    """set a new range value or values in local instance"""
    self.sig = inspect.signature( self.set_range )
    ee = dict()
    args = list( self.sig.parameters.keys() )
    for k in args[1:]:
      val = locals()[k]
      if val != None:
        if type(val) == type( () ):
          ee[k] = val
        elif type(val) in [type( 1. ),type( 1 )]:
          ee[k] = (val,"provisional")
        else:
          print ('xxx002: ',"value for arg %s not recognised" % k )
          raise

    if varid in self.new["data"]:
      this = self.new["data"][varid]
      this["ranges"]
      for k in prev:
        if k not in ee:
          ee[k] = prev[k]
      this["ranges"] = ee
      hist = this["history"]
      hist.append( "Record updates %s" % time.ctime() )
      this["history"] = this
    else:
      this = {"ranges":ee, "history":"Record created %s" % time.ctime() }

    self.new["data"][varid] = this
    if len( ee.keys() ) > 0:
      self.new_modified.add( varid )
     
   
  def __call__(self, table,ipath=None,var=None,verbose=True):
    if ipath == None:
      assert var !=None, "check_json: either ipath or var must be set"
      ipath = "json_ranges/%s/%s_historical_consol-var.json" % (table,var)

    assert os.path.isfile( ipath ), "check_json: file %s not found" % ipath

    ifile = ipath.rpartition("/")[-1]
    var = ifile.split("_")[0]
    wg1 =  WGIPriority()
    varid = "%s.%s" % (table,var)
    if verbose: print( 'xxx003: ',"check_json",table, ipath, varid )
    ee = json.load( open( ipath, "r" ) )
    data = ee["data"]
    percentiles = ee["info"]["tech"]["percentiles"]
    models = sorted( list( data.keys() ) )
    p0 = data[models[0]]["percentiles"]
    isDict = type(p0) == type( {} )

    if len(percentiles) == 13:
  ## "This code assumes 13 percentiles"
      if isDict:
        pmx = [max( [data[m]["percentiles"]["0"][j] for m in models] ) for j in range(len(percentiles)) ]
        pmn = [min( [data[m]["percentiles"]["0"][j] for m in models] ) for j in range(len(percentiles)) ]
      else:
        pmx = [max( [data[m]["percentiles"][j] for m in models] ) for j in range(len(percentiles)) ]
        pmn = [min( [data[m]["percentiles"][j] for m in models] ) for j in range(len(percentiles)) ]
      pctcomp = [pmx[i+1] < pmn[i] for i in range(4,8) ] 
      if verbose:
        print ( 'xxx004: ',pctcomp, pmx[5:9], pmn[4:8] )
        print ("pmx", pmx)
        print ("pmn", pmn)
      clean = all( pctcomp )
      if clean:
        distmsg = "COMPACT DISTRIBUTION"
      else:
        distmsg =  "overlapping distributions"
      if verbose:
          print ('info.check.005: %s' % distmsg)
    else:
      distmsg =  "__na__"
    agg_this = dict()

    hh = ["Q(%s)" % stn(x) for x in percentiles[::-1]]
    table_records = [ ["Model","Minimum"] + hh + ["Maximum",],
                     [ " :--",  ] + [" :--: ", ]*( len(percentiles) + 2 ) ]

    metam = dict()
    for m in sorted( list( data.keys() ) ):
        errs = []
        minfo = data[m]["model_info"]
        table,var,inst,model,expt,variant_id,grid_id,version = minfo["drs"]
        ##CMIP6.OMIP.NOAA-GFDL.GFDL-OM4p5B.omip1.r1i1p1f1.Omon.volcello.gn.v20180701
        if expt != "historical":
            print ("need to add some code here ...")
            raise
        esgf_ds_id = "CMIP6.CMIP.%s.%s.%s.%s.%s.%s.%s.%s" % (inst,model,expt,variant_id,table,var,grid_id,version)
        pid = self.pid_lookup.get(esgf_ds_id,'__not_found__')
        contact = ";".join( minfo["contact"] )
        known_error = self.known_errors.get( esgf_ds_id, 'none')
        metam[m] = (esgf_ds_id, pid, contact, known_error)
        this, this_sum = get_quantiles_and_summary( data[m] )
        ##if isDict:
          ##this = data[m]["summary"]["0"]
        ##else:
          ##this = data[m]["summary"]
        agg_this[m] = this_sum

        tr0 = [m,this_sum[2]] + this[::-1] + [this_sum[1]]
        table_records.append( [stn(x) for x in tr0 ] )

    if varid not in wg1.ranges and varid not in self.new["data"]:
      if verbose:
        print ( "No range information for %s" % varid )
      rangemsg = "No Range Set"
    else:
      if varid in self.new["data"]:
        ranges = self.get_range( varid )
        if varid in wg1.ranges:
          ranges = self.range_merge( ranges, wg1.ranges[varid] )
      else:
        ranges = wg1.ranges[varid]
      rsum = dict()
      for m in sorted( list( data.keys() ) ):
        this = agg_this[m]
        
        range_error_max = (ranges.max != null_range_value) and this[1] > float(ranges.max.value)
        range_error_min = (ranges.min != null_range_value) and this[2] < float(ranges.min.value)
        errs = []
        try:
          range_error_ma_max = (ranges.ma_max != null_range_value) and this[3] > float(ranges.ma_max.value)
        except:
          print ('xxx006: ',ranges.ma_max)
          raise
        try:
          range_error_ma_min = (ranges.ma_min != null_range_value) and this[4] < float(ranges.ma_min.value)
        except:
          print ('xxx007: ',ranges.ma_min)
          raise

        if not any( [range_error_max,range_error_min, range_error_ma_max, range_error_ma_min] ):
           res = (True,"OK")
        else:
          if verbose:
              print('xxx008: ', m, [range_error_max,range_error_min, range_error_ma_max, range_error_ma_min] )

          for k in range(4):
            if [range_error_max,range_error_min, range_error_ma_max, range_error_ma_min][k]:
              elab = ["Max","Min","MA Max","MA Min"][k]
              ##targ = [float(ranges.max.value), float(ranges.min.value), float(ranges.ma_max.value), float(ranges.ma_min.value)][k]
              targ = [ranges.max.value, ranges.min.value, ranges.ma_max.value, ranges.ma_min.value][k]
              msg = "%s: %s -- %s" % (elab, this[k+1], targ)
              errs.append( msg)
          res = (False,"; ".join( errs ))
              
        if verbose:
            print ('xxx009: ',"%s:: %s/%s" % (m,res,errs) )
        rsum[m] = res

      bad = [k for k,v in rsum.items() if not v[0]]
      if verbose:
        for k in bad:
            print ('xxx010: ',"ERROR: %s:: %s" % (k,rsum[k][1]) )
        print ('xxx011: ',"Targets:", [ranges.max.value, ranges.min.value, ranges.ma_max.value, ranges.ma_min.value] )
      if len( bad) == 0:
         rangemsg = "All models in range"
      else:
         rangemsg = "Range errors: %s [of %s]" % (len(bad),len(rsum.keys()))
         oo = open( "test.md", 'w')
         oo.write( "ERROR SUMMARY\n=============\n\n" )
         for m in sorted( list( rsum.keys() ) ):
            if not rsum[m][0]:
                esgf_ds_id, pid, contact, known = metam[m]
                pid_link = "[%s](http://hdl.handle.net/%s)" % (pid,pid[4:])
                oo.write( '%s :: %s\n' % (m,contact) )
                if known != 'none':
                    oo.write( 'Known errors: see %s\n' % known )
                oo.write( '%s\n' % rsum[m][1] )
                oo.write( '%s -- %s\n\n' % (esgf_ds_id,pid_link) )
         oo.close()

    image_dir = "images/%s" % table
    oo = open( '%s/Overview_%s.md' % (image_dir,var), "w" )
    for record in table_records:
       oo.write( ' | '.join( record ) + "\n" )
    oo.write( '\n\n' )
    for m in sorted( list( rsum.keys() ) ):
            esgf_ds_id, pid, contact, known = metam[m]
            if pid[:4] == 'hdl:':
              pid_link = "[%s](http://hdl.handle.net/%s)" % (pid,pid[4:])
            elif pid == '__not_found__':
              pid_link = '[DS PID not found]'
            else:
              pid_link = '["%s"?]' % pid
              
            oo.write( ' - %s :: %s\n' % (m.replace( '_', '\\_') ,contact) )
            if known != 'none':
                    oo.write( 'Known errors: see %s\n' % known )
            if not rsum[m][0]:
                oo.write( '  - %s\n' % rsum[m][1] )
            oo.write( '  - %s -- %s\n\n' % (esgf_ds_id,pid_link) )
    oo.close()

    if verbose:
        maxval = max( [x[1] for k,x in agg_this.items()] )
        minval = min( [x[2] for k,x in agg_this.items()] )
        ma_maxval = max( [x[3] for k,x in agg_this.items()] )
        ma_minval = min( [x[4] for k,x in agg_this.items()] )
        print ( "Actual: ",[maxval,minval,ma_maxval,ma_minval] )

    print (var,distmsg,rangemsg)


def run_dataset_review(repeat=False, mode='a'):
     dsl = []
     if repeat:
       if mode=='a':
         review_version = '01-02-a1'
         ii = open( '/home/mjuckes/Repositories/git/shared/c3s_34g_qc_results/QC_Results/passes.csv').readlines()
         this_table = 'other'
         for l in ii[1:]:
           h,i = [ x.strip() for x in l.split( '\t' )[:2] ]
           v = i.rpartition( '.' )[-1]
           dsl.append( (h,i,v) )
       else:
         review_version = '01-02-01'
         ii = open( 'hdl_rev/june/hdl-reviewed_datasets_Amon.csv').readlines()
         this_table = 'other'
         for l in ii[1:]:
           h,i,v,check = [ x.strip() for x in l.split( '\t' )[:4] ]
           if check != 'OK':
             dsl.append( (h,i,v) )
     else:

       review_version = '02-01'
       ii = open( pid_input_oct).readlines()
       set1 = ['Omon','Amon','Lmon','day']
       this_table = 'other'
       this_table = 'Amon'
       ne = 0
       for l in ii[1:]:
           esgf_id,h = [x.strip() for x in l.split(',')[:2]]
           #CMIP6.CMIP.NCC.NorESM2-LM.esm-hist.r1i1p1f1.Lmon.cSoilFast.gn
           ttt = esgf_id.split('.')
           if len(ttt) != 10:
               ne +=1 
               if ne < 100:
                   print( "run_dataset_review: unexpected length of dataset split: %s" % esgf_id )
           else:
             era, mip, inst, model, expt, variant, table, var, grid, version = ttt
             if mip in ['CMIP','ScenarioMIP'] and (table == this_table or (this_table == 'other' and table not in set1)):
               dsl.append( (h, '.'.join( [era, mip, inst, model, expt, variant, this_table, var, grid] ), version) )
       ###dsl = dsl[:100]

     
     print ("Reviewing %s datasets" % len(dsl) )

     dss = CMIPDatasetSample()
     dss.review(dsl,'%s_%s' % (this_table,review_version))

if __name__ == "__main__":
   mm = 'ds'
   if mm == 'ds':
     run_dataset_review()
   elif mm == 'ds2':
     run_dataset_review(repeat=True)
   else:
     check_json = CheckJson()
     wg1 = WGIPriority()
     print ( wg1.ranges.keys() )
     k = wg1.ranges.keys().pop()
     print ( k, wg1.ranges[k] )
