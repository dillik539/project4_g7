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
from metadata_manager import MetadataManager
import pysal
import os

#https://github.com/johan/world.geo.json geojson data

ui = user_interface
api = ApiController()
sources = api.build_sources()
mgr = MetadataManager('geo_data_for_news_choropleth.txt')
# result_map = dict.fromkeys([k['id'] for k in json.load(open('country_data.txt'))['features']], 0)
# geo_json_data = requests.get('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
# data = geo_json_data.json()
#
# for k in data['features']:
#     if k['id'] == '-99':
#         k['id'] = 'CYP'
#
# json_geo_file = None
# json_geo_data = None


# with open('country_data.txt', 'w') as outfile:
#     json.dump(data, outfile)


def main():
    #
    # test_map_and_data()
    # test_geopandas()
    #
    # keys=[k['id'] for k in json.load(open('country_data.txt'))['features']]
    # for k in keys:
    #     ui.message(str(k))


    mgr.get_geo_data()
    mgr.fix_cyprus_country_code()
    write_json_to_file(mgr.json_filename, mgr.json_geo_data)
    mgr.build_query_results_dict()
    menu_controller(ui.top_menu())


    # json_geo_file = 'json_geo_data.txt'
    # json_geo_data = get_geo_data()
    # write_json_to_file(json_geo_file, json_geo_data)
    # query_results_dict = dict.fromkeys([k['id'] for k in json.load(open(json_geo_file))['features']], 0)


    menu_controller(ui.top_menu())

def write_json_to_file(filename, json_data):
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile)

# def get_geo_data():
#     geo_data_request = requests.get('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
#     request_to_json = geo_data_request.json()
#     json_geo_data = fix_cyprus_country_code(request_to_json)
#     return json_geo_data

def fix_cyprus_country_code(json_geo_data):
    for key in json_geo_data:
        if key['id'] == '-99':
            key['id'] = 'CYP'
    return json_geo_data

# def test_geopandas():
#
#     test_map = folium.Map([0,0], tiles='Mapbox Bright', zoom_start=4)
#
#
#     test_article_count_dict = dict.fromkeys([k for k in result_map], 0)
#
#     for k in test_article_count_dict:
#
#         test_article_count_dict[k] = random.randint(1, 100)
#
#
#     world = gpd.read_file('country_data.txt')
#     article_values = pd.Series(test_article_count_dict)
#     print(article_values)
#
#     world['article_count'] = world['id'].map(article_values)
#     world.head() # keys are ID NAME GEOGRAPHY
#     print(world)
#
#     world.plot(column='article_count')
#     test_json_data = world.to_json()
#     with open('geopandas_dataframe_test_output', 'w') as f:
#         json.dump(test_json_data, f)
#
#     threshold_scale = np.linspace(article_values.values.min(), article_values.values.max(), 6, dtype=int).tolist()
#
#     test_map.choropleth(geo_str=data,
#                         data=world,
#                         columns=['id','article_count'],
#                         key_on='feature.id',
#                         fill_color='YlGn',
#                         fill_opacity=0.7,
#                         line_opacity=0.2,
#                         threshold_scale=threshold_scale
#                         )
#
#     folium.LayerControl().add_to(test_map)
#     test_map.save('gpd_test_map_.html')


# def test_map_and_data():

    # map = folium.Map([0,0], zoom_start=4)
    #
    # folium.GeoJson(
    #     'country_data.txt',
    #     style_function=lambda feature: {
    #     'fillColor': '#dc322f' if 's' in feature['properties']['name'].lower() else 'green',
    #     'color': 'black',
    #     'weight': 2,
    #     'dashArray': '5, 5'
    # }).add_to(map)
    #
    # result_map['USA'] = 10
    # result_map['CND'] = 5
    # result_map['SWE'] = 2
    # for k in result_map:
    #     ui.message(k + ': ' + str(result_map[k]))
    #
    # with open('country_data.txt') as f:
    #     get_id = json.load(f)
    #
    # countries = []
    #
    # article_count = [result_map[x] for x in (get_id['features']['id'])]
    # article_df = pd.DataFrame({'Article_Count': article_count}, dtype=int)
    #
    #
    # country_df = pd.DataFrame({'Country': [k for k in result_map]}, dtype=str)
    #
    #
    # merged = pd.merge(article_df, country_df, on='Country')
    # for k in merged:
    #     ui.message(k + ': ' + str(merged[k]))
    #
    #
    # map.save('test_map.html')
    # map.render()



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
        # result_map['None'] = 1
        ui.message('No Source Country Matched')
    else:
        mgr.query_data_dict[source_country] += 1
    # else:
    #     if result_map.keys().__contains__(source_country):
    #         if result_map[source_country] is None:
    #             result_map[source_country] = 1
    #         else:
    #             result_map[source_country] += 1
    #             ui.message('For already present key of ' + str(source_country) + ', value = ' + str(result_map[source_country]))
    #     elif not result_map.keys().__contains__(source_country):
    #         result_map[source_country] = None
    #         # ui.message('For new key of ' + str(source_country) + ', value = ' + str(result_map[source_country]))
    #     else:
    #         ui.message('def map_source should not have reached this')


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
            if source_country is not None:
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

    # formatted_dict = preformat_df_dict()
    # for k in formatted_dict:
    #     ui.message(k + ": " + str(formatted_dict[k]))

    # df_and_totals = build_dataframe(result_map)
    # ui.message('KEYS: ' + (dataframe.keys()))
    # ui.message('VALUES: ' + str(dataframe.values))



    # super_data = dict(ChainMap(dataframe, result_map))
    # super_data = dict(ChainMap(dataframe, data))
    # ui.message('super_data[ITA]: ' + str(super_data['ITA']))
    # ui.message('super_data KEYS: ' + str(super_data.keys()))
    # ui.message('super_data VALUES: ' + str(super_data.values()))

    # for k in super_data:
    #     ui.message('super_data key: ' + k + ' value: ' + str(super_data[k]))

    # map_dataframe(super_data)
    # map_dataframe(df_and_totals[0], df_and_totals[1])
    build_choropleth()



