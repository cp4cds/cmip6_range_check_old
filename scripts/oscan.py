import glob, collections, sys

class Oscan(object):
  def __init__(self,idir='Amon.evspsbl'):
    self.idir = idir
    self.fl = sorted( list( glob.glob( 'out_01/%s/*' % idir ) ) )
    self.cc = collections.defaultdict( list )
    for f in self.fl:
      fname = f.rpartition( '/' )[-1]
      fds,x,tt = fname.rpartition( '_' )
      self.cc[fds].append( f )


    print( 'Files: %s, datasets: %s' % (len(self.fl), len(self.cc) ) )

  def scan(self):
    for ds in sorted( list( self.cc.keys() ) ):
      nf = 0
      for p in self.cc[ds]:
        for l in open(p).readlines():
          if l[:4] == 'FAIL':
            nf += 1
      print ('%s: %s' % (ds,nf) )


if __name__ == "__main__":
  idir='Amon.evspsbl'
  if len( sys.argv ) == 2:
    idir = sys.argv[1]
    
  o = Oscan(idir=idir)
  o.scan()
      
