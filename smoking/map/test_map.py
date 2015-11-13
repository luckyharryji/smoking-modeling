from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import json

class Map(object):
    def __init__(self):
        self.m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,projection='lcc',lat_1=33,lat_2=45,lon_0=-95,resolution='c')
        self.min_marker_size = 2.5


    def initial_map(self):
        self.m.drawcoastlines()
        self.m.drawstates()
        self.m.drawcountries()


    def plot_point(self, URL, r, marker):
        with open(URL) as f_in:
            _points = json.load(f_in)['center']
        for geo in _points:
            x,y = self.m(geo[0], geo[1])
            msize = r * self.min_marker_size
            marker_string = marker
            self.m.plot(x, y, marker_string, markersize=msize)


if __name__ == '__main__' :
    plt.figure(figsize=(10,8))
    new_map = Map()
    new_map.initial_map()
    new_map.plot_point('random_center.json',3,'go')
    new_map.plot_point('smoke_center.json',4,'ro')
    plt.title('Smoking')
    plt.show()
