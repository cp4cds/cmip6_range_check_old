
import json

class Rtable(object):
    def __init__(self):
        ee = json.load( open( '../Resources/ranges.json', 'r' ) )
        self.data = ee['data']
        print(ee['header'])

    def csv(self):
        ks = sorted( list( self.data.keys() ) )
        oo = open( 'test.csv', 'w' )
        for k in ks:
            for c in ['ma_max', 'ma_min', 'max', 'min']:
                if self.data[k][c][1] != 'NONE':
                   rec = [k,c,str(self.data[k][c][0]),self.data[k][c][1]]
                   oo.write( '\t'.join( rec ) + '\n' )
        oo.close()



if __name__ == "__main__":
    r = Rtable()
