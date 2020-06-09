Cell Methods Errors
===================

Overview
========

Message | Model/variable | Count | Example
 :--:  |  :--:  |  :--:  |  :--: 
["(7.3): Invalid 'name' in cell\_methods attribute: month", "(7.3): Invalid 'name' in cell\_methods attribute: year"] | ('KACE-1-0-G', 'Amon.tasmax'), ('KACE-1-0-G', 'Amon.tasmin') | 2 | /badc/cmip6/data/CMIP6/ScenarioMIP/NIMS-KMA/KACE-1-0-G/ssp126/r1i1p1f1/Amon/tasmax/gr/v20200317/tasmax\_Amon\_KACE-1-0-G\_ssp126\_r1i1p1f1\_gr\_20150101-21001230.nc
['(7.3): Invalid cell\_method: mask', "(7.3): Invalid 'name' in cell\_methods attribute: (comment"] | ('KACE-1-0-G', 'SImon.sithick'), ('SAM0-UNICON', 'SImon.sithick') | 18 | /badc/cmip6/data/CMIP6/CMIP/SNU/SAM0-UNICON/historical/r1i1p1f1/SImon/sithick/gn/v20190323/sithick\_SImon\_SAM0-UNICON\_historical\_r1i1p1f1\_gn\_198001-198912.nc
['(7.3): Invalid syntax for cell\_methods attribute'] | ('BCC-CSM2-MR', 'Amon.o3'), ('BCC-CSM2-MR', 'Amon.tasmax'), ('BCC-CSM2-MR', 'Amon.tasmin'), ('BCC-ESM1', 'Amon.o3'), ('BCC-ESM1', 'Amon.tasmax'), ('BCC-ESM1', 'Amon.tasmin'), ('FGOALS-g3', 'Amon.tasmax'), ('FGOALS-g3', 'Amon.tasmin'), ('INM-CM4-8', 'Amon.tasmax'), ('INM-CM4-8', 'Amon.tasmin'), ('INM-CM5-0', 'Amon.tasmax'), ('INM-CM5-0', 'Amon.tasmin'), ('SAM0-UNICON', 'Amon.tasmax'), ('SAM0-UNICON', 'Amon.tasmin') | 568 | /badc/cmip6/data/CMIP6/CMIP/BCC/BCC-CSM2-MR/esm-piControl/r1i1p1f1/Amon/o3/gn/v20181122/o3\_Amon\_BCC-CSM2-MR\_esm-piControl\_r1i1p1f1\_gn\_185001-185012-clim.nc
['(7.3): Invalid unit hours, in cell\_methods comment'] | ('KACE-1-0-G', '3hr.huss'), ('KACE-1-0-G', '3hr.tas'), ('KACE-1-0-G', '3hr.uas'), ('KACE-1-0-G', '3hr.vas') | 38 | /badc/cmip6/data/CMIP6/CMIP/NIMS-KMA/KACE-1-0-G/historical/r1i1p1f1/3hr/uas/gr/v20190913/uas\_3hr\_KACE-1-0-G\_historical\_r1i1p1f1\_gr\_200001010130-200912302230.nc
["(7.3): Invalid 'name' in cell_methods attribute: month", "(7.3): Invalid 'name' in cell_methods attribute: year"]
===================================================================================================================

'''
	float tasmax(time, lat, lon) ;

		tasmax:standard_name = "air_temperature" ;

		tasmax:long_name = "Daily Maximum Near-Surface Air Temperature" ;

		tasmax:units = "K" ;

		tasmax:cell_methods = "area: mean time: maximum (interval: 1 day) month: year: mean" ;

		tasmax:coordinates = "height" ;

'''

['(7.3): Invalid cell_method: mask', "(7.3): Invalid 'name' in cell_methods attribute: (comment"]
=================================================================================================

'''
	float sithick(time, j, i) ;

		sithick:standard_name = "sea_ice_thickness" ;

		sithick:long_name = "Sea Ice Thickness" ;

		sithick:comment = "Actual (floe) thickness of sea ice (NOT volume divided by grid area as was done in CMIP5)" ;

		sithick:units = "m" ;

		sithick:history = "rewrote by cmor via python script 2019-04-01T06:10:48Z altered by CMOR: replaced missing value flag (1e+30) with standard missing value (1e+20)." ;

		sithick:cell_methods = "area: time: mean (interval: 1 month) where sea_ice (comment: mask=siconc)" ;

		sithick:cell_measures = "area: areacello" ;

		sithick:missing_value = 1.e+20f ;

		sithick:_FillValue = 1.e+20f ;

		sithick:coordinates = "latitude longitude" ;

'''

['(7.3): Invalid syntax for cell_methods attribute']
====================================================

'''
	float o3(time, plev, lat, lon) ;

		o3:standard_name = "mole_fraction_of_ozone_in_air" ;

		o3:long_name = "Mole Fraction of O3" ;

		o3:comment = "Mole fraction is used in the construction mole_fraction_of_X_in_Y, where X is a material constituent of Y." ;

		o3:units = "mol mol-1" ;

		o3:original_name = "O3VMR" ;

		o3:cell_methods = "area: mean time: mean (interval: 5 minutes) within years time: mean over years" ;

		o3:cell_measures = "area: areacella" ;

		o3:missing_value = 1.e+20f ;

		o3:_FillValue = 1.e+20f ;

'''

['(7.3): Invalid unit hours, in cell_methods comment']
======================================================

'''
	float uas(time, lat, lon) ;

		uas:standard_name = "eastward_wind" ;

		uas:long_name = "Eastward Near-Surface Wind" ;

		uas:comment = "Eastward component of the near-surface (usually, 10 meters)  wind" ;

		uas:units = "m s-1" ;

		uas:original_name = "m01s03i225" ;

		uas:cell_methods = "area: mean time: point (interval: 3 hours, Instantaneous)" ;

		uas:cell_measures = "area: areacella" ;

		uas:history = "2019-09-13T08:34:53Z altered by CMOR: Treated scalar dimension: \'height\'. 2019-09-13T08:34:53Z altered by CMOR: replaced missing value flag (-1.07374e+09) with standard missing value (1e+20)." ;

		uas:coordinates = "height" ;

		uas:missing_value = 1.e+20f ;

		uas:_FillValue = 1.e+20f ;

'''

