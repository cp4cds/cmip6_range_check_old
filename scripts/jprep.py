
import csv, json, time

ds_pass_msg = dict( error_severity='na', error_message='No handle registry errors detected' )

input_dataset_list = 'c3s34g_pids_qcTest_Oct2020.txt'
major_error_codes = {'ERROR.ds.0900'}
minor_error_codes = {'ERROR.ds.0040'}

class Jprep(object):
    def __init__(self, version='02-01'):
        refile_june = '../esgf_fetch/lists/wg1subset-r1-datasets-pids-clean.csv'
        refile = "../esgf_fetch/lists/%s" % input_dataset_list
        review = 'summary-reviewed_datasets_%s_%s.csv'
        nbad = 0

        self.ref = dict()
        ii = open( refile ).readlines()
        for record in csv.reader( ii[1:], delimiter=',' ):
            if len(record) != 2:
                print ('BAD REF FILE RECORD: ',record)
                nbad +=1
            else:
                dsidv, hdl = record
                self.ref[dsidv.strip()] = hdl.strip()
        assert nbad == 0
        print ( len(self.ref) )

        self.aa = dict()
        self.aa_oflow = dict()
        for tab in ['Amon','Lmon','day','Omon','other']:
            f = review % (tab, version)
            print ( 'TABLE - START: %s, len dict: %s' % (tab, len(self.aa) ) )
            self.scan1(f)
            print ( 'TABLE: %s, len dict: %s' % (tab, len(self.aa) ) )
        self.jdump()

    def scan1(self,f):            
        nbad = 0
        ii = open( f ).readlines()
        for record in csv.reader( ii, delimiter='\t' ):
            if len(record) != 5:
                print ('BAD RECORD: ',record)
                nbad +=1
            else:
                dsid, version, f1, f2, mask = record
                dsidv = '%s.%s' % (dsid.strip(), version)
                if dsidv in self.ref:
                    h = self.ref[dsidv]
                    self.aa[h] = ((f1=='OK') and (f2=='OK'), dsid,version,f1,f2,mask)
                else:
                    print( 'WARN.scan.002: dataset not found: ',dsidv)
                    self.aa_oflow[(dsid,version)] = ((f1=='OK') and (f2=='OK'), f1,f2,mask)

        print ( 'INFO.scan.001:', f, len(self.aa), len( [ x for x,v in self.aa.items() if v[0] ] ), len(self.aa_oflow) )
        assert nbad == 0

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
                this = {'qc_status':'pass', 'dset_id':dsidv, 'dataset_qc':ds_pass_msg}
            else:
                eseverity='unknown'
                f1,f2 = r[3:5]
                msg = ''
                if f1 != 'OK':
                    msg = f1
                    ecode = msg.split(':')[0]
                    ecat = 'Handle Registry'
                    if ecode in major_error_codes:
                        eseverity='major'
                    elif ecode in minor_error_codes:
                        eseverity='minor'
                if f2 != 'OK':
                    if msg != '':
                        msg += '; '
                    msg += f2
                    ecat = 'Mask Availability'
                this = {'qc_status':'fail', 'dset_id':dsidv, 
                        'dataset_qc':dict( error_message=msg, error_severity=eseverity, error_category=ecat, error_code=ecode ) }
            that = this.copy()
            if that['qc_status'] == 'pass' and r[5] != 'na':
               that['mask']= r[5]
               print (that['mask'])
            ee[h] = this
            ee2[h] = that
            
        n = len(ee)
        npass = len( [h for h,e in ee.items() if e['qc_status'] == 'pass'] )
        summary = '%s records, %s passed, %s failed' % (n,npass,n-npass)
        print (summary)
        info = dict( source='jprep.py', history='Created at CEDA, based on a scan of handle records',
                  title = title, abstract=abstract, summary=summary,
                  inputs='(1) %s: list of ESGF datasets, (2) filtered to MIP=CMIP or ScenarioMIP, table = Amon or Lmon' % input_dataset_list,
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
