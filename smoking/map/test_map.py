
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import json

# Make this plot larger.
plt.figure(figsize=(10,8))

# eq_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
#               lat_0=0, lon_0=-100)
# eq_map.drawcoastlines()
# eq_map.drawcountries()
# eq_map.fillcontinents(color = 'gray')
# eq_map.drawmapboundary()
# eq_map.drawmeridians(np.arange(0, 360, 30))
# eq_map.drawparallels(np.arange(-90, 90, 30))
#
min_marker_size = 2.5

m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,projection='lcc',lat_1=33,lat_2=45,lon_0=-95,resolution='c')
m.drawcoastlines()
m.drawstates()
m.drawcountries()
max_size=80

with open('random_center.json') as f_in:
    _random = json.load(f_in)['center']

with open('smoke_center.json') as f_in2:
    _smoke = json.load(f_in2)['center']
print _random
print _smoke

# for lon, lat,in zip(lons, lats):
for geo in _random:
    x,y = m(geo[0], geo[1])
    msize = 3 * min_marker_size
    marker_string = 'go'
    m.plot(x, y, marker_string, markersize=msize)

for geo in _smoke:
    x,y = m(geo[0], geo[1])
    msize = 4 * min_marker_size
    marker_string = 'ro'
    m.plot(x, y, marker_string, markersize=msize)


plt.title('Smoking')
#
plt.show()
