bsub << END_OF_SCRIPT
#!/bin/bash
#BSUB -q short-serial
#BSUB -oo logs_02/shs-%J.o
#BSUB -eo logs_02/shs-%J.e 
#BSUB -W 8:00

source activate myenv38

ls -l $1*

python << END_OF_PYTHON
print( "HELLO FROM PYTHON" )
input_file="$1"
print( "Inspecting %s" % input_file )
import shelve, json
sh = shelve.open( input_file )
print ( sh['__info__'] )
print ( sh['__tech__'] )
ks = [k for k in sh.keys() if k[0] != '_']
print ( 'Data records: %s' % len(ks) )
ksamp = sorted( ks )[0]
print ( 'Sample: %s' % ksamp )
print ( sh[ksamp] )

ee = dict()
for k in list(sh.keys()):
 if k[0] == '_':
    if k == "__tech__":

      this = sh[k].copy()
      finfo = this['file_info']
      finfo['fill_value'] = float( finfo['fill_value'] )
      finfo['shape'] = tuple( [int(x) for x in finfo['shape']] )
      if 'time_intervals' in finfo:
        finfo['time_intervals'] = tuple( [float(x) for x in finfo['time_intervals'] ] )
      this['file_info'] = finfo
      ee[k] = this

    else:
      ee[k] = sh[k]
 else:
  this = dict()
  SKIPPED = []
  for k1 in sh[k].keys():
    frag = sh[k][k1]
    print( "%s: %s" % (k1, frag) )
    if k1 == 'basic':
      this['basic'] = (*[float(x) for x in frag[:3]],  int(frag[3]) )
    elif k1 == 'quantiles':
      this[k1] = [float(x) for x in frag]
    elif k1 == 'extremes':
      res = []
      for trip in frag:
        res.append( [trip[0], trip[1], [float(x) for x in trip[2]]] )
      this[k1] = res
    elif k1 == 'mask_ok':
      this[k1] = [frag[0],*[int(x) for x in frag[1:]]]
    elif k1 in ['fraction']:
      this[k1] = [frag[0],*[float(x) for x in frag[1:]]]
      ###this[k1] = frag
    else:
      SKIPPED.append( k1 )

  if len(SKIPPED) == 0:
    this['SKIPPED'] = SKIPPED
    print('SKIPPED RECORDS: %s' % SKIPPED ) 

  ee[k] = this

oo = open( '%s.json' % input_file, 'w' )
json.dump( {'A: header':'Dump of results from %s' % input_file, 'B: data':ee}, oo, indent=4, sort_keys=True )
oo.close()
END_OF_PYTHON

END_OF_SCRIPT

