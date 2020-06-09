Cell Methods Errors
===================

Overview
========

Message | Model/variable | Count | Example
 :--:  |  :--:  |  :--:  |  :--: 
["(7.3): Invalid 'name' in cell\_methods attribute: month", "(7.3): Invalid 'name' in cell\_methods attribute: year"] | ('KACE-1-0-G', 'Amon.tasmax'), ('KACE-1-0-G', 'Amon.tasmin') | 2 | /badc/cmip6/data/CMIP6/ScenarioMIP/NIMS-KMA/KACE-1-0-G/ssp126/r1i1p1f1/Amon/tasmax/gr/v20200317/tasmax\_Amon\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_20150101-21001230.nc
['(7.3): Invalid cell\_method: mask', "(7.3): Invalid 'name' in cell\_methods attribute: (comment"] | ('KACE-1-0-G', 'SImon.sithick'), ('SAM0-UNICON', 'SImon.sithick') | 18 | /badc/cmip6/data/CMIP6/ScenarioMIP/NIMS-KMA/KACE-1-0-G/ssp126/r1i1p1f1/SImon/sithick/gr/v20200130/sithick\_SImon\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_201501-210012.nc
['(7.3): Invalid syntax for cell\_methods attribute'] | ('BCC-CSM2-MR', 'Amon.o3'), ('BCC-CSM2-MR', 'Amon.tasmax'), ('BCC-CSM2-MR', 'Amon.tasmin'), ('BCC-ESM1', 'Amon.o3'), ('BCC-ESM1', 'Amon.tasmax'), ('BCC-ESM1', 'Amon.tasmin'), ('FGOALS-g3', 'Amon.tasmax'), ('FGOALS-g3', 'Amon.tasmin'), ('INM-CM4-8', 'Amon.tasmax'), ('INM-CM4-8', 'Amon.tasmin'), ('INM-CM5-0', 'Amon.tasmax'), ('INM-CM5-0', 'Amon.tasmin'), ('SAM0-UNICON', 'Amon.tasmax'), ('SAM0-UNICON', 'Amon.tasmin') | 568 | /badc/cmip6/data/CMIP6/AerChemMIP/BCC/BCC-ESM1/hist-piNTCF/r1i1p1f1/Amon/tasmax/gn/v20190621/tasmax\_Amon\_BCC-ESM1\_hist-piNTCF\_r1i1p1f1\_gn\_185001-201412.nc
['(7.3): Invalid unit hours, in cell\_methods comment'] | ('KACE-1-0-G', '3hr.huss'), ('KACE-1-0-G', '3hr.tas'), ('KACE-1-0-G', '3hr.uas'), ('KACE-1-0-G', '3hr.vas') | 38 | /badc/cmip6/data/CMIP6/ScenarioMIP/NIMS-KMA/KACE-1-0-G/ssp370/r1i1p1f1/3hr/tas/gr/v20191225/tas\_3hr\_KACE-1-0-G\_ssp370\_r1i1p1f1\_gr\_207501010130-208412302230.nc
["(7.3): Invalid 'name' in cell_methods attribute: month", "(7.3): Invalid 'name' in cell_methods attribute: year"]
===================================================================================================================

```
	float tasmax(time, lat, lon) ;
		tasmax:standard_name = "air_temperature" ;
		tasmax:long_name = "Daily Maximum Near-Surface Air Temperature" ;
		tasmax:units = "K" ;
		tasmax:cell_methods = "area: mean time: maximum (interval: 1 day) month: year: mean" ;
		tasmax:coordinates = "height" ;
```

['(7.3): Invalid cell_method: mask', "(7.3): Invalid 'name' in cell_methods attribute: (comment"]
=================================================================================================

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

['(7.3): Invalid syntax for cell_methods attribute']
====================================================

```
	float tasmax(time, lat, lon) ;
		tasmax:standard_name = "air_temperature" ;
		tasmax:long_name = "Daily Maximum Near-Surface Air Temperature" ;
		tasmax:comment = "maximum near-surface (usually, 2 meter) air temperature (add cell_method attribute \'time: max\')" ;
		tasmax:units = "K" ;
		tasmax:original_name = "TREFMXAV" ;
		tasmax:cell_methods = "area: mean time: maximum (interval: 20 minutes) within days time: mean over days" ;
		tasmax:cell_measures = "area: areacella" ;
		tasmax:history = "2019-06-21T07:16:28Z altered by CMOR: Treated scalar dimension: \'height\'." ;
		tasmax:coordinates = "height" ;
		tasmax:missing_value = 1.e+20f ;
		tasmax:_FillValue = 1.e+20f ;
```

['(7.3): Invalid unit hours, in cell_methods comment']
======================================================

```
	float tas(time, lat, lon) ;
		tas:standard_name = "air_temperature" ;
		tas:long_name = "Near-Surface Air Temperature" ;
		tas:comment = "near-surface (usually, 2 meter) air temperature" ;
		tas:units = "K" ;
		tas:original_name = "m01s03i236" ;
		tas:cell_methods = "area: mean time: point (interval: 3 hours, Instantaneous)" ;
		tas:cell_measures = "area: areacella" ;
		tas:history = "2019-12-25T02:16:15Z altered by CMOR: Treated scalar dimension: \'height\'. 2019-12-25T02:16:15Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20)." ;
		tas:coordinates = "height" ;
		tas:missing_value = 1.e+20f ;
		tas:_FillValue = 1.e+20f ;
```

