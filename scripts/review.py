import shelve, numpy, time, sys, collections, string, scipy, math, os
import scipy.cluster
from config import *
class c1(object):
    def __init__(self):
      self.a = collections.defaultdict( list )

def stn(x,j=','):
  if type(x) == type(''):
    return x
  elif type(x) == type([]):
    return string.join( [stn(i) for i in x], j )
  else:
    return str(x)


oo = open( 'reviewSummary03.txt', 'w' )
oot = open( 'reviewSummary03.csv', 'w' )

class scan1(object):

  def __init__(self,tag,vnlist):
    
    for vn in vnlist:
##for vn in ['clivi',]:
      thiss = 'shelve/%s/c/%s/%s' % (expt,tag,vn)
      thisx = 'shelve/%s/c/%s/x_%s' % (expt,tag,vn)
      if os.path.isfile(  thiss ) or os.path.isfile(  thiss + '.dat' ):
        self.run( thiss, vn, thisx )
    
  def run(self,thiss, vn, thisx):
    if not os.path.isfile( '%s.dir' % thiss ):
      print '!!!!!! NO SHELVE: ', thiss, vn
      return
    print '###########',thiss, vn, '#################'
    sh = shelve.open( thiss, 'r' )
    shx = shelve.open( thisx, 'r' )
    ks = sorted( [ k for k in sh.keys() if k[0] != '_' and k in shx] )
    if len( ks ) == 0:
      print '%s:: No fields to analyse\n' % (vn)
      return
##time.sleep( 3 )
#sh[f] = (t.shape[0],counts,bins,med,max,min,mamx,mamn,fvk)
#    sh[f] = (True,v.shape,med,mx,mn,mamx,mamn,fvcount,hasfv,dt0,dt1)
  ##nt_rec = collections.namedtuple( 'record', ['ok','shape','median','mx','mn','mamx','mamn','nfv','hasfv','dt0','dt1','units'] )
    nt_rec = collections.namedtuple( 'record', ['ok','shape','median','mx','mn','mamx','mamn','nfv','hasfv','dt0','dt1','units','tid'] )
    aa = []
    bb = []
    cc = []
    dd = []
    sver = 0.1
    if sh.has_key( '__info__'):
      sver = sh['__info__'][0]

    assert sver >0.3, 'Cannot handle version less than 0.3'
    col1 = collections.defaultdict( c1 )

    nf = 0
    ncon = 0
    ntrl = []
    for k in ks:
      fn = string.split( k, '/' )[-1]
      rec = sh[k][:]
      shxk = False
      if k in shx:
        thist = shx[k]
        if len(thist) == 2:
           print 'WARN: missing flags in shx record: ',k
           am, ap = thist
           flgs = (0,0,0)
        elif sver > 0.7:
           am,ap,flgs, dd = thist
        else:
           am,ap,flgs = thist
        shxk = True

      if len( flgs ) < 3:
        print model, vn
        print am, ap, flgs
      if flgs[2] != 0:
        print 'Skipping record with bad mask flag, %s, %s, %s' % (model,vn,flgs[2])
      elif rec[0]:
      ##ntr = nt_rec._make( rec[:11] )
        ntr = nt_rec._make( rec )
        ntrl.append(ntr)
        model = string.split( fn, '_' )[2]
        if ntr.mx - ntr.mn != 0.:
          r = rec[1:]
          col1[model].a['mn'].append( ntr.mn )
          col1[model].a['mx'].append( ntr.mx )
          col1[model].a['mamx'].append( ntr.mamx )
          col1[model].a['mamn'].append( ntr.mamn )
          col1[model].a['units'].append( ntr.units )
          col1[model].a['median'].append( ntr.median )
          col1[model].a['dt0'].append( ntr.dt0 )
          col1[model].a['dt1'].append( ntr.dt1 )
          col1[model].a['hasfv'].append( ntr.hasfv )
          col1[model].a['nfv'].append( ntr.nfv )
          if shxk:
            for l in ap:
              col1[model].a['pp'].append( l )
          try:
            aa.append( r[1] )
            bb.append( r[2] )
            dd.append( r[3] )
            cc.append( r[6] )
          except:
            print k
        else:
          print 'CONSTANT FIELD SKIPPED: %s' % model
          ncon += 1
      else:
        print 'FAILED: ',k
        nf += 1

    if shxk:
      for k in sorted( col1.keys() ):
        nfv = numpy.sum( col1[k].a['nfv'] )
        pp = [numpy.median( [l[i] for l in col1[k].a['pp']] ) for i in range(9)]
        oot.write( stn( ['__pctls__',k,vn,nfv,] + pp, '\t' ) + '\n' )
        print k,pp
    if len( col1.keys() ) == 0:
      #oo.write( '%s:: No fields to analyse, ncon=%s\n' % (vn,ncon) )
      print '%s:: No fields to analyse, ncon=%s\n' % (vn,ncon)
      return
    aa.sort()
    bb.sort()
    cc.sort()
    dd.sort()
    print '##################    minimums  ################'
    print dd[0],dd[-1],numpy.median(dd),numpy.histogram( dd )
    print '##################    medians ################'
    print aa[0],aa[-1],numpy.median(aa),numpy.histogram( aa )
    print '##################    maximums ################'
    print bb[0],bb[-1],numpy.median(bb),numpy.histogram( bb )
    print '##################    fill count ################'
    print cc[0],cc[-1],numpy.median(cc),numpy.histogram( cc )
    print 'Number of failed scans = %s' %  nf
    ks0 = sorted( col1.keys() )
    ks = []
    rng = {}
    lr = []
    lx = []
    for k in ks0:
      a,b = ( min( col1[k].a['mn'] ), max( col1[k].a['mx'] ) )
      c,d,e = ( min( col1[k].a['mamn'] ), max( col1[k].a['mamx'] ), string.join(sorted( list( set( col1[k].a['units'] ) ) ), '; ') )
      if (not math.isnan(a)) and (not math.isnan(b)):
        rng[k] = (a,b,b-a)
        ks.append(k)
        lr.append( [a,b] )
        lx.append( [c,d,e] )
        print k, rng[k]
  
    try:
      x = numpy.array( lr )
      cbk = scipy.cluster.vq.kmeans(x, 3 )
      kkk = [0,0,0]
      ix, dist = scipy.cluster.vq.vq( x, cbk[0] )
      print ix
      for k in range(len(ks)):
        oot.write( stn( [ks[k],vn,ix[k],lr[k][0],lr[k][1]] + lx[k], '\t' ) + '\n' )
      for k in range(  len(cbk[0])  ):
        oot.write( stn( ['cluster',vn,k,cbk[0][k][0],cbk[0][k][1], 0, 0, ''], '\t' ) + '\n' )
    except:
      for k in range(len(ks)):
        oot.write( stn( [ks[k],vn,0,lr[k][0],lr[k][1]] + lx[k], '\t' ) + '\n' )
      oot.write( stn( ['nocluster',vn,0,0,0,0,0,''], '\t' ) + '\n' )
      return
    for i in ix:
      kkk[i] += 1
    print cbk, kkk
    m = max( kkk )
    im = kkk.index(m)
    a0 = []
    b0 = []
    a1 = []
    b1 = []
    for i in range(len(lr)):
      if ix[i] == im:
        a0.append( lr[i][0] )
        b0.append( lr[i][1] )
      a1.append( lr[i][0] )
      b1.append( lr[i][1] )
    oor = [ cbk[0][im][0], cbk[0][im][1], m, min( a0 ), max(b0 ),  min(a1), max(b1), len(ks), '%5.2f' % (m/float(len(lr))) ]
    print oor
    oo.write( '%s, %s,\n' % (vn,string.join( [str(x) for x in oor], ',' ) ) )
