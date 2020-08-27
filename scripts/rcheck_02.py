import json, collections, os, sys
import local_utilities


class Review(object):
    def __init__(self,idir='json_agg_02'):
        assert os.path.isdir(idir)
        self.dir = idir
        self.ranges = local_utilities.get_new_ranges()
        self.hdls = Hdls()
        self.hdls_raw = Hdls_raw()

    def review(self,ifile):
        if os.path.isfile(ifile):
            file = ifile
        elif os.path.isfile( '%s/%s' % (self.dir,ifile) ):
            file = '%s/%s' % (self.dir,ifile)
        else:
            assert False, 'File not found: %s' % ifile

        ee = json.load( open( file, 'r' ) )
        var,tab = file.rpartition( '/' )[-1].rpartition( '.' )[0].split('_')[:2]

        data = ee['data']
        ks = []
        for k in sorted( list( data.keys() ) ):
          kk = k.rpartition( '.' )[0]
          if k.find( 'AWI-CM-1-1-MR' ) == -1:
            cce = collections.defaultdict(set)
            ks.append(k)
            this = data[k]
            cons = this['consol']
            tech = this['tech']
            if type(tech) == type( [] ):
                tech = tech[-1]
            print ( kk, cons['basic'], cons['fraction_report'] )
            if '%s.%s' % (tab,var) in self.ranges:
              this = self.ranges['%s.%s' % (tab,var)]
              mn_error = this.min.status != 'NONE' and cons['basic'][0] < this.min.value
              cce[mn_error].add( 'Min %s >= %s' % (cons['basic'][0],this.min.value) )
              mx_error = this.max.status != 'NONE' and cons['basic'][1] > this.max.value
              cce[mn_error].add( 'Max %s <= %s' % (cons['basic'][2],this.max.value) )
              if any( [mn_error, mx_error] ):
                print (mn_error, mx_error, cce[True] )
                contact = tech['file_info']['contact']
                hdl = self.hdls.key02_lookup(kk)
                if hdl == None:
                  hdl = self.hdls_raw.key02_lookup(kk)
                  if hdl == None:
                    print( 'ERROR:: in un-prioritised data .....', contact )
                  else:
                      print( 'ERROR**:: %s :' % contact, hdl )

                else:
                  h,item = hdl

                  print( 'ERROR:: %s :' % contact, h,item['dset_id'],item.get('qc_message','OK') )


        mn = min( [data[k]['consol']['basic'][0] for k in ks] )
        mx = max( [data[k]['consol']['basic'][1] for k in ks] )
        mna = min( [data[k]['consol']['basic'][2] for k in ks] )
        mxa = max( [data[k]['consol']['basic'][3] for k in ks] )
        print (ifile,mn, mx, mna, mxa)

class Hdls(dict):
    def __init__(self,input_file='data/handle_scan_report_20200710.json'):
      ii = open( input_file, 'r' )
      ee = json.load( ii )
              ##"hdl:21.14100/000cce7f-69c7-333f-8c46-07825bc73cf3": {
            ##"dset_id": "CMIP6.CMIP.CAS.FGOALS-f3-L.piControl.r1i1p1f1.Omon.thetao.gn.v20191028",
            ##"error_level": 2,
            ##"qc_message": "mask_error",
            ##"qc_status": "ERROR"

      for h,item in ee['results'].items():
          id = item['dset_id']
          era,mip,inst,model,expt,ense,table,var,grid,version = id.split( '.' )
          k2 = '.'.join( [ model,expt,ense,table,var,grid ] )
          self[k2] = (h,item)

    def key02_lookup(self,key,invalid_key_return=None):
        try:
          var,table,model,expt,ense,grid = key.split( '_')                
          k2 = '.'.join( [ model,expt,ense,table,var,grid ] )
        except:
          print (key )
          raise
        return self.get(k2,invalid_key_return)

class Hdls_obs(dict):
    def __init__(self,input_file='hdl-reviewed_datasets.csv'):
      ii = open( input_file, 'r' )
      for l in ii.readlines():
          hdl,id,version = l.split('\t')[:3]
    ##CMIP6.CMIP.E3SM-Project.E3SM-1-1-ECA.piControl.r1i1p1f1.Lmon.mrso.gr
          era,mip,inst,model,expt,ense,table,var,grid = id.split( '.' )
          k2 = '.'.join( [ model,expt,ense,table,var,grid ] )
          self[k2] = (hdl,id,version,( model,expt,ense,table,var,grid ))

    def key02_lookup(self,key,invalid_key_return=None):
        try:
          var,table,model,expt,ense,grid = key.split( '_')                
          k2 = '.'.join( [ model,expt,ense,table,var,grid ] )
        except:
          print (key )
          raise
        return self.get(k2,invalid_key_return)

class Hdls_raw(dict):
    def __init__(self,input_file='../esgf_fetch/lists/wg1subset-r1-datasets-pids-clean.csv'):
      ii = open( input_file, 'r' )
      for l in ii.readlines()[1:]:
          try:
            id,hdl = l.strip().split(',')
          except:
              print(l)
              raise
          ##CMIP6.CMIP.NOAA-GFDL.GFDL-CM4.historical.r1i1p1f1.Omon.fgco2.gr.v20180701
    ##CMIP6.CMIP.E3SM-Project.E3SM-1-1-ECA.piControl.r1i1p1f1.Lmon.mrso.gr
          try:
            era,mip,inst,model,expt,ense,table,var,grid,version = id.split( '.' )
          except:
              print(l)
              print(id)
              raise
          k2 = '.'.join( [ model,expt,ense,table,var,grid ] )
          self[k2] = (hdl,id,version,( model,expt,ense,table,var,grid ))

    def key02_lookup(self,key,invalid_key_return=None):
        try:
          var,table,model,expt,ense,grid = key.split( '_')                
          k2 = '.'.join( [ model,expt,ense,table,var,grid ] )
        except:
          print (key )
          raise
        return self.get(k2,invalid_key_return)


if __name__ == '__main__':
    import sys
    r = Review()
    r.review( sys.argv[1] )
