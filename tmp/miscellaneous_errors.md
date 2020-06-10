Miscellaneous Errors
====================

Overview
========

Miscellaneous Errors - 1
------------------------

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type), (7.2): Invalid cell\_measures syntax
 - Models and Vars: CESM2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-FV2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-WACCM: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-WACCM-FV2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo
 - Files affected: 438
 - Example: uo\_Omon\_CESM2-WACCM-FV2\_historical\_r1i1p1f1\_gn\_190001-194912.nc

ncdump sample
=============

```
	float uo(time, lev, nlat, nlon) ;
		uo:_FillValue = 1.e+20f ;
		uo:cell_measures = "--OPT" ;
		uo:cell_methods = "time: mean" ;
		uo:comment = "UVEL" ;
		uo:coordinates = "time lev lat lon" ;
		uo:description = "Prognostic x-ward velocity component resolved by the model." ;
		uo:frequency = "mon" ;
		uo:id = "uo" ;
		uo:long_name = "Sea Water X Velocity" ;
		uo:mipTable = "Omon" ;
		uo:missing_value = 1.e+20 ;
		uo:out_name = "uo" ;
		uo:prov = "Omon ((isd.003))" ;
		uo:realm = "ocean" ;
		uo:standard_name = "sea_water_x_velocity" ;
		uo:time = "time" ;
		uo:time_label = "time-mean" ;
		uo:time_title = "Temporal mean" ;
		uo:title = "Sea Water X Velocity" ;
		uo:type = "real" ;
		uo:units = "m s-1" ;
		uo:variable_id = "uo" ;
```

Miscellaneous Errors - 2
------------------------

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type), (7.3): Invalid type1: sector - must be a variable name or valid area\_type
 - Models and Vars: CESM2: Emon.sweLut, CESM2-FV2: Emon.sweLut, CESM2-WACCM-FV2: Emon.sweLut
 - Files affected: 7
 - Example: sweLut\_Emon\_CESM2\_esm-hist\_r2i1p1f1\_gn\_185001-189912.nc

ncdump sample
=============

```
	float sweLut(time, landuse, lat, lon) ;
		sweLut:_FillValue = 1.e+20f ;
		sweLut:cell_measures = "area: areacella" ;
		sweLut:cell_methods = "area: time: mean where sector" ;
		sweLut:comment = "CLM_landunit_to_CMIP6_Lut(H2OSNO,\"all\",time,lat,lon,grid1d_ixy,grid1d_jxy,grid1d_lon,grid1d_lat,land1d_lon,land1d_lat,land1d_ityplunit,land1d_active,land1d_wtgcell,landUse)" ;
		sweLut:coordinates = "time landuse lat lon" ;
		sweLut:description = "The surface called \"surface\" means the lower boundary of the atmosphere. \"lwe\" means liquid water equivalent. \"Amount\" means mass per unit area. The construction lwe_thickness_of_X_amount or _content means the vertical extent of a layer of liquid water having the same mass per unit area. Surface amount refers to the amount on the ground, excluding that on the plant or vegetation canopy." ;
		sweLut:frequency = "mon" ;
		sweLut:id = "sweLut" ;
		sweLut:long_name = "Snow Water Equivalent on Land-Use Tile" ;
		sweLut:mipTable = "Emon" ;
		sweLut:missing_value = 1.e+20 ;
		sweLut:out_name = "sweLut" ;
		sweLut:prov = "LUMIP [Lmon_Lut]" ;
		sweLut:realm = "land" ;
		sweLut:standard_name = "lwe_thickness_of_surface_snow_amount" ;
		sweLut:time = "time" ;
		sweLut:time_label = "time-mean" ;
		sweLut:time_title = "Temporal mean" ;
		sweLut:title = "Snow Water Equivalent on Land-Use Tile" ;
		sweLut:type = "real" ;
		sweLut:units = "m" ;
		sweLut:variable_id = "sweLut" ;
```

Miscellaneous Errors - 3
------------------------

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type)
 - Models and Vars: CESM2: 3hr.huss, .. [164], CESM2-FV2: AERmon.abs550aer, .. [149], CESM2-WACCM: AERmon.abs550aer, .. [131], CESM2-WACCM-FV2: AERmon.abs550aer, .. [159], MCM-UA-1-0: Ofx.deptho
 - Files affected: 37409
 - Example: hus\_Amon\_CESM2\_pdSST-futAntSIC\_r39i1p1f1\_gn\_200006-200105.nc

ncdump sample
=============

