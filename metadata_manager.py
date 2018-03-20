import requests
import json


class MetadataManager(object):

    def __init__(self, json_filename, request_geo_data=None, json_geo_data=None, query_data_dict={}):
        self.json_filename=json_filename
        self.request_geo_data=request_geo_data
        self.json_geo_data=json_geo_data
        self.query_data_dict=query_data_dict

    def __str__(self):
        with open(self.json_filename) as f:
            return f

    def get_geo_data(self):

        self.request_geo_data = requests.get('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')

        self.json_geo_data = self.request_geo_data.json()


    def build_query_results_dict(self):
        self.query_data_dict = dict.fromkeys([k['id'] for k in json.load(open(self.json_filename))['features']], 0)

    def fix_cyprus_country_code(self):
        for key in self.json_geo_data:
            if self.json_geo_data[key] == '-99':
                self.json_geo_data[key] = 'CYP'
