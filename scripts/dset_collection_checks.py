
import json, glob, collections


class CollectionCheck(object):
    def __init__(self):
        fl = glob.glob( 'handle_scan_report_*.json' )
        assert len(fl) > 0, 'No input data found'
        this_file = sorted( list( fl ) )[-1]

        self.input = json.load( open( this_file ) )

        assert 'results' in self.input, 'Do not understand input'

        self.results = self.input['results']

    def scan2(self):
        ks = [k for k,item in self.cc.items() if len (item.keys()) > 1]
        self.cc2 = collections.defaultdict( lambda: collections.defaultdict( dict ) )
        for k in ks:
            item = self.cc[k]
            for grid in item.keys():
                if grid == 'gm':
                    gcat = 'gm'
                elif grid[-1] == 'z':
                    gcat = 'zm'
                else:
                    gcat = 'gg'

                self.cc2[k][gcat][grid] =item[grid] 
        reps = dict()
        for c,item in self.cc2.items():
            for gc,xx in item.items():
              if len( xx.keys() ) > 1:
                if len( xx.keys() ) == 2:
                    a, b = sorted( list( xx.keys() ) )
                    ai, bi = [xx[k] for k in [a,b] ]
                    sai = set()
                    for k,v in ai.items():
                        for x in v:
                          sai.add(x)
                    sbi = set()
                    for k,v in bi.items():
                        for x in v:
                          sbi.add(x)
                    sd = sai.symmetric_difference( sbi )
                    if len(sd) == 0:
                        msg = 'identical'
                    else:
                      da = sai.difference( sbi )
                      db = sbi.difference( sai )
                      if len( da ) == 0:
                          msg = 'subset in %s' % a
                      elif len( db ) == 0:
                          msg = 'subset in %s' % b
                      else:
                          msg = 'OVERLAPS'

                reps[ (c,gc) ] = sorted( list( xx.keys() ) ) + [msg,]
        for t in sorted( list( reps.keys() ) ):
            print (t,reps[t] )



    def scan(self):
        self.cc = collections.defaultdict( lambda: collections.defaultdict( lambda: collections.defaultdict( set ) ) )
        for h, rec in self.results.items():
            #CMIP6.OMIP.NOAA-GFDL.GFDL-OM4p5B.omip1.r1i1p1f1.Omon.volcello.gn.v20180701
            activity, mip, inst, model, expt,variant_id,table,var,grid_id,version = rec['dset_id'].split('.')
            collection_id = '.'.join( [activity, mip, inst, model, expt,variant_id,table] )
            self.cc[collection_id][grid_id][version].add(var)


        ee = dict()
        count = collections.defaultdict( int )
        for c,item in self.cc.items():
            ff = dict()
            for gr,ss in item.items():
                ff[gr] = {k:sorted( list( v ) ) for k,v in ss.items()}
            count[ len( ff.keys() ) ] +=1 
            ##if len( ff.keys() ) > 1:
                ##print (c, sorted( list( ff.keys() ) ) )
            ee[c] = ff
        print ( count )
        oo = open( 'summary_by_collection.json', 'w' )
        info = 'overview'
        json.dump( {'header':info, 'results':ee}, oo, indent=4, sort_keys=True )
        oo.close()


c = CollectionCheck()
c.scan()
c.scan2()


