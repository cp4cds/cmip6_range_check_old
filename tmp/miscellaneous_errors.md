# Miscellaneous Errors

## Miscellaneous Errors - 1

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type), (7.2): Invalid cell\_measures syntax
 - Models and Vars: CESM2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-FV2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-WACCM: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo, CESM2-WACCM-FV2: Omon.tauuo,Omon.tauvo,Omon.uo,Omon.vo
 - Files affected: 438
 - Example: [tauvo\_Omon\_CESM2-WACCM\_ssp245\_r1i1p1f1\_gr\_201501-206412.nc](http://esgf-data.ucar.edu/thredds/dodsC/esg_dataroot/CMIP6/ScenarioMIP/NCAR/CESM2-WACCM/ssp245/r1i1p1f1/Omon/tauvo/gr/v20190815/tauvo_Omon_CESM2-WACCM_ssp245_r1i1p1f1_gr_201501-206412.nc.html)

 - PID: [hdl:21.14100/8a4a4e79-e228-4f12-947e-20b469bd728a](http://hdl.handle.net/21.14100/8a4a4e79-e228-4f12-947e-20b469bd728a)

## Miscellaneous Errors - 2

 - Message: Attribute missing\_value of incorrect type (expecting 'Data Variable' type, got 'Numeric' type), (7.3): Invalid type1: sector - must be a variable name or valid area\_type
 - Models and Vars: CESM2: Emon.sweLut, CESM2-FV2: Emon.sweLut, CESM2-WACCM-FV2: Emon.sweLut
 - Files affected: 7
 - Example: [sweLut\_Emon\_CESM2-FV2\_historical\_r1i1p1f1\_gn\_190001-194912.nc](http://esgf-data.ucar.edu/thredds/dodsC/esg_dataroot/CMIP6/CMIP/NCAR/CESM2-FV2/historical/r1i1p1f1/Emon/sweLut/gn/v20191120/sweLut_Emon_CESM2-FV2_historical_r1i1p1f1_gn_200001-201412.nc.html)

 - PID: [hdl:21.14100/dc2a75bb-be49-40dc-8651-33ee04a44b9d](http://hdl.handle.net/21.14100/dc2a75bb-be49-40dc-8651-33ee04a44b9d)

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
 - Example: [snc\_LImon\_CESM2-WACCM-FV2\_historical\_r1i1p1f1\_gn\_195001-199912.nc](http://esgf-data.ucar.edu/thredds/dodsC/esg_dataroot/CMIP6/CMIP/NCAR/CESM2-WACCM-FV2/historical/r1i1p1f1/LImon/snc/gn/v20191120/snc_LImon_CESM2-WACCM-FV2_historical_r1i1p1f1_gn_200001-201412.nc.html)

 - PID: [hdl:21.14100/96bd17f8-70b4-44a4-88b9-e17db54ab478](http://hdl.handle.net/21.14100/96bd17f8-70b4-44a4-88b9-e17db54ab478)

## Miscellaneous Errors - 4

 - Message: (7.2): Invalid cell\_measures syntax
 - Models and Vars: AWI-CM-1-1-MR: Omon.tauuo, .. [10], AWI-ESM-1-1-LR: Omon.thetaoga, GFDL-CM4: AERmonZ.ta,AERmonZ.ua,EdayZ.ua,EdayZ.zg, GFDL-ESM4: AERmonZ.ta,AERmonZ.ua,EdayZ.ua,EdayZ.zg, MPI-ESM1-2-HR: Omon.tauuo, .. [6]
 - Files affected: 1509
 - Example: [zg\_EdayZ\_GFDL-ESM4\_piControl\_r1i1p1f1\_gr1z\_04210101-04401231.nc](http://esgdata.gfdl.noaa.gov/thredds/dodsC/gfdl_dataroot4/CMIP/NOAA-GFDL/GFDL-ESM4/piControl/r1i1p1f1/EdayZ/zg/gr1z/v20180701/zg_EdayZ_GFDL-ESM4_piControl_r1i1p1f1_gr1z_04210101-04401231.nc.html)

 - PID: [hdl:21.14100/7d3d22b0-b6a3-47c1-ab78-4bd477746d9f](http://hdl.handle.net/21.14100/7d3d22b0-b6a3-47c1-ab78-4bd477746d9f)

## Miscellaneous Errors - 5

 - Message: (7.2): cell\_measures variable areacella must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-ESM-1-1-LR: Amon.prsn, GFDL-AM4: Amon.clt, .. [36], GISS-E2-1-G: SImon.sithick, GISS-E2-1-G-CC: SImon.sithick, GISS-E2-1-H: SImon.sithick, IPSL-CM6A-LR: fx.mrsofc, MPI-ESM1-2-HR: Amon.clt, .. [52], MPI-ESM1-2-XR: Amon.clt, .. [52]
 - Files affected: 6902
 - Example: [rsdt\_Amon\_GFDL-AM4\_amip\_r1i1p1f1\_gr1\_198001-201412.nc](http://esgdata.gfdl.noaa.gov/thredds/dodsC/gfdl_dataroot3/CMIP/NOAA-GFDL/GFDL-AM4/amip/r1i1p1f1/Amon/rsdt/gr1/v20180807/rsdt_Amon_GFDL-AM4_amip_r1i1p1f1_gr1_198001-201412.nc.html)

 - PID: [hdl:21.14100/d2cf5aaf-e060-4eb7-8033-1e9c33477eb4](http://hdl.handle.net/21.14100/d2cf5aaf-e060-4eb7-8033-1e9c33477eb4)

## Miscellaneous Errors - 6

 - Message: (7.2): cell\_measures variable areacellg must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-ESM-1-1-LR: ImonAnt.prsn,ImonGre.prsn
 - Files affected: 22
 - Example: [prsn\_ImonAnt\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_187101-188012.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/AWI/AWI-ESM-1-1-LR/piControl/r1i1p1f1/ImonAnt/prsn/gn/v20200212/prsn_ImonAnt_AWI-ESM-1-1-LR_piControl_r1i1p1f1_gn_187101-188012.nc.html)

 - PID: [hdl:21.14100/31848572-4897-4e8e-b963-eaf166de7d8b](http://hdl.handle.net/21.14100/31848572-4897-4e8e-b963-eaf166de7d8b)

## Miscellaneous Errors - 7

 - Message: (7.2): cell\_measures variable areacello must either exist in this netCDF file or be named by the external\_variables attribute, (7.2): cell\_measures variable volcello must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-CM-1-1-MR: Omon.so,Omon.thetao, AWI-ESM-1-1-LR: Omon.thetao
 - Files affected: 373
 - Example: [thetao\_Omon\_AWI-CM-1-1-MR\_piControl\_r1i1p1f1\_gn\_286101-287012.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/AWI/AWI-CM-1-1-MR/piControl/r1i1p1f1/Omon/thetao/gn/v20181218/thetao_Omon_AWI-CM-1-1-MR_piControl_r1i1p1f1_gn_286101-287012.nc.html)

 - PID: [hdl:21.14100/39df4eea-58c7-466a-9280-8f9bfa22f9fa](http://hdl.handle.net/21.14100/39df4eea-58c7-466a-9280-8f9bfa22f9fa)

## Miscellaneous Errors - 8

 - Message: (7.2): cell\_measures variable areacello must either exist in this netCDF file or be named by the external\_variables attribute
 - Models and Vars: AWI-CM-1-1-MR: Oday.tos, .. [8], AWI-ESM-1-1-LR: Oday.tos, .. [5], CNRM-ESM2-1: Ofx.deptho
 - Files affected: 1051
 - Example: [tos\_Oday\_AWI-ESM-1-1-LR\_piControl\_r1i1p1f1\_gn\_18710101-18801231.nc](http://esgf3.dkrz.de/thredds/dodsC/cmip6/CMIP/AWI/AWI-ESM-1-1-LR/piControl/r1i1p1f1/Oday/tos/gn/v20200212/tos_Oday_AWI-ESM-1-1-LR_piControl_r1i1p1f1_gn_18710101-18801231.nc.html)

 - PID: [hdl:21.14100/678c9db2-924e-4571-a5f4-0c1f5dd908f9](http://hdl.handle.net/21.14100/678c9db2-924e-4571-a5f4-0c1f5dd908f9)

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
 - Example: [sweLut\_Emon\_UKESM1-0-LL\_ssp534-over-bgc\_r4i1p1f2\_gn\_205001-210012.nc](http://esgf-data3.ceda.ac.uk/thredds/dodsC/esg_cmip6/CMIP6/C4MIP/MOHC/UKESM1-0-LL/ssp534-over-bgc/r4i1p1f2/Emon/sweLut/gn/v20200501/sweLut_Emon_UKESM1-0-LL_ssp534-over-bgc_r4i1p1f2_gn_205001-210012.nc.html)

 - PID: [hdl:21.14100/7fa028c6-8993-4c49-93af-32b11f0886b6](http://hdl.handle.net/21.14100/7fa028c6-8993-4c49-93af-32b11f0886b6)

