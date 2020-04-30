import os

##
## remove LD_LIBRARY_PATH to avoid a configuration issue with the conda installation
##

import sys
if "--RESTART" in sys.argv:
  sys.argv.pop( sys.argv.index( "--RESTART" ) )
elif "LD_LIBRARY_PATH" in os.environ:
  cmd = " ".join( sys.argv )
  os.popen( "(unset LD_LIBRARY_PATH;python %s --RESTART)" % cmd )
  sys.exit(0)

import matplotlib.pyplot as plt
import numpy
from matplotlib.patches import Ellipse, Polygon, Rectangle

class mbox(object):
  def __init__(self, subp, ax ):
    self.subp = subp
    self.ax = ax

  def add(self, xl, xh, yy):
    assert len(yy) == 9, 'Set up for 9 percentiles'
    q1 = yy[3]
    q3 = yy[5]
    me = yy[4]
    xm = (xl+xh)*.5
    xl1 = xm + 0.75*(xl-xm)
    xh1 = xm + 0.75*(xh-xm)
    xl2 = xm + 0.5*(xl-xm)
    xh2 = xm + 0.5*(xh-xm)
    self.ax.add_patch(Polygon([[xl, q1], [xl, me], [xh, me], [xh, q1]], closed=True,
                      fill=True, color='#8888ff'))
    self.ax.add_patch(Polygon([[xl, q3], [xl, me], [xh, me], [xh, q3]], closed=True,
                      fill=True, color='#ff8888'))
    self.subp.plot( [xm,xm], [yy[1],q1], linewidth=3, color='black' )
    self.subp.plot( [xl1,xh1], [yy[2],yy[2]], linewidth=3, color='black' )
    self.subp.plot( [xl2,xh2], [yy[1],yy[1]], linewidth=3, color='black' )
    self.subp.plot( [xm,xm], [yy[7],q3], linewidth=3, color='black' )
    self.subp.plot( [xl1,xh1], [yy[6],yy[6]], linewidth=3, color='black' )
    self.subp.plot( [xl2,xh2], [yy[7],yy[7]], linewidth=3, color='black' )
    self.subp.plot( [xm,], [yy[0],], marker='o', color='blue' )
    self.subp.plot( [xm,], [yy[8],], marker='o', color='red' )


def boxplot( dd, var, boxLegend = True ): 
   fig, ax = plt.subplots()
   ax.set_xticklabels('')
   ax.set_yticklabels('')
   fig.set_size_inches(9.,6.)

   n_groups = len(dd.keys())
   ks = sorted( dd.keys() )
   index = numpy.arange(n_groups  )
   bar_width = 1.0

   opacity = 0.8
   m = mbox(plt, ax)
   ii = 0
   for k in ks:
     rec = dd[k]["percentiles"][:]
     rec.reverse()
     m.add( ii +.1, ii+.9, rec )
     ii += 1
   ##refrec = cc[table][var]
   ##refv = getRef( refrec, var )
   ##if refv != False:
     ##x = ax.get_xlim()
     ##print 'Trying line plot for CMIP5 ref:',var,x,refv
     ##plt.plot( x, [refv[0],refv[0]], color='#0000ff', alpha=0.7, linewidth=3 )
     ##plt.plot( x, [refv[1],refv[1]], color='#ff0000', alpha=0.7, linewidth=3 )
     ##plt.plot( x, [refv[2],refv[2]], color='#00ff00', alpha=0.7, linewidth=2 )
     ##plt.plot( x, [refv[3],refv[3]], color='#aa00aa', alpha=0.7, linewidth=2 )

   plt.xlabel('Model')
   plt.ylabel(var)
   leg1 = Rectangle((0, 0), 0, 0, alpha=0.0)
   if boxLegend:
     leg = plt.legend( (leg1,leg1,leg1,leg1), ('boxes: quartiles','first bar: 5%, 95%','2nd bar: 1%,99%', 'circles: 0.1%,99.9%'), fontsize = 'x-small')
     leg.get_frame().set_alpha(0.5)
   plt.title('Ranges for %s historical CMIP6' % var )
   xt = ["%s %s" % tuple(x.split("_")[:2]) for x in ks]
   if len(ks) > 28:
     plt.xticks(index + bar_width, xt, rotation=40, ha='right', fontsize=8)
   else:
     plt.xticks(index + bar_width, xt, rotation=40, ha='right')

   ytfmt = {"hurs":"%3i%%", "tas":"%3.0fK"}
   yt = ax.get_yticks()
   ax.set_yticklabels( [ytfmt[var] % y for y in yt] )

   plt.tight_layout()
   setyl = False
   ax.set_ylim( [160.,340.] )
   if setyl:
     v1 = var + '_pp'
     dpith=17
     plt.ylim( self.ylims[var]  )
   else:
     v1 = var
     dpith=20
   plt.savefig( 'box_%s.png' % v1, dpi=150)
   plt.savefig( 'th_box_%s.png' % v1, dpi=dpith)

    
def example():
  fig, ax = plt.subplots()
  m = mbox(plt,ax)
  m.add( 0., .9, [-3.,-2.,-1.,0.,2.,3.,4.,5.,6.] )
  m.add( 1., 1.9, [-2.,-1.,0.,2.,3.,4.,5.,6.,6.5] )
  ax.set_ylim([-4.,7.])
  ax.set_xlim([0.,2.])
  ##plt.legend( ('label','l2'), numpoints=0 )
  plt.tight_layout()
  plt.show()


if __name__ == "__main__":
  import sys
  if len(sys.argv) == 1:
    example()
  else:
    import json
    ee = json.load( open( sys.argv[1], "r" ) )
    ipath = sys.argv[1]
    ifile = ipath.rpartition("/")[-1]
    var = ifile.split("_")[0]
    boxplot( ee["data"], var, boxLegend = True )
