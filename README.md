# cmip6_range_check
Extract information about range of data values in CMIP6 datasets


ScanFile

For each file, places the following in a python shelve file record:

Flag,version, time, checks, res0, res1, res2

* Flag: set to True .. 
* time: time at which reocrd is written, from time.ctime()
* checks: (checkSpecial, cc, maskerr): maskerr is set ot 1 if a mask is needed and not found
* res0: tuple: shape,median,max,min,mean abs max,mean abs minn, number of fill values,has fv (boolean), mean dt,max dt,units,tracking id
* res1: mean absolute value at each time (or sampled time points)
* res2: percentiles at each time (or sampled time) [from numpy.percentile, for percentiles 99.9,99.,95.,75.,50.,25.,5.,1.,.1)

