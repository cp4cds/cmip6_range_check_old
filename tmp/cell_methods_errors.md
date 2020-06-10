Cell Methods Errors
===================

Overview
========

Cell Methods Errors - 1
-----------------------

 - Message: (7.3): Invalid 'name' in cell\_methods attribute: month, (7.3): Invalid 'name' in cell\_methods attribute: year
 - Models and Vars: KACE-1-0-G: Amon.tasmax,Amon.tasmin
 - Files affected: 2
 - Example: tasmin\_Amon\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_20150101-21001230.nc

ncdump sample
=============

```
	float tasmin(time, lat, lon) ;
		tasmin:standard_name = "air_temperature" ;
		tasmin:long_name = "Daily Minimum Near-Surface Air Temperature" ;
		tasmin:units = "K" ;
		tasmin:cell_methods = "area: mean time: minimum (interval: 1 day) month: year: mean" ;
		tasmin:coordinates = "height" ;
```

Cell Methods Errors - 2
-----------------------

 - Message: (7.3): Invalid cell\_method: mask, (7.3): Invalid 'name' in cell\_methods attribute: (comment
 - Models and Vars: KACE-1-0-G: SImon.sithick, SAM0-UNICON: SImon.sithick
 - Files affected: 18
 - Example: sithick\_SImon\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_201501-210012.nc

ncdump sample
=============

```
	float sithick(time, lat, lon) ;
		sithick:standard_name = "sea_ice_thickness" ;
		sithick:long_name = "Sea Ice Thickness" ;
		sithick:comment = "Actual (floe) thickness of sea ice (NOT volume divided by grid area as was done in CMIP5)" ;
		sithick:units = "m" ;
		sithick:original_name = "SITHICK" ;
		sithick:cell_methods = "area: time: mean (interval: 1 month) where sea_ice (comment: mask=siconc)" ;
		sithick:cell_measures = "area: areacello" ;
		sithick:history = "2020-01-30T09:55:04Z altered by CMOR: replaced missing value flag (0) with standard missing value (1e+20)." ;
		sithick:missing_value = 1.e+20f ;
		sithick:_FillValue = 1.e+20f ;
		sithick:coordinates = "latitude longitude" ;
```

Cell Methods Errors - 3
-----------------------

 - Message: (7.3): Invalid syntax for cell\_methods attribute
 - Models and Vars: BCC-CSM2-MR: Amon.o3,Amon.tasmax,Amon.tasmin, BCC-ESM1: Amon.o3,Amon.tasmax,Amon.tasmin, FGOALS-g3: Amon.tasmax,Amon.tasmin, INM-CM4-8: Amon.tasmax,Amon.tasmin, INM-CM5-0: Amon.tasmax,Amon.tasmin, SAM0-UNICON: Amon.tasmax,Amon.tasmin
 - Files affected: 568
 - Example: tasmin\_Amon\_INM-CM5-0\_piControl\_r1i1p1f1\_gr1\_254201-264112.nc

ncdump sample
=============

```
	float tasmin(time, lat, lon) ;
		tasmin:standard_name = "air_temperature" ;
		tasmin:long_name = "Daily Minimum Near-Surface Air Temperature" ;
		tasmin:comment = "minimum near-surface (usually, 2 meter) air temperature (add cell_method attribute \'time: min\')" ;
		tasmin:units = "K" ;
		tasmin:original_name = "tasmin" ;
		tasmin:cell_methods = "area: mean time: minimum (interval: 1 month) within days time: mean over days" ;
		tasmin:cell_measures = "area: areacella" ;
		tasmin:history = "2019-06-18T22:06:15Z altered by CMOR: Treated scalar dimension: \'height\'." ;
		tasmin:coordinates = "height" ;
		tasmin:missing_value = 1.e+20f ;
		tasmin:_FillValue = 1.e+20f ;
```

Cell Methods Errors - 4
-----------------------

 - Message: (7.3): Invalid unit hours, in cell\_methods comment
 - Models and Vars: KACE-1-0-G: 3hr.huss,3hr.tas,3hr.uas,3hr.vas
 - Files affected: 38
 - Example: tas\_3hr\_KACE-1-0-G\_historical\_r1i1p1f1\_gr\_199001010130-199912302230.nc

ncdump sample
=============

```
	float tas(time, lat, lon) ;
		tas:standard_name = "air_temperature" ;
		tas:long_name = "Near-Surface Air Temperature" ;
		tas:comment = "near-surface (usually, 2 meter) air temperature" ;
		tas:units = "K" ;
		tas:original_name = "m01s03i236" ;
		tas:cell_methods = "area: mean time: point (interval: 3 hours, Instantaneous)" ;
		tas:cell_measures = "area: areacella" ;
		tas:history = "2019-09-13T05:56:46Z altered by CMOR: Treated scalar dimension: \'height\'. 2019-09-13T05:56:46Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20)." ;
		tas:coordinates = "height" ;
		tas:missing_value = 1.e+20f ;
		tas:_FillValue = 1.e+20f ;
```