```
	float hus(time, plev, lat, lon) ;
		hus:_FillValue = 1.e+20f ;
		hus:cell_measures = "area: areacella" ;
		hus:cell_methods = "time: mean" ;
		hus:comment = "vinth2p(Q,hyam, hybm, plev, PS, P0)" ;
		hus:coordinates = "time plev lat lon" ;
		hus:description = "Specific humidity is the mass fraction of water vapor in (moist) air." ;
		hus:frequency = "mon" ;
		hus:id = "hus" ;
		hus:long_name = "Specific Humidity" ;
		hus:mipTable = "Amon" ;
		hus:missing_value = 1.e+20 ;
		hus:out_name = "hus" ;
		hus:prov = "Amon ((isd.003))" ;
		hus:realm = "atmos" ;
		hus:standard_name = "specific_humidity" ;
		hus:time = "time" ;
		hus:time_label = "time-mean" ;
		hus:time_title = "Temporal mean" ;
		hus:title = "Specific Humidity" ;
		hus:type = "real" ;
		hus:units = "1" ;
		hus:variable_id = "hus" ;
```

Miscellaneous Errors - 4
------------------------

 - Message: (7.2): Invalid cell\_measures syntax
 - Models and Vars: AWI-CM-1-1-MR: Omon.tauuo, .. [10], AWI-ESM-1-1-LR: Omon.thetaoga, GFDL-CM4: AERmonZ.ta,AERmonZ.ua,EdayZ.ua,EdayZ.zg, GFDL-ESM4: AERmonZ.ta,AERmonZ.ua,EdayZ.ua,EdayZ.zg, MPI-ESM1-2-HR: Omon.tauuo, .. [6]
 - Files affected: 1509
 - Example: ua\_EdayZ\_GFDL-CM4\_ssp585\_r1i1p1f1\_gr2z\_20610101-20801231.nc

ncdump sample
=============

```
	float ua(time, plev, lat) ;
		ua:long_name = "Eastward Wind" ;
		ua:units = "m s-1" ;
		ua:missing_value = 1.e+20f ;
		ua:cell_methods = "longitude: mean time: mean" ;
		ua:cell_measures = " " ;
		ua:standard_name = "eastward_wind" ;
		ua:interp_method = "conserve_order2" ;
		ua:_FillValue = 1.e+20f ;
		ua:original_name = "ua" ;
```

Miscellaneous Errors - 5
------------------------

 - Message: (7.2): cell\_measures variable areacella must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-ESM-1-1-LR: Amon.prsn, GFDL-AM4: Amon.clt, .. [36], GISS-E2-1-G: SImon.sithick, GISS-E2-1-G-CC: SImon.sithick, GISS-E2-1-H: SImon.sithick, IPSL-CM6A-LR: fx.mrsofc, MPI-ESM1-2-HR: Amon.clt, .. [52], MPI-ESM1-2-XR: Amon.clt, .. [52]
 - Files affected: 6902
 - Example: tasmin\_Amon\_MPI-ESM1-2-XR\_highresSST-present\_r1i1p1f1\_gn\_199801-199812.nc

ncdump sample
=============

```
	float tasmin(time, lat, lon) ;
		tasmin:standard_name = "air_temperature" ;
		tasmin:long_name = "Daily Minimum Near-Surface Air Temperature" ;
		tasmin:units = "K" ;
		tasmin:code = 202 ;
		tasmin:table = 128 ;
		tasmin:_FillValue = 1.e+20f ;
		tasmin:missing_value = 1.e+20f ;
		tasmin:cell_measures = "area: areacella" ;
		tasmin:comment = "minimum near-surface (usually, 2 meter) air temperature (add cell_method attribute \'time: min\')" ;
		tasmin:cell_methods = "area: mean time: minimum within days time: mean over days" ;
```

Miscellaneous Errors - 6
------------------------

 - Message: (7.2): cell\_measures variable areacellg must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-ESM-1-1-LR: ImonAnt.prsn,ImonGre.prsn
 - Files affected: 22
 - Example: prsn\_ImonGre\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_190101-191012.nc

ncdump sample
=============

```
	float prsn(time, ncells) ;
		prsn:units = "kg m-2 s-1" ;
		prsn:CDI_grid_type = "unstructured" ;
		prsn:_FillValue = 1.e+30f ;
		prsn:missing_value = 1.e+30f ;
		prsn:description = "At surface; includes precipitation of all forms of water in the solid phase" ;
		prsn:coordinates = "lat lon" ;
		prsn:standard_name = "snowfall_flux" ;
		prsn:cell_methods = "area: time: mean where ice_sheet" ;
		prsn:cell_measures = "area: areacellg" ;
```

Miscellaneous Errors - 7
------------------------

 - Message: (7.2): cell\_measures variable areacello must either exist in this netCDF file or be named by the external\_variables attribute, (7.2): cell\_measures variable volcello must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-CM-1-1-MR: Omon.so,Omon.thetao, AWI-ESM-1-1-LR: Omon.thetao
 - Files affected: 373
 - Example: thetao\_Omon\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_188101-189012.nc