###
### should now analyse this, to identify any "outlying" group .. e.g. if range of cluster differs from majority cluster.
### Can then define range in terms of (1) main cluster centroid, (2) main cluster extremes, (3) ensemble extremes, (4) proportion of models in main.
### In addition, provide (1) list of models in main cluster, (2) degree of difference between clusters.
###
  
    ll = []
    dl = []
    ee = {}
    okl = []
    rjl = []
    for k in range( len(ks) ):
      l0 = []
      m1 = ks[k]
      for j in range(k):
        l0.append( ll[j][k] )
      l0.append(0.)
      for j in range(k+1,len(ks)):
        m2 = ks[j]
        delt = ( abs( rng[m1][0] - rng[m2][0] ) + abs( rng[m1][1] - rng[m2][1] ) )/min( [rng[m1][2],rng[m2][2] ] )
        l0.append( delt)
        dl.append(delt)
      
      ll.append(l0)
      
      l0s = sorted(l0 )
      print m1,min(l0s),max(l0s)
  
    if len(dl) < 4:
      return
    dl.sort()
    dlmed = dl[ len(dl)/2 ]
    print numpy.histogram( dl )
    print '#################',dlmed, min(dl), max(dl)
    for k in range( len(ks) ):
      l0 = ll[k]
      m1 = ks[k]
      nnn = 0.
      acrit = 2.*dlmed
      for x in l0:
        if x > acrit:
          nnn += 1
      ee[m1] =  nnn < len(l0)/3
      if ee[m1]:
        okl.append( m1 )
      else:
        rjl.append( m1 )

expt = 'historical'
tag = 'aero3d'
ss = scan1(tag, locals()[tag])
oo.close()
oot.close()
