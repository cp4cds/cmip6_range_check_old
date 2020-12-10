import urllib.request
import json, collections, os, glob, csv
from dreqPy import dreq

template_001 = "http://esgf-index1.ceda.ac.uk/esg-search/search/?offset=%(offset)s&limit=10000&type=Dataset&replica=false&latest=true&activity_id=CMIP&source_id=%(source_id)s&mip_era=CMIP6&facets=mip_era%%2Cactivity_id%%2Cmodel_cohort%%2Cproduct%%2Csource_id%%2Cinstitution_id%%2Csource_type%%2Cnominal_resolution%%2Cexperiment_id%%2Csub_experiment_id%%2Cvariant_label%%2Cgrid_label%%2Ctable_id%%2Cfrequency%%2Crealm%%2Cvariable_id%%2Ccf_standard_name%%2Cdata_node&format=application%%2Fsolr%%2Bjson"
base_001 = "http://esgf-index1.ceda.ac.uk/esg-search/search/?offset=0&limit=50&type=Dataset&replica=false&latest=true&activity_id=CMIP&mip_era=CMIP6&facets=mip_era%2Cactivity_id%2Cmodel_cohort%2Cproduct%2Csource_id%2Cinstitution_id%2Csource_type%2Cnominal_resolution%2Cexperiment_id%2Csub_experiment_id%2Cvariant_label%2Cgrid_label%2Ctable_id%2Cfrequency%2Crealm%2Cvariable_id%2Ccf_standard_name%2Cdata_node&format=application%2Fsolr%2Bjson"

ex1 = "http://esgf-index1.ceda.ac.uk/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&activity_id=CMIP&experiment_id=piControl&project%21=input4mips&variant_label=r1i1p1f2&table_id=fx&mip_era=CMIP6&facets=mip_era%2Cactivity_id%2Cmodel_cohort%2Cproduct%2Csource_id%2Cinstitution_id%2Csource_type%2Cnominal_resolution%2Cexperiment_id%2Csub_experiment_id%2Cvariant_label%2Cgrid_label%2Ctable_id%2Cfrequency%2Crealm%2Cvariable_id%2Ccf_standard_name%2Cdata_node&format=application%2Fsolr%2Bjson"

ex1 = "http://esgf-index1.ceda.ac.uk/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&project%21=input4mips&activity_id=CMIP&table_id=fx&mip_era=CMIP6&variable_id=orog&facets=mip_era%2Cactivity_id%2Cmodel_cohort%2Cproduct%2Csource_id%2Cinstitution_id%2Csource_type%2Cnominal_resolution%2Cexperiment_id%2Csub_experiment_id%2Cvariant_label%2Cgrid_label%2Ctable_id%2Cfrequency%2Crealm%2Cvariable_id%2Ccf_standard_name%2Cdata_node&format=application%2Fsolr%2Bjson"


ex_tas = "http://esgf-index1.ceda.ac.uk/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&project%21=input4mips&activity_id=CMIP&table_id=Amon&mip_era=CMIP6&variable_id=tas&experiment_id=historical&facets=mip_era%2Cactivity_id%2Cmodel_cohort%2Cproduct%2Csource_id%2Cinstitution_id%2Csource_type%2Cnominal_resolution%2Cexperiment_id%2Csub_experiment_id%2Cvariant_label%2Cgrid_label%2Ctable_id%2Cfrequency%2Crealm%2Cvariable_id%2Ccf_standard_name%2Cdata_node&format=application%2Fsolr%2Bjson"

filters_tas = 'table_id=Amon&mip_era=CMIP6&variable_id=tas&experiment_id=historical'
tmpl_tas = "http://esgf-index1.ceda.ac.uk/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&project%%21=input4mips&activity_id=CMIP&%(filters)s&facets=mip_era%%2Cactivity_id%%2Cmodel_cohort%%2Cproduct%%2Csource_id%%2Cinstitution_id%%2Csource_type%%2Cnominal_resolution%%2Cexperiment_id%%2Csub_experiment_id%%2Cvariant_label%%2Cgrid_label%%2Ctable_id%%2Cfrequency%%2Crealm%%2Cvariable_id%%2Ccf_standard_name%%2Cdata_node&format=application%%2Fsolr%%2Bjson"

