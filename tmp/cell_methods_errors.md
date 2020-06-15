# Cell Methods Errors

## Cell Methods Errors - 1

 - Message: (7.3): Invalid 'name' in cell\_methods attribute: month, (7.3): Invalid 'name' in cell\_methods attribute: year
 - Models and Vars: KACE-1-0-G: Amon.tasmax,Amon.tasmin
 - Files affected: 2
 - Example: [tasmax\_Amon\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_20150101-21001230.nc](http://esgf-nimscmip6.apcc21.org/thredds/dodsC/my_cmip6_dataroot/ScenarioMIP/ssp126/R1/aa008s-Amon/CMIP6/ScenarioMIP/NIMS-KMA/KACE-1-0-G/ssp126/r1i1p1f1/Amon/tasmax/gr/v20200317/tasmax_Amon_KACE-1-0-G_ssp126_r1i1p1f1_gr_20150101-21001230.nc.html)

 - PID: [hdl:21.14100/4d8bfc10-1f8f-4a82-b586-5c7ee31bc2a1](http://hdl.handle.net/21.14100/4d8bfc10-1f8f-4a82-b586-5c7ee31bc2a1)

### ncdump sample

```
	float tasmax(time, lat, lon) ;
		tasmax:standard_name = "air_temperature" ;
		tasmax:long_name = "Daily Maximum Near-Surface Air Temperature" ;
		tasmax:units = "K" ;
		tasmax:cell_methods = "area: mean time: maximum (interval: 1 day) month: year: mean" ;
		tasmax:coordinates = "height" ;
```

## Cell Methods Errors - 2

 - Message: (7.3): Invalid cell\_method: mask, (7.3): Invalid 'name' in cell\_methods attribute: (comment
 - Models and Vars: KACE-1-0-G: SImon.sithick, SAM0-UNICON: SImon.sithick
 - Files affected: 18
 - Example: [sithick\_SImon\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_201501-210012.nc](http://esgf-nimscmip6.apcc21.org/thredds/dodsC/my_cmip6_dataroot/ScenarioMIP/ssp126/R1/aa008s-SImon/CMIP6/ScenarioMIP/NIMS-KMA/KACE-1-0-G/ssp126/r1i1p1f1/SImon/sithick/gr/v20200130/sithick_SImon_KACE-1-0-G_ssp126_r1i1p1f1_gr_201501-210012.nc.html)

 - PID: [hdl:21.14100/b22f1a2e-769d-4700-baee-6db41eec810a](http://hdl.handle.net/21.14100/b22f1a2e-769d-4700-baee-6db41eec810a)

### ncdump sample

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

## Cell Methods Errors - 3

 - Message: (7.3): Invalid syntax for cell\_methods attribute
 - Models and Vars: BCC-CSM2-MR: Amon.o3,Amon.tasmax,Amon.tasmin, BCC-ESM1: Amon.o3,Amon.tasmax,Amon.tasmin, FGOALS-g3: Amon.tasmax,Amon.tasmin, INM-CM4-8: Amon.tasmax,Amon.tasmin, INM-CM5-0: Amon.tasmax,Amon.tasmin, SAM0-UNICON: Amon.tasmax,Amon.tasmin
 - Files affected: 568
 - Example: [tasmin\_Amon\_INM-CM5-0\_piControl\_r1i1p1f1\_gr1\_254201-264112.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/INM/INM-CM5-0/piControl/r1i1p1f1/Amon/tasmin/gr1/v20190619/tasmin_Amon_INM-CM5-0_piControl_r1i1p1f1_gr1_254201-264112.nc.html)

 - PID: [hdl:21.14100/d65836bf-7a25-446d-8b9c-a18f19cfbd22](http://hdl.handle.net/21.14100/d65836bf-7a25-446d-8b9c-a18f19cfbd22)

### ncdump sample

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

## Cell Methods Errors - 4

 - Message: (7.3): Invalid unit hours, in cell\_methods comment
 - Models and Vars: KACE-1-0-G: 3hr.huss,3hr.tas,3hr.uas,3hr.vas
 - Files affected: 38
 - Example: [huss\_3hr\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_208501010130-209412302230.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/INM/INM-CM5-0/piControl/r1i1p1f1/Amon/tasmin/gr1/v20190619/tasmin_Amon_INM-CM5-0_piControl_r1i1p1f1_gr1_254201-264112.nc.html)

 - PID: [hdl:21.14100/e055c61e-6cbd-43c0-9420-60a2f9c2e1f1](http://hdl.handle.net/21.14100/e055c61e-6cbd-43c0-9420-60a2f9c2e1f1)

### ncdump sample

```
	float huss(time, lat, lon) ;
		huss:standard_name = "specific_humidity" ;
		huss:long_name = "Near-Surface Specific Humidity" ;
		huss:comment = "Near-surface (usually, 2 meter) specific humidity." ;
		huss:units = "1" ;
		huss:original_name = "m01s03i237" ;
		huss:cell_methods = "area: mean time: point (interval: 3 hours, Instantaneous)" ;
		huss:cell_measures = "area: areacella" ;
		huss:history = "2019-10-19T02:05:09Z altered by CMOR: Treated scalar dimension: \'height\'. 2019-10-19T02:05:09Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20)." ;
		huss:coordinates = "height" ;
		huss:missing_value = 1.e+20f ;
		huss:_FillValue = 1.e+20f ;
```

