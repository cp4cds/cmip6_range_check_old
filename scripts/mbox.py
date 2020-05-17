import os, glob
from local_utilities import WGIPriority

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
    assert len(yy) in [9,13], 'Set up for 9 or 13 percentiles'
    if len(yy) == 9:
      q1 = yy[3]
      q3 = yy[5]
      me = yy[4]
      i999, i99, i95, i001, i01, i05 = (0,1,2,8,7,6)
    else:
      q1 = yy[5]
      q3 = yy[7]
      me = yy[6]
      i999, i99, i95, i001, i01, i05 = (0,2,3,12,10,9)

    xm = (xl+xh)*.5
    xl1 = xm + 0.75*(xl-xm)
    xh1 = xm + 0.75*(xh-xm)
    xl2 = xm + 0.5*(xl-xm)
    xh2 = xm + 0.5*(xh-xm)
    self.ax.add_patch(Polygon([[xl, q1], [xl, me], [xh, me], [xh, q1]], closed=True,
                      fill=True, color='#8888ff'))
    self.ax.add_patch(Polygon([[xl, q3], [xl, me], [xh, me], [xh, q3]], closed=True,
                      fill=True, color='#ff8888'))
    self.subp.plot( [xm,xm], [yy[i99],q1], linewidth=3, color='black' )
    self.subp.plot( [xl1,xh1], [yy[i95],yy[i95]], linewidth=3, color='black' )
    self.subp.plot( [xl2,xh2], [yy[i99],yy[i99]], linewidth=3, color='black' )
    self.subp.plot( [xm,xm], [yy[i01],q3], linewidth=3, color='black' )
    self.subp.plot( [xl1,xh1], [yy[i05],yy[i05]], linewidth=3, color='black' )
    self.subp.plot( [xl2,xh2], [yy[i01],yy[i01]], linewidth=3, color='black' )
    self.subp.plot( [xm,], [yy[i999],], marker='o', color='blue' )
    self.subp.plot( [xm,], [yy[i001],], marker='o', color='red' )

def boxplot( dd, var, boxLegend = True, units="1", image_dir="images" ): 
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
   table_records = [ ["Model","Minimum","5th pct","Median","95th pct","Maximum"],
                     [ " :--",  " :--: ",  " :--: ", " :--: ", " :--: ", " :--: "   ] ]

   for k in ks:
     this = dd[k]["percentiles"]
     thissum = dd[k]["summary"]
     table_records.append( [str(x) for x in [k,thissum[2],this[3],this[6],this[9],thissum[1] ]] )

     if type( this ) == type( [] ):
       rec = this[:]
     else:
       try:
         rec = this["0"][:]
       except:
         print ("Could not extract percentiles info for %s" % k )
         print (this.keys() )
         raise
     rec.reverse()
     m.add( ii +.1, ii+.9, rec )
     ii += 1

   oo = open( '%s/Overview_%s.md' % (image_dir,var), "w" )
   for record in table_records:
     oo.write( ' | '.join( record ) + "\n" )
   oo.close()


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
   if var in ytfmt:
     this_ytfmt = ytfmt[var]
   else:
     this_ytfmt = "%s"
     if units != "1":
       this_ytfmt += units
       if units == "%":
         this_ytfmt += "%"

   ax.set_yticklabels( [this_ytfmt % y for y in yt] )

   plt.tight_layout()
   setyl = False
   ##ax.set_ylim( [160.,340.] )
   if setyl:
     v1 = var + '_pp'
     dpith=17
     plt.ylim( self.ylims[var]  )
   else:
     v1 = var
     dpith=20
   plt.savefig( '%s/box_%s.png' % (image_dir,v1), dpi=150)
   plt.savefig( '%s/th_box_%s.png' % (image_dir,v1), dpi=dpith)

    
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

def check_json(table,ipath):
    ifile = ipath.rpartition("/")[-1]
    var = ifile.split("_")[0]
    wg1 =  WGIPriority()
    varid = "%s.%s" % (table,var)
    print( "check_json",table, ipath, varid )
    if varid not in wg1.ranges:
      print ( "No range information for %s" % varid )
      return None
    else:
      ranges = wg1.ranges[varid]
      ee = json.load( open( ipath, "r" ) )
      data = ee["data"]
      rsum = dict()
      for m in sorted( list( data.keys() ) ):
        this = data[m]["summary"]
        range_error_max = this[1] > float(ranges.max.value)
        range_error_min = this[2] < float(ranges.min.value)
        if not any( [range_error_max,range_error_min] ):
           res = (True,"OK")
        elif all( [range_error_max,range_error_min] ):
           res = (False, "ERROR: Max and Min range errors: %s > %s and %s < %s" % (this[1],ranges.max.value,this[2],ranges.min.value) )
        elif range_error_max:
           res = (False, "ERROR: Max range error: %s > %s" % (this[1],ranges.max.value) )
        elif range_error_min:
           res = (False, "ERROR: Min range error: %s < %s" % ( this[2],ranges.min.value) )
        print ("%s:: %s" % (m,res[1]) )
        rsum[m] = res[0]

    bad = [k for k,v in rsum.items() if not v]
    if len( bad) == 0:
       print ("All models in range")
    else:
       print( "WARNING: %s models (from %s) out of range" % (len(bad),len(rsum.keys())) )
           

def plot_json(table,ipath):
    ee = json.load( open( ipath, "r" ) )
    ifile = ipath.rpartition("/")[-1]
    image_dir = "images/%s" % table
    if not os.path.isdir( image_dir ):
      os.mkdir( image_dir )

    var = ifile.split("_")[0]
    wg1 =  WGIPriority()
    units = wg1.ee["%s.%s" % (table,var)]
    print ( var, units )
    boxplot( ee["data"], var, boxLegend = True, units=units, image_dir=image_dir )

def plot_files(table):
    fl = glob.glob( "json_ranges/%s/*.json" % table )
    for f in fl:
      plot_json( table, f )

if __name__ == "__main__":
  import sys
  if len(sys.argv) == 1:
    example()
  else:
    mode = sys.argv[1]
    print (sys.argv, mode)
    if mode in ["-p","-c"]:
      import json
      table, file = sys.argv[2:]
      if mode == "-p":
        plot_json( table, file )
      else:
        check_json( table, file )
    elif mode == "-px":
      import json
      table = sys.argv[2]
      plot_files( table )
