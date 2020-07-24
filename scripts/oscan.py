import glob, collections, sys, json, os, time, datetime

__version__ = 1.0

class Oscan(object):
  def __init__(self,idir='Amon.evspsbl'):
    self.idir = idir
    self.fl = sorted( list( glob.glob( 'out_01/%s/*' % idir ) ) )
    self.cc = collections.defaultdict( list )
    for f in self.fl:
      fname = f.rpartition( '/' )[-1]
      fds,x,tt = fname.rpartition( '_' )
      self.cc[fds].append( f )


    print( 'Files: %s, datasets: %s' % (len(self.fl), len(self.cc) ) )

  def scan(self,force=False):
    jfile = 'out_01/json/%s.json' % self.idir
    reftime = -1
    if not force and os.path.isfile( jfile ):
      reftime = os.stat( jfile ).st_mtime
      ee = json.load( open( jfile ) )
    else: 
      ee = dict()

    for ds in sorted( list( self.cc.keys() ) ):
      nf = 0
      nu = 0
      for p in self.cc[ds]:
        if force or reftime < 0 or os.stat(p).st_mtime > reftime:
          nu += 1
          for l in open(p).readlines():
            if l[:4] == 'FAIL':
              nf += 1
      if nu > 0:
        if nf > 0:
          ee[ds] = {'qc_status':'ERROR', 'qc_message':nf }
        else:
          ee[ds] = {'qc_status':'pass', 'qc_message':nf }
      else:
        if ds in ee:
          nf = ee[ds].get( 'qc_message', '??' )
        else:
          nf = None
      print ('%s: %s' % (ds,nf) )
    oo = open( jfile, 'w' )
    json.dump( ee, oo, indent=4, sort_keys=True )
    oo.close()

def isotimenow():
  dt = datetime.datetime( 2020, 1, 1)
  return dt.now().isoformat()

def fecho(fp, msg=''):
  t0 = os.stat( fp ).st_mtime
  dt = datetime.datetime( *list( time.gmtime( t0 ) )[:6] )
  return (fp, dt.isoformat(), msg )

# "CMIP6.CMIP.CAS.FGOALS-f3-L.piControl.r1i1p1f1.Omon.thetao.gn.v20191028"
# tas_Amon_AWI-CM-1-1-MR_abrupt-4xCO2_r1i1p1f1_gn
class Osummary( object ):
  def __init__(self):
    fl = glob.glob( 'out_01/json/*.json' )
    n1 = len(fl)
    cc = collections.defaultdict(int)
    cc2 = collections.defaultdict(int)
    data01 = {}
    for f in fl:
      this = json.load( open( f ) )
      for k,item in this.items():
        cc[ item['qc_status'] ] += 1
        data01[k] = item
    self.cc = cc
    print ( cc )

    hh = json.load( open( 'data/handle_scan_report_20200710.json' ) )
    dd = hh['results']
    for h,item in dd.items():
      ds = item['dset_id']
      era,mip,inst,model,expt,variant,table,var,grid,version = ds.split('.')
      targ = '_'.join( [var,table,model,expt,variant,grid] )
      if item['qc_status'] == 'pass':
        if targ not in data01:
          item['qc_status'] = 'ERROR'
          item['error_level'] = 1
          item['qc_message'] = 'Range checks not run'
        else:
          this = data01[targ]
          item['qc_status'] = this['qc_status']
          if this['qc_status'] == 'pass':
            item['qc_message'] = 'Range checks OK'
          else:
            item['qc_message'] = 'Range check errors: %s' % this['qc_message']
            item['error_level'] = 2
        dd[h] = item
      else:
        if item['qc_message'] == 'mask_error':
          item['qc_message'] = 'Mask file absent or has issue raised'
      cc2[ item['qc_message'] ] += 1


    description="""The range checks are carried out by the test_cmip6_file.py script, which generates a short text file report for each CMIP6 file checked.
             These results are then aggregated and translated into json files, with one file for each CMIP6 variable (e.g. Amon.tas, Omon.sos). The final script
             combines these with the output from the handle scan to create a single json file."""

    tech = dict( dependencies_data=[fecho( 'data/new_limits.csv', 'Prescribed data ranges' ),
                                    fecho( 'data/handle_scan_report_20200710.json', 'Results of checks on handle records' ) ],
                 dependencies_code=[fecho( 'test_cmip_file.py', 'Check ranges and masks' ),
                                    fecho( 'local_utilities.py', 'Scan data files' )] )

    info = dict( title="Aggregated Results of CMIP6 Range Checks", source="cmip6_range_checks/scripts/oscan.py", time=isotimenow(), 
                 description=description, script_version=__version__, tech=tech)

    print(cc2)
    with open( 'data/range_check_report_version1-0.json', 'w' ) as oo:
      json.dump( {'header':info, 'results':dd}, oo, indent=4, sort_keys=True  )

if __name__ == "__main__":
  idir='Amon.evspsbl'
  if len( sys.argv ) <= 2:
    if len( sys.argv ) == 2:
      idir = sys.argv[1]
    o = Oscan(idir=idir)
    o.scan()
  else:
    if sys.argv[1] == '-s':
      mode = sys.argv[2]
    
      o = Osummary()
