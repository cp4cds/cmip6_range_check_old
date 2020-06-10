# Cell Methods Errors

## Cell Methods Errors - 1

 - Message: (7.3): Invalid 'name' in cell\_methods attribute: month, (7.3): Invalid 'name' in cell\_methods attribute: year
 - Models and Vars: KACE-1-0-G: Amon.tasmax,Amon.tasmin
 - Files affected: 2
 - Example: tasmax\_Amon\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_20150101-21001230.nc

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
 - Example: sithick\_SImon\_SAM0-UNICON\_historical\_r1i1p1f1\_gn\_185001-185912.nc

 - PID: [hdl:21.14100/e4f94168-a4c6-411e-97bd-730e392915dc](http://hdl.handle.net/21.14100/e4f94168-a4c6-411e-97bd-730e392915dc)

### ncdump sample

```
	float sithick(time, j, i) ;
		sithick:standard_name = "sea_ice_thickness" ;
		sithick:long_name = "Sea Ice Thickness" ;
		sithick:comment = "Actual (floe) thickness of sea ice (NOT volume divided by grid area as was done in CMIP5)" ;
		sithick:units = "m" ;
		sithick:history = "rewrote by cmor via python script 2019-04-02T05:18:56Z altered by CMOR: replaced missing value flag (1e+30) with standard missing value (1e+20)." ;
		sithick:cell_methods = "area: time: mean (interval: 1 month) where sea_ice (comment: mask=siconc)" ;
		sithick:cell_measures = "area: areacello" ;
		sithick:missing_value = 1.e+20f ;
		sithick:_FillValue = 1.e+20f ;
		sithick:coordinates = "latitude longitude" ;
```

## Cell Methods Errors - 3

 - Message: (7.3): Invalid syntax for cell\_methods attribute
 - Models and Vars: BCC-CSM2-MR: Amon.o3,Amon.tasmax,Amon.tasmin, BCC-ESM1: Amon.o3,Amon.tasmax,Amon.tasmin, FGOALS-g3: Amon.tasmax,Amon.tasmin, INM-CM4-8: Amon.tasmax,Amon.tasmin, INM-CM5-0: Amon.tasmax,Amon.tasmin, SAM0-UNICON: Amon.tasmax,Amon.tasmin
 - Files affected: 568
 - Example: tasmin\_Amon\_BCC-ESM1\_piControl\_r1i1p1f1\_gn\_185001-230012.nc

 - PID: [hdl:21.14100/e406a6f8-16de-4c43-834d-e08ab3437436](http://hdl.handle.net/21.14100/e406a6f8-16de-4c43-834d-e08ab3437436)

### ncdump sample

```
	float tasmin(time, lat, lon) ;
		tasmin:standard_name = "air_temperature" ;
		tasmin:long_name = "Daily Minimum Near-Surface Air Temperature" ;
		tasmin:comment = "minimum near-surface (usually, 2 meter) air temperature (add cell_method attribute \'time: min\')" ;
		tasmin:units = "K" ;
		tasmin:original_name = "TREFMNAV" ;
		tasmin:cell_methods = "area: mean time: minimum (interval: 20 minutes) within days time: mean over days" ;
		tasmin:cell_measures = "area: areacella" ;
		tasmin:history = "2018-12-14T08:53:31Z altered by CMOR: Treated scalar dimension: \'height\'." ;
		tasmin:coordinates = "height" ;
		tasmin:missing_value = 1.e+20f ;
		tasmin:_FillValue = 1.e+20f ;
```

## Cell Methods Errors - 4

 - Message: (7.3): Invalid unit hours, in cell\_methods comment
 - Models and Vars: KACE-1-0-G: 3hr.huss,3hr.tas,3hr.uas,3hr.vas
 - Files affected: 38
 - Example: vas\_3hr\_KACE-1-0-G\_ssp370\_r1i1p1f1\_gr\_208501010130-209412302230.nc

 - PID: [hdl:21.14100/328bef08-4a3e-4109-bb11-2e17753e6809](http://hdl.handle.net/21.14100/328bef08-4a3e-4109-bb11-2e17753e6809)

### ncdump sample

```
	float vas(time, lat, lon) ;
		vas:standard_name = "northward_wind" ;
		vas:long_name = "Northward Near-Surface Wind" ;
		vas:comment = "Northward component of the near surface wind" ;
		vas:units = "m s-1" ;
		vas:original_name = "m01s03i226" ;
		vas:cell_methods = "area: mean time: point (interval: 3 hours, Instantaneous)" ;
		vas:cell_measures = "area: areacella" ;
		vas:history = "2019-12-25T09:52:28Z altered by CMOR: Treated scalar dimension: \'height\'. 2019-12-25T09:52:28Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20)." ;
		vas:coordinates = "height" ;
		vas:missing_value = 1.e+20f ;
		vas:_FillValue = 1.e+20f ;
```

