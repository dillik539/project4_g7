import random
import sys
from collections import OrderedDict, ChainMap
import folium
import math

from folium.colormap import linear

import user_interface
from api_controller import ApiController
import pycountry
import pandas as pd
import geopandas as gpd
import json
import requests
import numpy as np
import pysal
import os

#https://github.com/johan/world.geo.json geojson data

ui = user_interface
api = ApiController()
sources = api.build_sources()
result_map = dict.fromkeys([k['id'] for k in json.load(open('country_data.txt'))['features']], 0)

invalid_key = None
for k in result_map:
    if k == '-99':
        invalid_key = k

# result_map.pop(invalid_key)
# geo_json_data = json.load(open('countries.geo.json'))

geo_json_data = requests.get('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
data = geo_json_data.json()
data2 = {}
for k in data['features']:
    if k['id'] == '-99':
        ui.message('bad key = ')
        k['id'] = 'CYP'
        ui.message('updated to: ' + k['id'])

        #todo remove this fucking thing
with open('country_data.txt', 'w') as outfile:
    json.dump(data, outfile)




def main():
    #
    # test_map_and_data()
    test_geopandas()

    # keys=[k['id'] for k in json.load(open('country_data.txt'))['features']]
    # for k in keys:
    #     ui.message(str(k))
    #
    #
    #
    #
    # menu_controller(ui.top_menu())


def test_geopandas():

    test_map = folium.Map([0,0], tiles='Mapbox Control Room', zoom_start=4)
    result_map['USA']=5

    test_article_count_dict = dict.fromkeys([k for k in result_map], 0)
    for k in test_article_count_dict:
        # ui.message('Key for article_values: ' + k)
        test_article_count_dict[k] = random.randint(1, 100)
    # articles = gpd.GeoSeries(test_article_count_dict)




    world = gpd.read_file('country_data.txt')
    article_values = pd.Series(test_article_count_dict)
    print(article_values)
    # article_values = pd.DataFrame(test_article_count_dict)
    # for k in article_values:
    #     ui.message('Article: ' + str(k) + ' Value: ' + str(article_values[k]))
    # ui.message(str(article_values))
    # ui.message(str(world))
    # world.insert(loc=2, column='article_count', value=article_values)
    world['article_count'] = world['id'].map(article_values)
    world.head() # keys are ID NAME GEOGRAPHY
    print(world)
    # world.plot(column='article_count', cmap='OrRd', scheme='quantiles')
    world.plot(column='article_count')

    test_json_data = world.to_json()
    with open('geopandas_dataframe_test_output', 'w') as f:
        json.dump(test_json_data, f)

    # ui.message(world.geometry.name)



    # folium.GeoJson(world, style_function=lambda feature: {
    #     'color': 'black',
    #     'weight': 2,
    #     'dashArray': '5, 5'
    # }).add_to(test_map)

    # folium.GeoJson(world).add_to(test_map)



    threshold_scale = np.linspace(article_values.values.min(), article_values.values.max(), 6, dtype=int).tolist()

    test_map.choropleth(geo_str=data,
                        # data_out='test_data_out.json',
                        data=world,
                        columns=['id','article_count'],
                        key_on='feature.id',
                        fill_color='YlGn',
                        fill_opacity=0.7,
                        line_opacity=0.2,
                        threshold_scale=threshold_scale
                        )

    folium.LayerControl().add_to(test_map)

    # print(geo_json_data.json())

    test_map.save('gpd_test_map_.html')
    # test_map.render()

def test_map_and_data():

    map = folium.Map([0,0], zoom_start=4)

    folium.GeoJson(
        'country_data.txt',
        style_function=lambda feature: {
        'fillColor': '#dc322f' if 's' in feature['properties']['name'].lower() else 'green',
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    }).add_to(map)

    result_map['USA'] = 10
    result_map['CND'] = 5
    result_map['SWE'] = 2
    for k in result_map:
        ui.message(k + ': ' + str(result_map[k]))

    with open('country_data.txt') as f:
        get_id = json.load(f)

    countries = []

    article_count = [result_map[x] for x in (get_id['features']['id'])]
    article_df = pd.DataFrame({'Article_Count': article_count}, dtype=int)


    country_df = pd.DataFrame({'Country': [k for k in result_map]}, dtype=str)


    merged = pd.merge(article_df, country_df, on='Country')
    for k in merged:
        ui.message(k + ': ' + str(merged[k]))


    map.save('test_map.html')
    map.render()

def my_color_function(feature):
    ui.message('feature: ' + str(feature))
    if feature > 50:
        return '#dc322f'
    else:
        return '#008000'


def menu_controller(menu_selection):

    selection_dict = {
        '1': execute_query('headlines'),
        '2': execute_query('all'),
        '3': query_all_from_date_range,
        'q': quit_program,
    }

    call_function = selection_dict.get(menu_selection)

    if menu_selection is None:
        ui.message('Invalid Selection, Try Again')
    else:
        return call_function()

def get_source_country(source_name):

    for source in sources:
        if source.name == source_name:
            # ui.message('source: ' + source.name + '\ncountry: ' + source.country)
            alpha_2_code = source.country
            # ui.message(alpha_2_code.upper())

            country = pycountry.countries.get(alpha_2=alpha_2_code.upper())
            # ui.message('Full Country Conversion: ' + str(country.official_name))
            # alpha_3_code = country.alpha_3
            # ui.message('alpha_3: ' + str(alpha_3_code))
            return country.alpha_3
        # todo for cache: once a source-country is queried, store it in a dict?


def map_source(source_country):



    if type(source_country) is None:
        result_map['None'] = 1
        ui.message('No Source Country Matched')
    else:
        if result_map.keys().__contains__(source_country):
            if result_map[source_country] is None:
                result_map[source_country] = 1
            else:
                result_map[source_country] += 1
                ui.message('For already present key of ' + str(source_country) + ', value = ' + str(result_map[source_country]))
        elif not result_map.keys().__contains__(source_country):
            result_map[source_country] = None
            # ui.message('For new key of ' + str(source_country) + ', value = ' + str(result_map[source_country]))
        else:
            ui.message('def map_source should not have reached this')


def execute_query(query_type):

    query_argument = ui.get_user_query()
    article_data = api.query_api(query_argument, query_type)
    # query_metadata = QueryMetadata(query_argument, article_data, {})
    # try:
    #     for article in article_data:
    #         ui.message(article.__str__())
    #         article_source_name = article.source
    #         try:
    #             source_country = get_source_country(article_source_name)
    #             map_source(source_country)
    #         except AttributeError:
    #             ui.message('Error from article: ' + article.__str__())
    #             ui.message('Article Source Type: ' + str(type(article.source)))
    #         # ui.message('source_country: ' + source_country)
    #
    #         # data_map = folium.Map(location=[0, 0], tiles='Mapbox Control Room', zoom_start=0)
    #         # folium.GeoJson(geo_json_data).add_to(data_map)
    #         # data_map.save(os.path.join('results', 'GeoJSON_and_choropleth_0.html'))
    #         # data_map.choropleth(geo_path='countries.geo.json', data=df,
    #         #                columns=['Country', 'Article_Count'],
    #         #                key_on='feature.properties.iso_a3',
    #         #                fill_color='YlGnBu', fill_opacity=0.7, line_opacity=0.2)
    #         # data_map.render()
    #         # map_dataframe(build_dataframe(preformat_df_dict()))
    #         # ui.message('(def execute_query) source_country from execute_query: ' + str(source_country))
    #
    #
    #         # for k in query_metadata.result_map:
    #         #     try:
    #         #         ui.message(k + ': ' + str(query_metadata.result_map[k]))
    #         #     except TypeError:
    #         #         ui.message('Error parsing metadata result map entry.')
    #
    #     # query_metadata.map_dataframe(query_metadata.build_dataframe(query_metadata.preformat_df_dict()))
    #
    #     formatted_dict = preformat_df_dict()
    #     for k in formatted_dict:
    #         ui.message(k + ": " + str(formatted_dict[k]))
    #
    #     dataframe = build_dataframe(formatted_dict)
    #     ui.message('KEYS: ' + (dataframe.keys()))
    #     ui.message('VALUES: ' + str(dataframe.values))
    #
    #     map_dataframe(dataframe)
    #
    #
    #
    # except KeyError:
    #     ui.message('Error mapping source')
    for article in article_data:
        ui.message(article.__str__())
        article_source_name = article.source
        try:
            source_country = get_source_country(article_source_name)
            map_source(source_country)
        except AttributeError:
            ui.message('Error from article: ' + article.__str__())
            ui.message('Article Source Type: ' + str(type(article.source)))
            # ui.message('source_country: ' + source_country)

            # data_map = folium.Map(location=[0, 0], tiles='Mapbox Control Room', zoom_start=0)
            # folium.GeoJson(geo_json_data).add_to(data_map)
            # data_map.save(os.path.join('results', 'GeoJSON_and_choropleth_0.html'))
            # data_map.choropleth(geo_path='countries.geo.json', data=df,
            #                columns=['Country', 'Article_Count'],
            #                key_on='feature.properties.iso_a3',
            #                fill_color='YlGnBu', fill_opacity=0.7, line_opacity=0.2)
            # data_map.render()
            # map_dataframe(build_dataframe(preformat_df_dict()))
            # ui.message('(def execute_query) source_country from execute_query: ' + str(source_country))


            # for k in query_metadata.result_map:
            #     try:
            #         ui.message(k + ': ' + str(query_metadata.result_map[k]))
            #     except TypeError:
            #         ui.message('Error parsing metadata result map entry.')

    # query_metadata.map_dataframe(query_metadata.build_dataframe(query_metadata.preformat_df_dict()))

    formatted_dict = preformat_df_dict()
    # for k in formatted_dict:
    #     ui.message(k + ": " + str(formatted_dict[k]))

    dataframe = build_dataframe(formatted_dict)
    # ui.message('KEYS: ' + (dataframe.keys()))
    # ui.message('VALUES: ' + str(dataframe.values))



    # super_data = dict(ChainMap(dataframe, result_map))
    super_data = dict(ChainMap(dataframe, data))
    # ui.message('super_data[ITA]: ' + str(super_data['ITA']))
    ui.message('super_data KEYS: ' + str(super_data.keys()))
    ui.message('super_data VALUES: ' + str(super_data.values()))

    # for k in super_data:
    #     ui.message('super_data key: ' + k + ' value: ' + str(super_data[k]))

    map_dataframe(super_data)
    # map_dataframe(dataframe)




def query_all_from_date_range():
    ui.message('in query_all_from_date_range')


def quit_program():
    sys.exit('Farewell digital world...\n')



def preformat_df_dict():
    ordered_dict = OrderedDict([
        ('Country', [k for k in result_map]),
        ('Article_Count', [result_map[k] for k in result_map])])

    return ordered_dict

    # ordered_dict = OrderedDict((k, result_map[k]) for k in result_map)
    # return ordered_dict



def build_dataframe(data_dict):
    df = pd.DataFrame.from_dict(data_dict)
    for key in df['Country']:
        ui.message('df key: ' + str(key))
        if key not in result_map:
            ui.message('Key Not Found in Result Map ' + str(key))
    return df




    # counter = 0
    # for k in data_dict:
    #     counter+=1
    #
    # index = [x for x in range(counter)]
    # df = pd.DataFrame.from_records(data_dict, index)



    # dataFrame = pd.Series(data_dict).to_frame() #todo try me next
    # return df

def map_dataframe(df):

    # countries = os.path.join('data', 'countries.geo.json')
    # geo_json_data = geojson.load(open(countries))

    data_map = folium.Map(location=[0,0], tiles='Mapbox Control Room', zoom_start=4)
    folium.GeoJson('country_data.txt').add_to(data_map)
    # data_map.save(os.path.join('results', 'GeoJSON_and_choropleth_0.html'))
    data_map.choropleth(data=df,
                        # columns=['feature.id', 'feature.properties.article_count'],
                        columns=['Country', 'Article_Count'],
                        key_on='feature.id',
                        fill_color='YlGn',
                        fill_opacity=0.7,
                        line_opacity=0.3)
    ui.message('Past data_map.choropleth(), before data_map.render()')
    data_map.save('data_map.html')
    data_map.render()


if __name__ == '__main__':
    main()

