import json, collections, os, glob, sys
import local_utilities as lu

BASE_DIR = '/badc/cmip6/data/'

##`CMIP/E3SM-Project/E3SM-1-1-ECA/piControl/r1i1p1f1/Lmon/mrsos/gr/v20191218/mrsos_Lmon_E3SM-1-1-ECA_piControl_r1i1p1f1_gr_195001-195912.nc

TEMPLATE = '%(base)s/%(era)s/%(mip)s/%(inst)s/%(model)s/%(expt)s/%(variant)s/%(table)s/%(var)s/%(grid)s/%(version)s/'

class Rprep( object ):
    def __init__(self,with_limits=True, group=1):
        ee01 = json.load( open( 'data/c3s34g_variables.json', 'r' ) )
        req = ee01['requested']
        sreq = set()
        for t,l in req.items():
          for v in l:
            sreq.add( '%s.%s' % (t,v) )
        jfile = "handle_scan_report_20201019.json"
        ee = json.load( open( 'data/%s' % jfile, 'r' ) )
        ff = dict()
        nf1 = 0
        nf2 = 0
        np2 = 0
        lims = lu.get_new_ranges()
        kkkk = 0
        print( sreq )
        print ( len( ee['results'].keys() ) )
        ##sys.exit(0)
        for h in ee['results'].keys():
            print (kkkk,h)
            d = ee['results'][h]
            kkkk += 1
            if d['qc_status'] == 'pass' or d['dataset_qc']['error_severity'] != 'major':
              ds = d['dset_id']
              this = dict( dset_id=ds )
              era,mip,inst,model,expt,variant,table,var,grid,version = ds.split('.')
              ##if '%s.%s' % (table,var) in sreq and mip == 'CMIP':
              if True:
                base=BASE_DIR
                p1 = TEMPLATE % locals()
                if not os.path.isdir( p1 ):
                    ## print ('NOT FOUND: %s' % p1 )
                    nf1 += 1
                    if nf1 == 5000:
                       sys.exit(0)
                    this['qc_status'] = 'ERROR'
                    this['qc_message'] = 'Dataset not present at STFC'
                else:
                    fl = glob.glob( '%s/*.nc' % p1 )
                    if len( fl ) == 0:
                      this['qc_status'] = 'ERROR'
                      this['qc_message'] = 'Dataset at STFC empty'
                    else:
                      this['qc_status'] = 'pass'
                      this['files'] = [x.rpartition('/')[-1] for x in sorted( list( fl) )] 
                      this['dir'] = p1
                if this['qc_status'] == 'pass' and with_limits:
                   var_id = '%s.%s' % (table,var)
                   if var_id not in lims:
                      this['qc_status'] = 'ERROR'
                      this['qc_message'] = 'No variable limits provided'

                if this['qc_status'] != 'pass':
                 ##  print (ds,this['qc_status'])
                   nf2 += 1
                else:
                   np2 += 1
                ff[h] = this

        print( np2, nf2, nf1 )
        oo = open( 'scanned_dset_for_qc_%2.2i.json' % group, 'w' )
        json.dump( {'info':{"title":"List of Scanned Datasets and their Files"}, 'data':ff}, oo, indent=4, sort_keys=True )
        oo.close()

class Rsplat(object):
  def __init__(self,group=1):
     self.group=group
     jfile = "handle_scan_report_extended_20201019.json"
     jfile = 'scanned_dset_for_qc_%2.2i.json' % group
     ee = json.load( open( jfile, 'r' ) )
     cc = collections.defaultdict( list )
     ff = collections.defaultdict( list )
     __all__ = True
     for h,d in ee['data'].items():
       ds = d['dset_id']
       era,mip,inst,model,expt,variant,table,var,grid,version = ds.split('.')
       if d['qc_status'] == 'pass' or (__all__ and d['qc_status'] != 'ERROR'):
         cc[(expt,table,var)].append( d )
       elif d['qc_message'] == 'No variable limits provided':
           ff[(table,var)].append(ds)
     self.cc = cc
     self.ff = ff

  def analysis(self):
      ks = sorted( list( self.ff.keys() ), key=lambda x:len( self.ff[x] ) )
      for k in ks[-20:]:
          print( k,len( self.ff[k] ) )
      print( len(ks) )

  def splat(self):
     cc = self.cc

     for k,item in cc.items():
       d0 = 'inputs_%2.2i/%s' %  (self.group,k[0])
       if not os.path.isdir(d0):
         os.mkdir( d0 )
       oo = open( 'inputs_%2.2i/%s/x1_%s_%s.txt' % (self.group,*k), 'w' )
       for d in item:
         d1 = d['dir']
         for f in d['files']:
           oo.write( '%s/%s\n' % (d1,f) )
       oo.close()
       

if __name__ == '__main__':
    ##rp = Rprep(with_limits=False, group=3)
    r = Rsplat(group=3)
    r.splat()
    r.analysis()
