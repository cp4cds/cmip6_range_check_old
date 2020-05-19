import matplotlib.pyplot as plt
import netCDF4

nc = netCDF4.Dataset( "snd_LImon_UKESM1-0-LL_historical_r1i1p1f2_gn_185001-194912.nc"  )


data = nc.variables["snd"]
print (data.shape)
lat = nc.variables["lat"]
lon = nc.variables["lon"]

fig, ax = plt.subplots( proj='robin', proj_kw={'lon_0': 180},)
# format options
ax.format(land=False, coast=True, innerborders=True, borders=True,
          labels=True, geogridlinewidth=0,)
map1 = ax.contourf(lon, lat, data[0,:,:],
                   cmap='IceFire', extend='both')
ax.colorbar(map1, loc='b', shrink=0.5, extendrect=True)
plt.show()
