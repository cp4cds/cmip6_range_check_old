# Standard Name Errors

## Standard Name Errors - 1

 - Message: (3.3): Invalid standard\_name: tendency\_of\_surface\_snow\_and\_ice\_amount\_due\_to\_sublimation
 - Models and Vars: EC-Earth3: Amon.sbl
 - Files affected: 158
 - Example: sbl\_Amon\_EC-Earth3\_historical\_r2i1p1f1\_gr\_188101-188112.nc

 - PID: [hdl:21.14100/67a2dc04-6cf6-45a5-95de-d7b4babc67e7](http://hdl.handle.net/21.14100/67a2dc04-6cf6-45a5-95de-d7b4babc67e7)

### ncdump sample

```
	float sbl(time, lat, lon) ;
		sbl:standard_name = "tendency_of_surface_snow_and_ice_amount_due_to_sublimation" ;
		sbl:long_name = "Surface Snow and Ice Sublimation Flux" ;
		sbl:comment = "The snow and ice sublimation flux is the loss of snow and ice mass per unit area from the surface resulting from their direct conversion to water vapor that enters the atmosphere." ;
		sbl:units = "kg m-2 s-1" ;
		sbl:cell_methods = "area: time: mean" ;
		sbl:cell_measures = "area: areacella" ;
		sbl:history = "2019-03-05T22:31:49Z altered by CMOR: Reordered dimensions, original order: lat lon time." ;
		sbl:missing_value = 1.e+20f ;
		sbl:_FillValue = 1.e+20f ;
```

## Standard Name Errors - 2

 - Message: (3.3): Invalid standard\_name: total\_water\_storage
 - Models and Vars: CNRM-CM6-1-HR: Emon.mrtws, IPSL-CM6A-LR: Emon.mrtws
 - Files affected: 20
 - Example: mrtws\_Emon\_IPSL-CM6A-LR\_hist-aer\_r10i1p1f1\_gr\_185001-202012.nc

 - PID: [hdl:21.14100/fab97c7f-6796-4eb5-b2cf-0572d3f3fc3b](http://hdl.handle.net/21.14100/fab97c7f-6796-4eb5-b2cf-0572d3f3fc3b)

### ncdump sample

```
	float mrtws(time, lat, lon) ;
		mrtws:long_name = "Total water storage in a grid cell" ;
		mrtws:units = "kg m-2" ;
		mrtws:online_operation = "average" ;
		mrtws:cell_methods = "area: mean where land time: mean" ;
		mrtws:interval_operation = "900 s" ;
		mrtws:interval_write = "1 month" ;
		mrtws:_FillValue = 1.e+20f ;
		mrtws:missing_value = 1.e+20f ;
		mrtws:coordinates = "" ;
		mrtws:standard_name = "total_water_storage" ;
		mrtws:description = "requested for C4MIP, OCMIP/OMIP, LUMIP, ScenarioMIP, DECK, DAMIP, GeoMIP, LS3MIP, ??" ;
		mrtws:history = "none" ;
		mrtws:cell_measures = "area: areacella" ;
```

