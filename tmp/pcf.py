import collections
import csv
import sys, os
sys.path.append('../scripts')
import local_utilities as lu


## path example; /badc/cmip6/data/CMIP6/AerChemMIP/BCC/BCC-ESM1/hist-piNTCF/r1i1p1f1/Amon/ch4/gn/v20190621/ch4_Amon_BCC-ESM1_hist-piNTCF_r1i1p1f1_gn_185001-201412.nc


def mcl(x):
    x = x.replace( '_', '\_' )
    return x

class Parse(object):
   def __init__(self):
          """ Load wg1 priority variables and open cf results """
          self.wg1 = lu.WGIPriority(ifile="../scripts/AR6_priority_variables_02.csv")
          self.ii = csv.reader( open( "cmip6-cf-df.csv" ) )
          self.head = self.ii.__next__()

   def run(self):
          wg1 = self.wg1
          cc = collections.defaultdict( set )
          cc3 = collections.defaultdict( set )
          cc2 = collections.defaultdict( lambda : collections.defaultdict( set ) )
          self.ee = collections.defaultdict( int )
          iv = self.head.index( 'var_id' )
          ie = self.head.index( 'error_level' )
          ied = self.head.index( 'error_details' )
          ifp = self.head.index( 'filepath' )
          im = self.head.index( 'model' )
          print ( self.head )
          ix = 1
          ic = collections.defaultdict( int )
          for l in self.ii:
              ix += 1
              if ix > 500000000:
                  break
              rec = l
              if len(rec) > len(self.head):
                  print ( rec )
              else:
                for k in range(len(rec)):
                  cc[self.head[k]].add( rec[k] )
              v0, err, fp, model, err_det = [rec[x] for x in [iv,ie, ifp, im,ied ]]
              if err == "ERROR":
                  fn = fp.rpartition('/')[-1]
                  var, table = fn.split('_')[:2]
                  vid = '%s.%s' % (table,var)
                  self.ee[vid] += 1 
                  if vid in wg1.ee:
                      ar6 = 'y'
                  else:
                      ar6 = 'n'

                  if v0 == var:
                      ic['v' + ar6] += 1
                      if ar6 == 'y':
                        cc2[model][vid].add(tuple(rec))
                        cc3[err_det].add( (model,vid) )
                  else:
                      ic['o' + ar6] += 1
          self.cc = cc
          self.cc2 = cc2
          self.cc3 = cc3
          self.ic = ic


   def write_md(self):
       ksn = [k for k in self.cc3.keys() if k.find( 'standard_name' ) != -1]
       kcm = [k for k in self.cc3.keys() if k.find( 'cell_methods' ) != -1]
       self.write_md_file( 'standard_name_errors.md', 'Standard Name Errors', ksn )
       self.write_md_file( 'cell_methods_errors.md', 'Cell Methods Errors', kcm )
       self.write_md_file( 'miscellaneous_errors.md', 'Miscellaneous Errors', [k for k in self.cc3.keys() if (k not in ksn) and (k not in kcm)] )

   def write_md_file(self, mdfile, title, key_list):
       ifp = self.head.index( 'filepath' )
       oo = open( mdfile, 'w' )
       oo.write( '%s\n%s\n\n' % (title,'='*len(title)) )
       oo.write( 'Overview\n========\n\n' )
       ks = sorted( key_list )
       rec = ['Message','Model/variable','Count','Example']
       align = [" :--: ", ]*4
       oo.write( ' | '.join(rec) + '\n' )
       oo.write( ' | '.join(align) + '\n' )

       ee = []
       for k in ks:
           rec = [k,', '.join( [str(x) for x in sorted( list( self.cc3[k] ) ) ] ) ]
           nf = str( sum( [ len(self.cc2[model][vid]) for model, vid in self.cc3[k] ] ) )
           rec.append(nf)
           model, vid = self.cc3[k].pop()
           r0 = self.cc2[model][vid].pop()
           fp = r0[ifp]
           rec.append(fp)
           rec = [mcl(x) for x in rec]

           oo.write( ' | '.join(rec) + '\n' )
           ee.append( (k,fp) )

       oos = open( 'ffetch.sh', 'w' )
       for k,fp in ee:
           oos.write( 'jcpfx 5 %s\n' % fp )
           fn = fp.rpartition('/')[-1]
           if os.path.isfile( fp ) or os.path.isfile( fn ):
               var = fn.split('_')[0]
               if os.path.isfile( fp ):
                 os.popen( 'ncdump -h %s | grep %s[\(:] > .ncdump' % (fp,var) ).read()
               else:
                 os.popen( 'ncdump -h %s | grep %s[\(:] > .ncdump' % (fn,var) ).read()
               oo.write( "%s\n%s\n\n'''\n" % (k,"="*len(k)) )
               for l in open( '.ncdump' ).readlines():
                   oo.write( l + '\n' )
               oo.write( "'''\n\n" )

       oo.close()
       oos.close()



p = Parse()
p.run()
p.write_md()