tmpl_isi = "https://esg.pik-potsdam.de/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&project=ISIMIP2b&facets=size%%2Cproduct%%2C%%2Cexperiment&format=application%%2Fsolr%%2Bjson"

ex2 = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r1i1p1f1/fx/areacella/gn/v20190710/areacella_fx_MPI-ESM1-2-LR_historical_r1i1p1f1_gn.nc"

temp2 = "http://%{node}s.de/thredds/fileServer/cmip6/CMIP/%{institute_id}s/%{source_id}s/%{experiment_id}s/%{variant_id}s/%{table_id}s/%{var}s/%{grid_id}s/%{version}s/%(file_name}s"

ex3 = "areacella_fx_MPI-ESM1-2-LR_historical_r1i1p1f1_gn.nc"

ex4 = "CMIP6.CMIP.MPI-M.MPI-ESM1-2-LR.historical.r1i1p1f1.fx.areacella.gn"
ex4 = "CMIP6.CMIP.MPI-M.MPI-ESM1-2-LR.historical.r1i1p1f1.fx.areacella.gn.v20190710|esgf3.dkrz.de"

DRS_dict = collections.namedtuple( "DRS", ["era", "activity_id", "institute_id", "source_id", "experiment_id", "variant_id", "table_id", "var", "grid_id", "version"] )

fntemplate = "%(var)s_%(table_id)s_%(source_id)s_%(experiment_id)s_%(variant_id)s_%(grid_id)s.nc"
dtemplate = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/%(institute_id)s/%(source_id)s/%(experiment_id)s/%(variant_id)s/%(table_id)s/%(var)s/%(grid_id)s/%(version)s/"
ttemplate = "http://%s/thredds/"
ddtemplate = "fileServer/cmip6/CMIP/%(institute_id)s/%(source_id)s/%(experiment_id)s/%(variant_id)s/%(table_id)s/%(var)s/%(grid_id)s/%(version)s/"

def get_drs(datasetid):
  ds0,x,node = datasetid.rpartition( '|' )
  ls = ds0.split("." )
  return (DRS_dict( *ls ),node)

class ParseDSList(object):
    def __init__(self,idir='o1'):
        self.fl = sorted( list( glob.glob( 'o1/scan_*.txt' ) ) )
        print( 'Manifests found: %s' % len(self.fl) )
        self.by_var = collections.defaultdict( set )
        self.by_model = collections.defaultdict( set )
        self.dq = None

    def parse(self):
        for f in self.fl:
            for l in open(f).readlines():
                drs,node = get_drs( l.strip() )
                self.by_model[ drs.source_id ].add( (drs.table_id,drs.var) )
                self.by_var[ (drs.table_id,drs.var) ].add( drs.source_id )

        ks = sorted( list( self.by_model.keys() ), key=lambda x:len(self.by_model[x]) )
        for k in ks:
            print (k,len(self.by_model[k]))

    def anal(self,dq=None):
        if dq != None:
            self.dq = dq
        if self.dq == None:
            self.dq = dreq.loadDreq()
        ifile = '../scripts/AR6_priority_variables_02.csv'
        ii = csv.reader( open( ifile ), delimiter='\t' )
        self.wg1_vars = set()
        for l in ii:
            self.wg1_vars.add( tuple( l[2].split('.' ) ) )
        self.priority_by_var = dict()
        cc0 = collections.defaultdict( int )
        for i in self.dq.coll['CMORvar'].items:
            v = self.dq.inx.uid[i.vid]
            tt = (i.mipTable,v.label)
            if tt in self.wg1_vars:
              p = 0
            else:
              p = i.defaultPriority 
            self.priority_by_var[ (i.mipTable,v.label) ] = p
            cc0[ p ] += 1
        ks = sorted( list( self.by_model.keys() ), key=lambda x:len(self.by_model[x]) )
        ks.reverse()
        oo = open( 'summary_by_model.csv', 'w' )
        for k in ks:
            cc = collections.defaultdict( int )
            l1 = len( self.by_model[k] )
            for v in self.by_model[k]:
                if v not in self.priority_by_var:
                    print( 'ERROR: not found: %s, %s' % (k,v) )
                    cc[ 999 ] += 1
                else:
                  cc[ self.priority_by_var[ v ] ] += 1
            print( '%32s:: %s  [%s -- %s -- %s -- %s] {%s}' % (k,l1,*[cc[k] for k in range(4)],cc[999]) )
            rec = [k, *[str(x) for x in [l1,cc[0],cc[1],cc[2],cc[3]] ], *[str( cc[k]/cc0[k] ) for k in [0,1,2,3]] ] 
            oo.write( '\t'.join( rec ) + '\n' )
        oo.close()

        oo = open( 'summary_by_var.csv', 'w' )
        ks = sorted( list( self.by_var.keys() ), key=lambda x:len(self.by_var[x]) )
        ks.reverse()
        for v in ks:
            cc = collections.defaultdict( int )
            if v not in self.priority_by_var:
                  p = -1
            else:
                  p = self.priority_by_var[ v ] 
            rec = [*v, str( len( self.by_var[v] ) ), str(p) ]
            oo.write( '\t'.join( rec ) + '\n' )
        oo.close()

