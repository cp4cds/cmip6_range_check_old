
import numpy, json


class Review(object):
  def __init__(self):
    pass

  def run(self,file):
    ee = json.load( open( file, 'r' ) )

    info = ee['info']
    dd = ee['data']
    nt = sum( [len(dd[k][5]) for k in dd.keys() ] )
    nf = len( dd.keys() )
    print (nt)
    work = numpy.zeros( (9,nt) )
    work02 = numpy.zeros( (5,nf) )
    i = 0
    j = 0
    for k in sorted( list( dd.keys() ) ):
      for l in dd[k][6]:
        work[:,i] = l
        i += 1
      work02[:,j] = dd[k][4][1:6]
      j += 1

    summary = [0.]*5
    percentiles = [0.]*9
    for k in range(9):
      percentiles[k] = numpy.median( work[k,:] )

    summary[0] = numpy.median( work02[0,:] )
    summary[1] = numpy.max( work02[1,:] )
    summary[2] = numpy.min( work02[2,:] )
    summary[3] = numpy.max( work02[3,:] )
    summary[4] = numpy.max( work02[4,:] )

    print ( percentiles, summary )

    this = {'percentiles':percentiles, "summary":summary}
    ofile = file.replace( ".json", "_summary.json" )
    oo = open( ofile, 'w' )
    info_out = {'title':info['title'], "tech":{"percentiles":[99.9,99.,95.,75.,50.,25.,5.,1.,.1], "summary":["median","max","min","mean absolute max","mean absolute min"]}}
    json.dump( {'info':info_out, 'data':this}, oo, indent=4, sort_keys=True )
    oo.close()

## l0: ['ok','shape','median','mx','mn','mamx','mamn','nfv','hasfv','dt0','dt1','units','tid']

      



r = Review()
r.run( 'hurs_AS-RCEC_TaiESM1_historical_00-01.json' )