def build_choropleth():
    world_df = gpd.read_file(mgr.json_filename)
    choro_map = folium.Map([0,0], tiles='Mapbox Bright', zoom_start=4)
    articles_per_country = pd.Series(mgr.query_data_dict)
    world_df['article_count']=world_df['id'].map(articles_per_country)
    world_df.head()
    world_df.plot(column='article_count')
    threshold_scale = np.linspace(articles_per_country.values.min(), articles_per_country.values.max(), 6, dtype=int).tolist()

    choro_map.choropleth(geo_str=mgr.json_geo_data,
                        data=world_df,
                        columns=['id', 'article_count'],
                        key_on='feature.id',
                        fill_color='YlOrRd', #YlGrBu
                        fill_opacity=0.7,
                        line_opacity=0.2,
                        threshold_scale=threshold_scale
                        )



    folium.TileLayer("MapQuest Open Aerial").add_to(choro_map)
    folium.TileLayer("stamenwatercolor").add_to(choro_map)
    folium.TileLayer("cartodbdark_matter").add_to(choro_map)
    folium.TileLayer("Mapbox Control Room").add_to(choro_map)
    folium.LayerControl().add_to(choro_map)



    choro_map.save('choropleth_map.html')
    choro_map.render()


def query_all_from_date_range():
    ui.message('in query_all_from_date_range')


def quit_program():
    sys.exit('Farewell digital world...\n')



# def preformat_df_dict():
#     ordered_dict = OrderedDict([
#         ('Country', [k for k in result_map]),
#         ('Article_Count', [result_map[k] for k in result_map])])
#
#     return ordered_dict

    # ordered_dict = OrderedDict((k, result_map[k]) for k in result_map)
    # return ordered_dict



# def build_dataframe(data_dict):
#
#     world = gpd.read_file('country_data.txt')
#     article_totals = pd.Series(result_map)
#     world['article_count'] = world['id'].map(article_totals)
#     return world,article_totals,


    # df = pd.DataFrame.from_dict(data_dict)
    # for key in df['Country']:
    #     ui.message('df key: ' + str(key))
    #     if key not in result_map:
    #         ui.message('Key Not Found in Result Map ' + str(key))
    # return df




    # counter = 0
    # for k in data_dict:
    #     counter+=1
    #
    # index = [x for x in range(counter)]
    # df = pd.DataFrame.from_records(data_dict, index)



    # dataFrame = pd.Series(data_dict).to_frame() #todo try me next
    # return df

# def map_dataframe(world, query_totals):
#
#     # countries = os.path.join('data', 'countries.geo.json')
#     # geo_json_data = geojson.load(open(countries))
#     world.head()
#     world.plot(column='article_count')
#     threshold_scale = np.linspace(
#         query_totals.values.min(),
#         query_totals.values.max(),
#         10, dtype=int).tolist()
#
#     data_map = folium.Map(location=[0,0], tiles='Mapbox Control Room', zoom_start=4)
#     data_map.choropleth(geo_str=data,
#                         data=world,
#                         columns=['id', 'article_count'],
#                         key_on='feature.id',
#                         fill_color='YlGnBu',
#                         fill_opacity=0.7,
#                         line_opacity=0.2,
#                         threshold_scale=threshold_scale
#                         )
#     folium.LayerControl().add_to(data_map)
#
#     # folium.GeoJson('country_data.txt').add_to(data_map)
#     # data_map.save(os.path.join('results', 'GeoJSON_and_choropleth_0.html'))
#     # data_map.choropleth(data=df,
#     #                     # columns=['feature.id', 'feature.properties.article_count'],
#     #                     columns=['Country', 'Article_Count'],
#     #                     key_on='feature.id',
#     #                     fill_color='YlGn',
#     #                     fill_opacity=0.7,
#     #                     line_opacity=0.3)
#     # ui.message('Past data_map.choropleth(), before data_map.render()')
#     data_map.save('data_map.html')
#     data_map.render()


if __name__ == '__main__':
    main()