class ESGF_Query(object):

  def __init__(self,query=ex1,resp=None, filters=None):

    if filters != None:
        if type (filters) == type(''):
            query=query % dict( filters=filters )
        else:
            query=query % dict( filters='&'.join( ['%s=%s' % (k,v) for k,v in filters.items()] ) )

    with urllib.request.urlopen(query) as response:
       self.json_string = response.read()

    print( len(self.json_string ) )
    print( self.json_string[:1000] )
    self.js = json.loads( self.json_string )
    self.resp = self.js["response"]
    self.docs = self.resp["docs"]
    self.drs_dict = dict()

  def get_drs(self, verbose=True):
    ss = 0
    for doc in self.docs:
      ss+= doc.get("size",0)
      datasetid = doc["id"]
      drs, node = get_drs( datasetid )
      if verbose:
        print ( datasetid, drs )
      self.drs_dict[datasetid] = (drs,node)
    print ("Size: %8.2fGB (%s)" % (ss*1.e-9,ss) )

  def get_file(self):
    for k,tt in self.drs_dict.items():
       drs,node = tt
       fn = fntemplate % drs._asdict()
       base = (ttemplate % node ) + (ddtemplate % drs._asdict() )
       ofile = "%(odir)s/%(fn)s" % {"fn":fn, "base":base, "odir":"data_files_orog"}
       if os.path.isfile( ofile ) and os.stat( ofile ).st_size > 10:
           pass
       else:
          cmd = "wget --tries=2 -nH -O %(odir)s/%(fn)s %(base)s/%(fn)s" % {"fn":fn, "base":base, "odir":"data_files_orog"}
          os.popen( cmd ).read()

class Scanner(object):
    def __init__(self,base=base_001,template=template_001,keys=['source_id']):
        self.base = base
        self.template = template
        self.base_obj = ESGF_Query(query=base)
        self.ee = dict()
        for k in keys:
            self.ee[k] = self.base_obj.js['facet_counts']['facet_fields'][k][::2]

    def scan(self):
        wcf0 = open( 'wc5000.txt' ).readlines()
        wfc1 = [x.strip().split()[-1].strip() for x in wcf0]
        wfc = [x.rpartition('.')[0].rpartition('_')[-1] for x in wfc1]
        wfc = ['CESM2-WACCM', 'MIROC-ES2L']
        print ( wfc )

        k0 = list( self.ee.keys() )[0]
        assert len( self.ee.keys() ) == 1, 'Not ready for greater than one key ....'
        ##for x in self.ee[k0]:
        for x in wfc:
          nf = 1
          nt = 0
          oo = open( 'scan_%s.txt' % x, 'a')
          kkk = 0
          while nt < nf and kkk < 10:
            kkk += 1
            q = self.template % { k0:x, "offset":nt }
            res = ESGF_Query(query=q )
            res.get_drs(verbose=False)
            n1 = len( res.drs_dict.keys()  )
            nf = res.resp['numFound']
            nt += n1
            print (k0,x,res.resp['numFound'],nt,nf)
            for d in sorted( list( res.drs_dict.keys() ) ):
                oo.write( d + '\n' )
          oo.close()

if __name__ == "__main__":
  eq = ESGF_Query(query=tmpl_tas, filters=filters_tas)
  eq.get_drs()
  ##eq.get_file()
