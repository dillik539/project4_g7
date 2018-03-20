
import folium

class Map(object):

    def __init__(self, latitude, longitude):
        self.lat = latitude
        self.map = self.build_map()
        self.long = longitude



    def build_map(self):
        f_map = folium.Map(location=[self.lat, self.long])
        f_map.choropleth(geo_path='world.geojson')
        return f_map
