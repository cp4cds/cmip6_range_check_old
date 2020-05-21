# CMIP6 Data Range Check

Extract end evaluate information about range of data values in CMIP6 datasets.

Abstract
========

This project aims to check data ranges in the archive of CMIP6 model output in order to provide information about the quality of data, provide guidance to the user community, and identify issues which need to be addressed in the planning of future model intercomparison projects.

The work is currently supported by funding from the Copernicus Climate Change Service (C3S) through a project which requires quality control of a subset of the CMIP6 archive which the IPCC WG1 has identified as a priority. 

Some of the CMIP6 variables have preset limits specified in the CMIP6 Data Request, but most do not. Where there is no a-priori information about valid ranges of data, new valid ranges will be established, if possible, by inspection of the CMIP6 multi-model ensemble, taking into account the degree of consistency between models.

In addition to the range of data values, the project will also examine the consistency of usage of the missing value flag in data files with relevant area masks. For instance, fields which are requested only on land surface grid points should have the missing value flag set if and only if a grid point as a land area fraction (variable `sftlf`) of 0%.

Introduction
============

The CMIP5 Standard Output spreadsheet specified a limits for many variables based on a scan of analogous variable in the CMIP3 archive. This was originally intended for use in automated tests, but experience showed that such tests produced too many false negatives resulting in which the specified limits where too restrictive. For the CMIP6 Data Request there was an attempt to avoid this through and analogous scan of the CMIP5 archive supplemented with visual inspection and checks on consistency of the CMIP5 model ensemble, but similar problems of false negatives (discussed further below) still occurred. nevertheless, the established guide values are useful in filtering the the extensive list of variables in the CMIP6 archive to identify a relatively compact list of _potential_ problems. Whether or not these are real problems relies on subjective interpretation. 




ScanFile

For each file, places the following in a python shelve file record:

Flag,version, time, checks, res0, res1, res2

* Flag: set to True .. 
* time: time at which reocrd is written, from time.ctime()
* checks: (checkSpecial, cc, maskerr): maskerr is set ot 1 if a mask is needed and not found
* res0: tuple: shape,median,max,min,mean abs max,mean abs minn, number of fill values,has fv (boolean), mean dt,max dt,units,tracking id
* res1: mean absolute value at each time (or sampled time points)
* res2: percentiles at each time (or sampled time) [from numpy.percentile, for percentiles 99.9,99.,95.,75.,50.,25.,5.,1.,.1)