ncdump sample
=============

```
	float thetao(time, depth, ncells) ;
		thetao:units = "degC" ;
		thetao:CDI_grid_type = "unstructured" ;
		thetao:_FillValue = 1.e+30f ;
		thetao:missing_value = 1.e+30f ;
		thetao:description = "Diagnostic should be contributed even for models using conservative temperature as prognostic field." ;
		thetao:coordinates = "lat lon" ;
		thetao:standard_name = "sea_water_potential_temperature" ;
		thetao:cell_methods = "area: mean where sea time: mean" ;
		thetao:cell_measures = "area: areacello volume: volcello" ;
```

Miscellaneous Errors - 8
------------------------

 - Message: (7.2): cell\_measures variable areacello must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-CM-1-1-MR: Oday.tos, .. [8], AWI-ESM-1-1-LR: Oday.tos, .. [5], CNRM-ESM2-1: Ofx.deptho
 - Files affected: 1051
 - Example: tos\_Omon\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_194101-195012.nc

ncdump sample
=============

```
	float tos(time, ncells) ;
		tos:units = "degC" ;
		tos:CDI_grid_type = "unstructured" ;
		tos:_FillValue = 1.e+30f ;
		tos:missing_value = 1.e+30f ;
		tos:description = "Temperature of upper boundary of the liquid ocean, including temperatures below sea-ice and floating ice shelves." ;
		tos:coordinates = "lat lon" ;
		tos:standard_name = "sea_surface_temperature" ;
		tos:cell_methods = "area: mean where sea time: mean" ;
		tos:cell_measures = "area: areacello" ;
```

Miscellaneous Errors - 9
------------------------

 - Message: (7.3): Invalid type1: landuse - must be a variable name or valid area\_type
 - Models and Vars: CNRM-ESM2-1: Emon.sweLut
 - Files affected: 1
 - Example: sweLut\_Emon\_CNRM-ESM2-1\_esm-hist\_r1i1p1f2\_gr\_185001-201412.nc

ncdump sample
=============

```
	float sweLut(time, landUse, lat, lon) ;
		sweLut:long_name = "snow water equivalent on land use tile" ;
		sweLut:units = "m" ;
		sweLut:online_operation = "average" ;
		sweLut:cell_methods = "area: time: mean where landuse" ;
		sweLut:interval_operation = "900 s" ;
		sweLut:interval_write = "1 month" ;
		sweLut:_FillValue = 1.e+20f ;
		sweLut:missing_value = 1.e+20f ;
		sweLut:coordinates = "" ;
		sweLut:description = "snow water equivalent on land use tile" ;
		sweLut:history = "none" ;
		sweLut:cell_measures = "area: areacella" ;
		sweLut:standard_name = "lwe_thickness_of_surface_snow_amount" ;
```

Miscellaneous Errors - 10
------------------------

 - Message: (7.3): Invalid type1: sector - must be a variable name or valid area\_type
 - Models and Vars: UKESM1-0-LL: Emon.sweLut
 - Files affected: 41
 - Example: sweLut\_Emon\_UKESM1-0-LL\_historical\_r10i1p1f2\_gn\_195001-201412.nc

ncdump sample
=============

```
	float sweLut(time, landuse, lat, lon) ;
		sweLut:standard_name = "lwe_thickness_of_surface_snow_amount" ;
		sweLut:long_name = "Snow Water Equivalent on Land-Use Tile" ;
		sweLut:comment = "The surface called \'surface\' means the lower boundary of the atmosphere. \'lwe\' means liquid water equivalent. \'Amount\' means mass per unit area. The construction lwe_thickness_of_X_amount or _content means the vertical extent of a layer of liquid water having the same mass per unit area. Surface amount refers to the amount on the ground, excluding that on the plant or vegetation canopy." ;
		sweLut:units = "m" ;
		sweLut:original_name = "mo: land_use_tile_mean( (stash: m01s08i236, lbproc: 128) / (FRESHWATER_DENSITY: 1000.), (stash: m01s03i317, lbproc: 128))" ;
		sweLut:cell_methods = "area: time: mean where sector" ;
		sweLut:cell_measures = "area: areacella" ;
		sweLut:history = "2019-12-09T15:26:51Z altered by CMOR: Reordered dimensions, original order: landuse time lat lon. 2019-12-09T15:26:51Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20)." ;
		sweLut:missing_value = 1.e+20f ;
		sweLut:_FillValue = 1.e+20f ;
		sweLut:coordinates = "sector" ;
```

