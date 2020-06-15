# Miscellaneous Errors

## Miscellaneous Errors - 1

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type), (7.2): Invalid cell\_measures syntax
 - Models and Vars: CESM2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-FV2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-WACCM: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-WACCM-FV2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo
 - Files affected: 438
 - Example: [uo\_Omon\_CESM2-WACCM\_abrupt-4xCO2\_r1i1p1f1\_gn\_010001-015012.nc](http://esgf-data.ucar.edu/thredds/dodsC/esg_dataroot/CMIP6/CMIP/NCAR/CESM2-WACCM/abrupt-4xCO2/r1i1p1f1/Omon/uo/gn/v20190425/uo_Omon_CESM2-WACCM_abrupt-4xCO2_r1i1p1f1_gn_010001-015012.nc.html)

 - PID: [hdl:21.14100/368ac575-558a-41db-8f9a-d9043225481b](http://hdl.handle.net/21.14100/368ac575-558a-41db-8f9a-d9043225481b)

### ncdump sample

```
	float uo(time, lev, nlat, nlon) ;
		uo:_FillValue = 1.e+20f ;
		uo:cell_measures = "--OPT" ;
		uo:cell_methods = "time: mean" ;
		uo:comment = "Prognostic x-ward velocity component resolved by the model." ;
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

## Miscellaneous Errors - 2

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type), (7.3): Invalid type1: sector - must be a variable name or valid area\_type
 - Models and Vars: CESM2: Emon.sweLut, CESM2-FV2: Emon.sweLut, CESM2-WACCM-FV2: Emon.sweLut
 - Files affected: 7
 - Example: [sweLut\_Emon\_CESM2-WACCM-FV2\_historical\_r1i1p1f1\_gn\_200001-201412.nc](http://esgf-data.ucar.edu/thredds/dodsC/esg_dataroot/CMIP6/CMIP/NCAR/CESM2-WACCM-FV2/historical/r1i1p1f1/Emon/sweLut/gn/v20191120/sweLut_Emon_CESM2-WACCM-FV2_historical_r1i1p1f1_gn_200001-201412.nc.html)

 - PID: [hdl:21.14100/65646a24-6c4c-4ac8-a9af-0054920adb06](http://hdl.handle.net/21.14100/65646a24-6c4c-4ac8-a9af-0054920adb06)

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
 - Example: [rsds\_ImonGre\_CESM2\_piControl\_r1i1p1f1\_gn\_050001-059912.nc](http://esgf-data.ucar.edu/thredds/dodsC/esg_dataroot/CMIP6/CMIP/NCAR/CESM2/piControl/r1i1p1f1/ImonGre/rsds/gn/v20190320/rsds_ImonGre_CESM2_piControl_r1i1p1f1_gn_110001-120012.nc.html)

 - PID: [hdl:21.14100/ba6e3b1a-bddd-4e0d-b399-5c6e3bf121b9](http://hdl.handle.net/21.14100/ba6e3b1a-bddd-4e0d-b399-5c6e3bf121b9)

### ncdump sample

```
	float rsds(time, lat, lon) ;
		rsds:_FillValue = 1.e+20f ;
		rsds:cell_measures = "area: areacellg" ;
		rsds:cell_methods = "area: time: mean where ice_sheet" ;
		rsds:comment = "Surface solar irradiance for UV calculations." ;
		rsds:coordinates = "time lat lon" ;
		rsds:description = "Surface solar irradiance for UV calculations." ;
		rsds:frequency = "mon" ;
		rsds:id = "rsds" ;
		rsds:long_name = "Surface Downwelling Shortwave Radiation" ;
		rsds:mipTable = "ImonGre" ;
		rsds:missing_value = 1.e+20 ;
		rsds:out_name = "rsds" ;
		rsds:positive = "down" ;
		rsds:prov = "ISMIP6 [ImonGre]" ;
		rsds:realm = "landIce land" ;
		rsds:standard_name = "surface_downwelling_shortwave_flux_in_air" ;
		rsds:time = "time" ;
		rsds:time_label = "time-mean" ;
		rsds:time_title = "Temporal mean" ;
		rsds:title = "Surface Downwelling Shortwave Radiation" ;
		rsds:type = "real" ;
		rsds:units = "W m-2" ;
		rsds:variable_id = "rsds" ;
```

## Miscellaneous Errors - 4

 - Message: (7.2): Invalid cell\_measures syntax
 - Models and Vars: AWI-CM-1-1-MR: Omon.tauuo, .. [10], AWI-ESM-1-1-LR: Omon.thetaoga, GFDL-CM4: AERmonZ.ta,AERmonZ.ua,EdayZ.ua,EdayZ.zg, GFDL-ESM4: AERmonZ.ta,AERmonZ.ua,EdayZ.ua,EdayZ.zg, MPI-ESM1-2-HR: Omon.tauuo, .. [6]
 - Files affected: 1509
 - Example: [vo\_Omon\_AWI-CM-1-1-MR\_historical\_r1i1p1f1\_gn\_194101-195012.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/AWI/AWI-CM-1-1-MR/historical/r1i1p1f1/Omon/vo/gn/v20181218/vo_Omon_AWI-CM-1-1-MR_historical_r1i1p1f1_gn_194101-195012.nc.html)

 - PID: [hdl:21.14100/acbb9666-4bce-49c8-91c7-6326336d87cc](http://hdl.handle.net/21.14100/acbb9666-4bce-49c8-91c7-6326336d87cc)

### ncdump sample

```
	float vo(time, depth, ncells) ;
		vo:units = "m s-1" ;
		vo:CDI_grid_type = "unstructured" ;
		vo:_FillValue = 1.e+30f ;
		vo:missing_value = 1.e+30f ;
		vo:description = "Prognostic x-ward velocity component resolved by the model." ;
		vo:coordinates = "lat lon" ;
		vo:standard_name = "sea_water_y_velocity" ;
		vo:cell_methods = "time: mean" ;
		vo:cell_measures = "--OPT" ;
```

## Miscellaneous Errors - 5

 - Message: (7.2): cell\_measures variable areacella must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-ESM-1-1-LR: Amon.prsn, GFDL-AM4: Amon.clt, .. [36], GISS-E2-1-G: SImon.sithick, GISS-E2-1-G-CC: SImon.sithick, GISS-E2-1-H: SImon.sithick, IPSL-CM6A-LR: fx.mrsofc, MPI-ESM1-2-HR: Amon.clt, .. [52], MPI-ESM1-2-XR: Amon.clt, .. [52]
 - Files affected: 6902
 - Example: [huss\_Amon\_MPI-ESM1-2-HR\_highresSST-present\_r1i1p1f1\_gn\_200601-200612.nc](http://esgf-data3.ceda.ac.uk/thredds/dodsC/esg_cmip6/CMIP6/HighResMIP/MPI-M/MPI-ESM1-2-HR/highresSST-present/r1i1p1f1/Amon/huss/gn/v20190923/huss_Amon_MPI-ESM1-2-HR_highresSST-present_r1i1p1f1_gn_200601-200612.nc.html)

 - PID: [hdl:21.14100/4197fd63-4f4d-40a7-b2d2-d002a93b2f54](http://hdl.handle.net/21.14100/4197fd63-4f4d-40a7-b2d2-d002a93b2f54)

### ncdump sample

```
	float huss(time, lat, lon) ;
		huss:standard_name = "specific_humidity" ;
		huss:long_name = "Near-Surface Specific Humidity" ;
		huss:units = "1.0" ;
		huss:code = 54 ;
		huss:table = 128 ;
		huss:_FillValue = 1.e+20f ;
		huss:missing_value = 1.e+20f ;
		huss:cell_measures = "area: areacella" ;
		huss:comment = "Near-surface (usually, 2 meter) specific humidity." ;
		huss:cell_methods = "area: time: mean" ;
```

## Miscellaneous Errors - 6

 - Message: (7.2): cell\_measures variable areacellg must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-ESM-1-1-LR: ImonAnt.prsn,ImonGre.prsn
 - Files affected: 22
 - Example: [prsn\_ImonAnt\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_193101-194012.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/AWI/AWI-ESM-1-1-LR/piControl/r1i1p1f1/ImonAnt/prsn/gn/v20200212/prsn_ImonAnt_AWI-ESM-1-1-LR_piControl_r1i1p1f1_gn_193101-194012.nc.html)

 - PID: [hdl:21.14100/56eba8ef-7b1f-45da-af93-ec688be5db9e](http://hdl.handle.net/21.14100/56eba8ef-7b1f-45da-af93-ec688be5db9e)

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
 - Example: [so\_Omon\_AWI-CM-1-1-MR\_piControl\_r1i1p1f1\_gn\_260101-261012.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/AWI/AWI-CM-1-1-MR/piControl/r1i1p1f1/Omon/so/gn/v20181218/so_Omon_AWI-CM-1-1-MR_piControl_r1i1p1f1_gn_260101-261012.nc.html)

 - PID: [hdl:21.14100/127162cd-a2a8-4d1e-88ad-f3ae9d8151af](http://hdl.handle.net/21.14100/127162cd-a2a8-4d1e-88ad-f3ae9d8151af)

### ncdump sample

```
	float so(time, depth, ncells) ;
		so:units = "0.001" ;
		so:CDI_grid_type = "unstructured" ;
		so:_FillValue = 1.e+30f ;
		so:missing_value = 1.e+30f ;
		so:description = "Sea water salinity is the salt content of sea water, often on the Practical Salinity Scale of 1978. However, the unqualified term \'salinity\' is generic and does not necessarily imply any particular method of calculation. The units of salinity are dimensionless and the units attribute should normally be given as 1e-3 or 0.001 i.e. parts per thousand. There are standard names for the more precisely defined salinity quantities: sea_water_knudsen_salinity, S_K (used for salinity observations between 1901 and 1966),  sea_water_cox_salinity, S_C (used for salinity observations between 1967 and 1977), sea_water_practical_salinity, S_P (used for salinity observations from 1978 to the present day), sea_water_absolute_salinity, S_A, sea_water_preformed_salinity, S_*, and sea_water_reference_salinity. Practical Salinity is reported on the Practical Salinity Scale of 1978 (PSS-78), and is usually based on the electrical conductivity of sea water in observations since the 1960s." ;
		so:coordinates = "lat lon" ;
		so:standard_name = "sea_water_salinity" ;
		so:cell_methods = "area: mean where sea time: mean" ;
		so:cell_measures = "area: areacello volume: volcello" ;
```

## Miscellaneous Errors - 8

 - Message: (7.2): cell\_measures variable areacello must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-CM-1-1-MR: Oday.tos, .. [8], AWI-ESM-1-1-LR: Oday.tos, .. [5], CNRM-ESM2-1: Ofx.deptho
 - Files affected: 1051
 - Example: [prsn\_Omon\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_186101-187012.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/AWI/AWI-ESM-1-1-LR/piControl/r1i1p1f1/Omon/prsn/gn/v20200212/prsn_Omon_AWI-ESM-1-1-LR_piControl_r1i1p1f1_gn_186101-187012.nc.html)

 - PID: [hdl:21.14100/7d287bcf-39e7-48e5-9de7-add902c6be12](http://hdl.handle.net/21.14100/7d287bcf-39e7-48e5-9de7-add902c6be12)

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
		prsn:cell_methods = "area: mean where ice_free_sea over sea time: mean" ;
		prsn:cell_measures = "area: areacello" ;
```

## Miscellaneous Errors - 9

 - Message: (7.3): Invalid type1: landuse - must be a variable name or valid area\_type
 - Models and Vars: CNRM-ESM2-1: Emon.sweLut
 - Files affected: 1
 - Example: [sweLut\_Emon\_CNRM-ESM2-1\_esm-hist\_r1i1p1f2\_gr\_185001-201412.nc](http://esg1.umr-cnrm.fr/thredds/dodsC/CMIP6_CNRM/CMIP/CNRM-CERFACS/CNRM-ESM2-1/esm-hist/r1i1p1f2/Emon/sweLut/gr/v20190215/sweLut_Emon_CNRM-ESM2-1_esm-hist_r1i1p1f2_gr_185001-201412.nc.html)

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
 - Example: [sweLut\_Emon\_UKESM1-0-LL\_deforest-globe\_r1i1p1f2\_gn\_185001-192912.nc](http://esgf-data3.ceda.ac.uk/thredds/dodsC/esg_cmip6/CMIP6/LUMIP/MOHC/UKESM1-0-LL/deforest-globe/r1i1p1f2/Emon/sweLut/gn/v20200203/sweLut_Emon_UKESM1-0-LL_deforest-globe_r1i1p1f2_gn_185001-192912.nc.html)

 - PID: [hdl:21.14100/d0f81944-6b28-4833-a89d-a265137ec425](http://hdl.handle.net/21.14100/d0f81944-6b28-4833-a89d-a265137ec425)

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
		sweLut:history = "2020-01-23T16:33:02Z altered by CMOR: Reordered dimensions, original order: landuse time lat lon. 2020-01-23T16:33:02Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20)." ;
		sweLut:missing_value = 1.e+20f ;
		sweLut:_FillValue = 1.e+20f ;
		sweLut:coordinates = "sector" ;
```

