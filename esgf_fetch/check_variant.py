


import fetch as f
import collections

ii = open( 'lists/c3s34g_pids_qcTest_Oct2020.txt', 'r' )

models = set()
for l in ii.readlines():
    models.add( l.split('.')[3] )

filters_tas = 'table_id=Amon&mip_era=CMIP6&variable_id=%s&experiment_id=historical'

for v in ['tas','uas','vas']:
  eq = f.ESGF_Query(query=f.tmpl_tas, filters=filters_tas % v)
  eq.get_drs()


  cc = collections.defaultdict( set )
  for k,i in eq.drs_dict.items():
     cc[i[0].source_id].add( i[0].variant_id )


  oo = open( 'mvsum_%s.csv' % v, 'w' )
  for m in models:
      print (m, len(cc[m]) )
      oo.write( '\t'.join( [m,str(len(cc[m]))]) + '\n' )
  oo.close()

