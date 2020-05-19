import urllib.request
import json, collections, os


ex1 = "http://esgf-index1.ceda.ac.uk/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&activity_id=CMIP&experiment_id=piControl&project%21=input4mips&variant_label=r1i1p1f2&table_id=fx&mip_era=CMIP6&facets=mip_era%2Cactivity_id%2Cmodel_cohort%2Cproduct%2Csource_id%2Cinstitution_id%2Csource_type%2Cnominal_resolution%2Cexperiment_id%2Csub_experiment_id%2Cvariant_label%2Cgrid_label%2Ctable_id%2Cfrequency%2Crealm%2Cvariable_id%2Ccf_standard_name%2Cdata_node&format=application%2Fsolr%2Bjson"
ex1 = "http://esgf-index1.ceda.ac.uk/esg-search/search/?offset=0&limit=500&type=Dataset&replica=false&latest=true&project%21=input4mips&activity_id=CMIP&table_id=fx&mip_era=CMIP6&experiment_id=piControl&facets=mip_era%2Cactivity_id%2Cmodel_cohort%2Cproduct%2Csource_id%2Cinstitution_id%2Csource_type%2Cnominal_resolution%2Cexperiment_id%2Csub_experiment_id%2Cvariant_label%2Cgrid_label%2Ctable_id%2Cfrequency%2Crealm%2Cvariable_id%2Ccf_standard_name%2Cdata_node&format=application%2Fsolr%2Bjson"

ex2 = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/MPI-M/MPI-ESM1-2-LR/historical/r1i1p1f1/fx/areacella/gn/v20190710/areacella_fx_MPI-ESM1-2-LR_historical_r1i1p1f1_gn.nc"

temp2 = "http://%{node}s.de/thredds/fileServer/cmip6/CMIP/%{institute_id}s/%{source_id}s/%{experiment_id}s/%{variant_id}s/%{table_id}s/%{var}s/%{grid_id}s/%{version}s/%(file_name}s"

ex3 = "areacella_fx_MPI-ESM1-2-LR_historical_r1i1p1f1_gn.nc"

ex4 = "CMIP6.CMIP.MPI-M.MPI-ESM1-2-LR.historical.r1i1p1f1.fx.areacella.gn"
ex4 = "CMIP6.CMIP.MPI-M.MPI-ESM1-2-LR.historical.r1i1p1f1.fx.areacella.gn.v20190710|esgf3.dkrz.de"

DRS_dict = collections.namedtuple( "DRS", ["era", "activity_id", "institute_id", "source_id", "experiment_id", "variant_id", "table_id", "var", "grid_id", "version"] )

fntemplate = "%(var)s_%(table_id)s_%(source_id)s_%(experiment_id)s_%(variant_id)s_%(grid_id)s.nc"
dtemplate = "http://esgf3.dkrz.de/thredds/fileServer/cmip6/CMIP/%(institute_id)s/%(source_id)s/%(experiment_id)s/%(variant_id)s/%(table_id)s/%(var)s/%(grid_id)s/%(version)s/"

def get_drs(datasetid):
  ls = datasetid.split("|")[0].split("." )
  return DRS_dict( *ls )

class ESGF_Query(object):

  def __init__(self,query=ex1,resp=None):
    with urllib.request.urlopen(query) as response:
       self.json_string = response.read()

    self.js = json.loads( self.json_string )
    self.resp = self.js["response"]
    self.docs = self.resp["docs"]
    self.drs_dict = dict()

  def get_drs(self):
    for doc in self.docs:
      datasetid = doc["id"]
      drs = get_drs( datasetid )
      print ( datasetid, drs )
      self.drs_dict[datasetid] = drs

  def get_file(self):
    for k,drs in self.drs_dict.items():
       fn = fntemplate % drs._asdict()
       base = dtemplate % drs._asdict()
       cmd = "wget -nH -O %(odir)s/%(fn)s %(base)s/%(fn)s" % {"fn":fn, "base":base, "odir":"data_files_2"}
       os.popen( cmd ).read()

eq = ESGF_Query()
eq.get_drs()
eq.get_file()
