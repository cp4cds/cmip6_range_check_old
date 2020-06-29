import os, glob
from local_utilities import WGIPriority, CheckJson, stn
'''
 -p, --plot [optional flag]: plot range values in a json file
'''

##
## remove LD_LIBRARY_PATH to avoid a configuration issue with the conda installation
##

class RecordException(Exception):
  def __init__(self,file,key,**kwargs):
    self.file = file
    self.key = key
    self.kwargs = kwargs

import sys
##
## this fix not needed with upgrade to ubuntu 18.04
##if "--RESTART" in sys.argv:
  ##sys.argv.pop( sys.argv.index( "--RESTART" ) )
##elif "LD_LIBRARY_PATH" in os.environ:
  ##cmd = " ".join( sys.argv )
  ##os.popen( "(unset LD_LIBRARY_PATH;python %s --RESTART)" % cmd )
  ##print ("You need to: unset LD_LIBRARY_PATH and rerun" )
  ##sys.exit(0)

import matplotlib.pyplot as plt
import numpy
from matplotlib.patches import Ellipse, Polygon, Rectangle

class mbox(object):
  def __init__(self, subp, ax ):
    self.subp = subp
    self.ax = ax

  def add(self, xl, xh, yy):
    assert len(yy) in [9,13,29], 'Set up for 9 or 13 percentiles'
    if len(yy) == 9:
      q1 = yy[3]
      q3 = yy[5]
      me = yy[4]
      i999, i99, i95, i001, i01, i05 = (0,1,2,8,7,6)
    elif len(yy) in [13,29]:
      i0 = (len(yy) - 13)//2
      q1 = yy[5] + i0
      q3 = yy[7] + i0
      me = yy[6] + i0
      i999, i99, i95, i001, i01, i05 = [i0 + x for x in (0,2,3,12,10,9)]

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

def boxplot( dd, var, title, percentiles,boxLegend = True, units="1", image_dir="images" ): 
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
   hh = ["Q(%s)" % stn(x) for x in percentiles[::-1]]
   table_records = [ ["Model","Minimum"] + hh + ["Maximum",],
                     [ " :--",  ] + [" :--: ", ]*( len(percentiles) + 2 ) ]

   for k in ks:
     this = dd[k]["percentiles"]
     thissum = dd[k]["summary"]

     isDict = type(this) == type( {} )
     if isDict:
       this = this["0"]

     isDict = type(thissum) == type( {} )
     if isDict:
       thissum = thissum["0"]

     isList = type(this) in [type([]), type(())] 
### and len(this) == 13
     if not ( isList or isDict ):
       raise RecordException("not known",k,this=this)

     if not ( type(thissum) in [type([]), type(())] and len(thissum) == 5 ):
       raise RecordException("not known",k,thissum=thissum)

     tr0 = [k,thissum[2]] + this[::-1] + [thissum[1]]
     table_records.append( [stn(x) for x in tr0 ] )

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
   plt.title('%s [%s] historical' % (title,var) )
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
   plt.close()

    
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
           
def plot_json(table,ipath):
    ee = json.load( open( ipath, "r" ) )
    ifile = ipath.rpartition("/")[-1]
    image_dir = "images/%s" % table
    if not os.path.isdir( image_dir ):
      os.mkdir( image_dir )

    var = ifile.split("_")[0]
    wg1 =  WGIPriority()
    units = wg1.ee["%s.%s" % (table,var)]
    title = wg1.title["%s.%s" % (table,var)]
    print ( var, units )
    pcts = ee["info"]["tech"]["percentiles"]
    boxplot( ee["data"], var, title, pcts, boxLegend = True, units=units, image_dir=image_dir )

def all_files(table,mode="plot.x"):
    fl = glob.glob( "json_ranges/%s/*.json" % table )
    for f in sorted(fl):
      try:
        if mode == "plot.x":
          plot_json( table, f )
        else:
          check_json = CheckJson()
          check_json( table, f, verbose=False )
      except RecordException as e:
        print ("====== ERROR WHILE PROCESSING %s\n====================================\n" % f )
        print ("key: %s, kwargs: %s" % (e.key,e.kwargs) )
        raise
      except:
        print ("====== ERROR WHILE PROCESSING %s\n====================================\n" % f )
        raise

if __name__ == "__main__":
  __version__ = "0.0.1"
  import sys, argparse
  if len(sys.argv) == 1:
    example()
    sys.exit(1)
  parser = argparse.ArgumentParser()
  parser.add_argument( '-p','--plot', dest='mode', action='append_const', const='plot', help='plot range values in a json file' )
  parser.add_argument( '-px','--plot_dir', dest='mode', action='append_const', const='plot.x', help='plot for all matching files in a directory' )
  parser.add_argument( '-cx','--check_dir', dest='mode', action='append_const', const='check.x', help='plot for all matching files in a directory' )
  parser.add_argument( '-c','--check', dest='mode', action='append_const', const='check', help='check range values' )
  parser.add_argument( '-v', '--version', action='version', version=__version__)
  parser.add_argument( 'table', type=str, help='MIP table name')
  parser.add_argument( 'file', type=str, help='name of file or directory, required for options -p or -c', nargs='?' )
  ##parser.add_argument( 'trailing', metavar='word', type=str, nargs='+',
                     ##help="[table] and name of file or directory" )
##
## this does not fit well with the structure below ... in which positional argument options vary according to mode
##
## best to move -px ....?
##
## this will give this.mode as a list ....
##   -- makes for simple parsing.
##
## run( file, plot=None, 
## run_parsed( this )
  this = parser.parse_args( sys.argv[1:] )
  if this.mode == None or len(this.mode) != 1:
    print (" At most one mode must be specified from %s" % " ".join( ['-p','-px','-c','-cx'] ) )
    sys.exit(0)
  mode = this.mode[0]
  if mode in ['plot','check'] and this.table == None:
    print ("Positional argument table must be given when mode if plot or check" )
    sys.exit(0)
    
  print (sys.argv, mode)
  print ('STARTING: ', mode)
  if mode in ["plot","check"]:
      import json
      table, file = sys.argv[2:]
      print ('STARTING: ', table, file, this.table, this.file )
      if mode == "plot":
        plot_json( this.table, this.file )
      else:
        check_json = CheckJson()
        check_json( this.table, ipath=this.file)
  elif mode in ["plot.x","check.x"]:
      import json
      all_files( this.table, mode=mode )
