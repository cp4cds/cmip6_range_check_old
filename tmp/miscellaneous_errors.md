# Miscellaneous Errors

## Miscellaneous Errors - 1

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type), (7.2): Invalid cell\_measures syntax
 - Models and Vars: CESM2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-FV2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-WACCM: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-WACCM-FV2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo
 - Files affected: 438
 - Example: vo\_Omon\_CESM2\_1pctCO2\_r1i1p1f1\_gn\_005101-010012.nc

 - PID: [hdl:21.14100/8783a205-d2aa-4e4f-abe5-34cd92adb2a8](http://hdl.handle.net/21.14100/8783a205-d2aa-4e4f-abe5-34cd92adb2a8)

### ncdump sample

```
	float vo(time, lev, nlat, nlon) ;
		vo:_FillValue = 1.e+20f ;
		vo:cell_measures = "--OPT" ;
		vo:cell_methods = "time: mean" ;
		vo:comment = "Prognostic y-ward velocity component resolved by the model." ;
		vo:coordinates = "time lev lat lon" ;
		vo:description = "Prognostic y-ward velocity component resolved by the model." ;
		vo:frequency = "mon" ;
		vo:id = "vo" ;
		vo:long_name = "Sea Water Y Velocity" ;
		vo:mipTable = "Omon" ;
		vo:missing_value = 1.e+20 ;
		vo:out_name = "vo" ;
		vo:prov = "Omon ((isd.003))" ;
		vo:realm = "ocean" ;
		vo:standard_name = "sea_water_y_velocity" ;
		vo:time = "time" ;
		vo:time_label = "time-mean" ;
		vo:time_title = "Temporal mean" ;
		vo:title = "Sea Water Y Velocity" ;
		vo:type = "real" ;
		vo:units = "m s-1" ;
		vo:variable_id = "vo" ;
```

## Miscellaneous Errors - 2

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type), (7.3): Invalid type1: sector - must be a variable name or valid area\_type
 - Models and Vars: CESM2: Emon.sweLut, CESM2-FV2: Emon.sweLut, CESM2-WACCM-FV2: Emon.sweLut
 - Files affected: 7
 - Example: sweLut\_Emon\_CESM2\_esm-hist\_r2i1p1f1\_gn\_200001-201412.nc

 - PID: [hdl:21.14100/412deb76-94d7-41a8-a0fb-e9a838c1ee3d](http://hdl.handle.net/21.14100/412deb76-94d7-41a8-a0fb-e9a838c1ee3d)

### ncdump sample

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

## Miscellaneous Errors - 3

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type)
 - Models and Vars: CESM2: 3hr.huss, .. [164], CESM2-FV2: AERmon.abs550aer, .. [149], CESM2-WACCM: AERmon.abs550aer, .. [131], CESM2-WACCM-FV2: AERmon.abs550aer, .. [159], MCM-UA-1-0: Ofx.deptho
 - Files affected: 37409
 - Example: mmrbc\_AERmon\_CESM2-WACCM\_ssp126\_r1i1p1f1\_gn\_206501-210012.nc

 - PID: [hdl:21.14100/d1d42ac9-36dc-4cc5-acae-a469314f8631](http://hdl.handle.net/21.14100/d1d42ac9-36dc-4cc5-acae-a469314f8631)

### ncdump sample

```
	float mmrbc(time, lev, lat, lon) ;
		mmrbc:_FillValue = 1.e+20f ;
		mmrbc:cell_measures = "area: areacella" ;
		mmrbc:cell_methods = "area: time: mean" ;
		mmrbc:comment = "bc_a1 + bc_a4" ;
		mmrbc:coordinates = "time lev lat lon" ;
		mmrbc:description = "Dry mass fraction of black carbon aerosol particles in air." ;
		mmrbc:frequency = "mon" ;
		mmrbc:id = "mmrbc" ;
		mmrbc:long_name = "Elemental Carbon Mass Mixing Ratio" ;
		mmrbc:mipTable = "AERmon" ;
		mmrbc:missing_value = 1.e+20 ;
		mmrbc:out_name = "mmrbc" ;
		mmrbc:prov = "AERmon ((isd.003))" ;
		mmrbc:realm = "aerosol" ;
		mmrbc:standard_name = "mass_fraction_of_elemental_carbon_dry_aerosol_particles_in_air" ;
		mmrbc:time = "time" ;
		mmrbc:time_label = "time-mean" ;
		mmrbc:time_title = "Temporal mean" ;
		mmrbc:title = "Elemental Carbon Mass Mixing Ratio" ;
		mmrbc:type = "real" ;
		mmrbc:units = "kg kg-1" ;
		mmrbc:variable_id = "mmrbc" ;
```

## Miscellaneous Errors - 4

 - Message: (7.2): Invalid cell\_measures syntax
 - Models and Vars: AWI-CM-1-1-MR: Omon.tauuo, .. [10], AWI-ESM-1-1-LR: Omon.thetaoga, GFDL-CM4: AERmonZ.ta,AERmonZ.ua,EdayZ.ua,EdayZ.zg, GFDL-ESM4: AERmonZ.ta,AERmonZ.ua,EdayZ.ua,EdayZ.zg, MPI-ESM1-2-HR: Omon.tauuo, .. [6]
 - Files affected: 1509
 - Example: uo\_Omon\_MPI-ESM1-2-HR\_control-1950\_r1i1p1f1\_gn\_203601-203612.nc

 - PID: [hdl:21.14100/0eb6c95c-3f56-4ee2-ba6a-f5331c1f471f](http://hdl.handle.net/21.14100/0eb6c95c-3f56-4ee2-ba6a-f5331c1f471f)

### ncdump sample

```
	float uo(time, depth, y_2, x_2) ;
		uo:standard_name = "sea_water_x_velocity" ;
		uo:long_name = "Sea Water X Velocity" ;
		uo:units = "m s-1" ;
		uo:code = 3 ;
		uo:coordinates = "lat_2 lon_2" ;
		uo:_FillValue = 1.e+20f ;
		uo:missing_value = 1.e+20f ;
		uo:cell_methods = "time: mean" ;
		uo:cell_measures = "--OPT" ;
		uo:comment = "Prognostic x-ward velocity component resolved by the model." ;
```

## Miscellaneous Errors - 5

 - Message: (7.2): cell\_measures variable areacella must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-ESM-1-1-LR: Amon.prsn, GFDL-AM4: Amon.clt, .. [36], GISS-E2-1-G: SImon.sithick, GISS-E2-1-G-CC: SImon.sithick, GISS-E2-1-H: SImon.sithick, IPSL-CM6A-LR: fx.mrsofc, MPI-ESM1-2-HR: Amon.clt, .. [52], MPI-ESM1-2-XR: Amon.clt, .. [52]
 - Files affected: 6902
 - Example: rsutcs\_Amon\_MPI-ESM1-2-HR\_highresSST-present\_r1i1p1f1\_gn\_198201-198212.nc

 - PID: [hdl:21.14100/42118a87-7b4e-419d-9b00-2faedca28a6a](http://hdl.handle.net/21.14100/42118a87-7b4e-419d-9b00-2faedca28a6a)

### ncdump sample

```
	float rsutcs(time, lat, lon) ;
		rsutcs:standard_name = "toa_outgoing_shortwave_flux_assuming_clear_sky" ;
		rsutcs:long_name = "TOA Outgoing Clear-Sky Shortwave Radiation" ;
		rsutcs:units = "W m-2" ;
		rsutcs:_FillValue = 1.e+20f ;
		rsutcs:missing_value = 1.e+20f ;
		rsutcs:cell_measures = "area: areacella" ;
		rsutcs:comment = "Calculated in the absence of clouds." ;
		rsutcs:cell_methods = "area: time: mean" ;
```

## Miscellaneous Errors - 6

 - Message: (7.2): cell\_measures variable areacellg must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-ESM-1-1-LR: ImonAnt.prsn,ImonGre.prsn
 - Files affected: 22
 - Example: prsn\_ImonGre\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_190101-191012.nc

 - PID: [hdl:21.14100/26be2e49-7641-48d7-97a8-78a79414d10e](http://hdl.handle.net/21.14100/26be2e49-7641-48d7-97a8-78a79414d10e)

### ncdump sample

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

## Miscellaneous Errors - 7

 - Message: (7.2): cell\_measures variable areacello must either exist in this netCDF file or be named by the external\_variables attribute, (7.2): cell\_measures variable volcello must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-CM-1-1-MR: Omon.so,Omon.thetao, AWI-ESM-1-1-LR: Omon.thetao
 - Files affected: 373
 - Example: thetao\_Omon\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_188101-189012.nc

 - PID: [hdl:21.14100/e3213373-10ae-47cc-8eea-dab4d021d9f6](http://hdl.handle.net/21.14100/e3213373-10ae-47cc-8eea-dab4d021d9f6)

### ncdump sample

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

## Miscellaneous Errors - 8

 - Message: (7.2): cell\_measures variable areacello must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-CM-1-1-MR: Oday.tos, .. [8], AWI-ESM-1-1-LR: Oday.tos, .. [5], CNRM-ESM2-1: Ofx.deptho
 - Files affected: 1051
 - Example: prsn\_Omon\_AWI-CM-1-1-MR\_ssp370\_r4i1p1f1\_gn\_205101-206012.nc

 - PID: [hdl:21.14100/045b7cff-dfc3-4068-8110-60726bfff4de](http://hdl.handle.net/21.14100/045b7cff-dfc3-4068-8110-60726bfff4de)

### ncdump sample

```
	float prsn(time, ncells) ;
		prsn:units = "kg m-2 s-1" ;
		prsn:CDI_grid_type = "unstructured" ;
		prsn:_FillValue = 1.e+30f ;
		prsn:missing_value = 1.e+30f ;
		prsn:description = "at surface; includes precipitation of all forms of water in the solid phase" ;
		prsn:coordinates = "lat lon" ;
		prsn:standard_name = "snowfall_flux" ;
		prsn:cell_methods = "area: mean where ice_free_sea over sea time: mean" ;
		prsn:cell_measures = "area: areacello" ;
```

## Miscellaneous Errors - 9

 - Message: (7.3): Invalid type1: landuse - must be a variable name or valid area\_type
 - Models and Vars: CNRM-ESM2-1: Emon.sweLut
 - Files affected: 1
 - Example: sweLut\_Emon\_CNRM-ESM2-1\_esm-hist\_r1i1p1f2\_gr\_185001-201412.nc

 - PID: [hdl:21.14100/c5be1142-4d24-4ae5-bff9-8dbf073c81cc](http://hdl.handle.net/21.14100/c5be1142-4d24-4ae5-bff9-8dbf073c81cc)

### ncdump sample

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

## Miscellaneous Errors - 10

 - Message: (7.3): Invalid type1: sector - must be a variable name or valid area\_type
 - Models and Vars: UKESM1-0-LL: Emon.sweLut
 - Files affected: 41
 - Example: sweLut\_Emon\_UKESM1-0-LL\_esm-1pct-brch-2000PgC\_r1i1p1f2\_gn\_205001-206112.nc

 - PID: [hdl:21.14100/bc4919e8-c8d6-4a8f-b0fe-b693621f9eef](http://hdl.handle.net/21.14100/bc4919e8-c8d6-4a8f-b0fe-b693621f9eef)

### ncdump sample

```
	float sweLut(time, landuse, lat, lon) ;
		sweLut:standard_name = "lwe_thickness_of_surface_snow_amount" ;
		sweLut:long_name = "Snow Water Equivalent on Land-Use Tile" ;
		sweLut:comment = "The surface called \'surface\' means the lower boundary of the atmosphere. \'lwe\' means liquid water equivalent. \'Amount\' means mass per unit area. The construction lwe_thickness_of_X_amount or _content means the vertical extent of a layer of liquid water having the same mass per unit area. Surface amount refers to the amount on the ground, excluding that on the plant or vegetation canopy." ;
		sweLut:units = "m" ;
		sweLut:original_name = "mo: land_use_tile_mean( (stash: m01s08i236, lbproc: 128) / (FRESHWATER_DENSITY: 1000.), (stash: m01s03i317, lbproc: 128))" ;
		sweLut:cell_methods = "area: time: mean where sector" ;
		sweLut:cell_measures = "area: areacella" ;
		sweLut:history = "2019-11-28T10:25:27Z altered by CMOR: Reordered dimensions, original order: landuse time lat lon. 2019-11-28T10:25:27Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20)." ;
		sweLut:missing_value = 1.e+20f ;
		sweLut:_FillValue = 1.e+20f ;
		sweLut:coordinates = "sector" ;
```

