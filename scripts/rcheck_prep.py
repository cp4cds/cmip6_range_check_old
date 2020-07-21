import json, collections, os, glob, sys

BASE_DIR = '/badc/cmip6/data/'

##`CMIP/E3SM-Project/E3SM-1-1-ECA/piControl/r1i1p1f1/Lmon/mrsos/gr/v20191218/mrsos_Lmon_E3SM-1-1-ECA_piControl_r1i1p1f1_gr_195001-195912.nc

TEMPLATE = '%(base)s/%(era)s/%(mip)s/%(inst)s/%(model)s/%(expt)s/%(variant)s/%(table)s/%(var)s/%(grid)s/%(version)s/'

class Rprep( object ):
    def __init__(self):
        ee = json.load( open( 'data/handle_scan_report_20200710.json', 'r' ) )
        ff = dict()
        nf1 = 0
        for h,d in ee['results'].items():
            if d['qc_status'] == 'pass':
                ds = d['dset_id']
                this = dict( dset_id=ds )
                era,mip,inst,model,expt,variant,table,var,grid,version = ds.split('.')
                base=BASE_DIR
                p1 = TEMPLATE % locals()
                if not os.path.isdir( p1 ):
                    print ('NOT FOUND: %s' % p1 )
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
                if this['qc_status'] != 'pass':
                   print (ds,this['qc_status'])
                ff[h] = this
        oo = open( 'scanned_dset_for_qc.json', 'w' )
        json.dump( {'info':{"title":"List of Scanned Datasets and their Files"}, 'data':ff}, oo, indent=4, sort_keys=True )
        oo.close()

if __name__ == '__main__':
    r = Rprep()
