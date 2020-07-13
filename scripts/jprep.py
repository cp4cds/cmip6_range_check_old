
import csv, json, time


class Jprep(object):
    def __init__(self):
        refile = '../esgf_fetch/lists/wg1subset-r1-datasets-pids-clean.csv'
        review = 'summary-reviewed_datasets_%s.csv'
        nbad = 0

        self.ref = dict()
        ii = open( refile ).readlines()
        for record in csv.reader( ii[1:], delimiter=',' ):
            if len(record) != 2:
                print ('BAD REF FILE RECORD: ',record)
                nbad +=1
            else:
                dsidv, hdl = record
                self.ref[dsidv] = hdl
        assert nbad == 0
        print ( len(self.ref) )

        self.aa = dict()
        self.aa_oflow = dict()
        for tab in ['Amon','Lmon','day','other']:
            f = review % tab
            self.scan1(f)

    def scan1(self,f):            

        nbad = 0
        ii = open( f ).readlines()
        for record in csv.reader( ii, delimiter='\t' ):
            if len(record) != 5:
                print ('BAD RECORD: ',record)
                nbad +=1
            else:
                dsid, version, f1, f2, mask = record
                dsidv = '%s.%s' % (dsid, version)
                if dsidv in self.ref:
                    h = self.ref[dsidv]
                    self.aa[h] = ((f1=='OK') and (f2=='OK'), dsid,version,f1,f2,mask)
                else:
                    self.aa_oflow[(dsid,version)] = ((f1=='OK') and (f2=='OK'), f1,f2,mask)

        print ( f, len(self.aa), len( [ x for x,v in self.aa.items() if v[0] ] ), len(self.aa_oflow) )
        assert nbad == 0
        self.jdump()



    def jdump(self,jfile='handle_scan_report_%s.json'):

        title = 'Handle Record QC Report (draft, Amon, Lmon day tables)'
        abstract = 'Results from a review of handle records, provided as a dictionary for each handle identifier. Error level 0 indicates no errors found. The report also includes a check on the availability of mask files '
        date = '%4.4i%2.2i%2.2i' % time.gmtime()[:3]
        jf = jfile % date
        ee = {}
        ee2 = {}
        for h,r in self.aa.items():
            dsidv = '%s.%s' % r[1:3]
            if r[0]:
                this = {'qc_status':'pass', 'error_level':0, 'dset_id':dsidv}
            else:
                f1,f2 = r[3:5]
                msg = ''
                if f1 != 'OK':
                    msg = f1
                if f2 != 'OK':
                    if msg != '':
                        msg += '; '
                    msg += f2
                this = {'qc_status':'ERROR', 'error_level':2, 'dset_id':dsidv, 'qc_message':msg}
            that = this.copy()
            if that['error_level'] == 0 and r[5] != 'na':
               that['mask']= r[5]
               print (that['mask'])
            ee[h] = this
            ee2[h] = that
            
        n = len(ee)
        nf = len( [h for h,e in ee.items() if e['error_level'] == 0] )
        summary = '%s records, %s passed, %s failed' % (n,nf,n-nf)
        print (summary)
        info = dict( source='jprep.py', history='Created at CEDA, based on a scan of handle records',
                  title = title, abstract=abstract, summary=summary,
                  inputs='(1) wg1subset-r1-datasets-pids-clean.csv: list of ESGF datasets, (2) filtered to MIP=CMIP or ScenarioMIP, table = Amon or Lmon',
                  creation_date=time.ctime(),
                  contact='support@ceda.ac.uk (ref C3S 34g,Martin Juckes)' )


        oo = open( jf, 'w' )
        json.dump( {'header':info, 'results':ee}, oo, indent=4, sort_keys=True )
        oo.close()
        jf = jfile % ('extended_%s' % date )
        oo = open( jf, 'w' )
        json.dump( {'header':info, 'results':ee2}, oo, indent=4, sort_keys=True )
        oo.close()


if __name__ == "__main__":
    j = Jprep()
