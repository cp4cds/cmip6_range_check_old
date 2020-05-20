import collections, os, glob

## see batch_prep.bsub

def p2var():
    fl = glob.glob( "inputs/historical/lsout/files_x1*.txt"  )
    cc = collections.defaultdict( set )
    for f in fl:
      ii = open( f ).readlines()
      for l in ii:
        parts = l.strip().split( "/"  )
        tab, var = parts[ 10:12 ]
        cc[ (tab,var) ].add( l.strip() )
    for k in cc.keys():
      oo = open( "inputs/historical/byvar/x1_%s_%s_latest.txt" % k, "w" )
      for l in sorted( list( cc[k] ) ):
        oo.write( l + "\n" )
      oo.close()
 
p2var()
print( "DONE" )
