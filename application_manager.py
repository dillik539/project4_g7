import datetime
import json
# import random
import sys
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import pycountry


import log_controller
import user_interface
from api_controller import ApiController
from metadata_manager import MetadataManager

#https://github.com/johan/world.geo.json geojson data

ui = user_interface
api = ApiController()
sources = api.build_sources()
log = log_controller

mgr = MetadataManager('geo_data_for_news_choropleth.txt')

# @Gooey(advanced=False) #for future implementation
def main():

    mgr.get_geo_data()
    mgr.fix_cyprus_country_code()
    write_json_to_file(mgr.json_filename, mgr.json_geo_data)
    mgr.build_query_results_dict()
    menu_controller(ui.top_menu())


def write_json_to_file(filename, json_data):
    with open(filename, 'w') as outfile:
        json.dump(json_data, outfile)


# def run_test_map():
#
#     test_map = folium.Map([0,0], tiles='Mapbox Bright', zoom_start=4)
#
#     test_article_count_dict = dict.fromkeys([k for k in mgr.query_data_dict], 0)
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
#     test_map.choropleth(geo_str=mgr.json_geo_data,
#                         data=world,
#                         columns=['id','article_count'],
#                         key_on='feature.id',
#                         fill_color='YlGn',
#                         fill_opacity=0.7,
#                         line_opacity=0.2,
#                         threshold_scale=threshold_scale,
#                         legend_name='Number of Articles Originating from Country'
#                         )
#     folium.LayerControl().add_to(test_map)
#     test_map.save('test_map.html')

def menu_controller(menu_selection):

    selection_dict = {
        '1': execute_query,
        '2': execute_query,
        '3': query_all_from_date_range,
        'q': quit_program,
    }

    call_function = selection_dict.get(menu_selection[0])
    # log.log_info_message(menu_selection)

    ui.message('menu_selection: ' + str(menu_selection))

    if menu_selection is None:
        ui.message('Invalid Selection, Try Again')
        # log.log_warning_message('invalid selection in menu_controller()')
    elif int(menu_selection) == 1:
        call_function('headlines')
    elif int(menu_selection) == 2:
        call_function('all')
    else:
        call_function()



def get_source_country(source_name):

    for source in sources:
        if source.name == source_name:
            alpha_2_code = source.country
            country = pycountry.countries.get(alpha_2=alpha_2_code.upper())

            return country.alpha_3



def map_source(source_country):

    if type(source_country) is None:
        ui.message('No Source Country Matched')
        # log.log_error_message(source_country + ' type of None')
    else:
        mgr.query_data_dict[source_country] += 1


def execute_query(query_type):

    query_argument = ui.get_user_query()
    article_data = api.query_api(query_argument, query_type)

    for article in article_data:
        ui.message(article.__str__())
        # log.log_info_message(article.__str__())
        article_source_name = article.source
        try:
            source_country = get_source_country(article_source_name)
            if source_country is not None:
                map_source(source_country)
        except AttributeError:
            log.log_error_message('Error from article: ' + article.__str__())
            log.log_error_message('Article Source Type: ' + str(type(article.source)))

    build_choropleth(query_argument, query_type)



def build_choropleth(query, query_type):
    world_df = gpd.read_file(mgr.json_filename)
    choro_map = folium.Map([0,0], tiles='Mapbox Bright', zoom_start=4)
    articles_per_country = pd.Series(mgr.query_data_dict)
    world_df['article_count']=world_df['id'].map(articles_per_country)
    world_df.head()
    world_df.plot(column='article_count')
    threshold_scale = np.linspace(articles_per_country.values.min(), articles_per_country.values.max(), 6, dtype=int).tolist()

    choro_map.choropleth(geo_data=mgr.json_geo_data,
                        data=world_df,
                        columns=['id', 'article_count'],
                        key_on='feature.id',
                        fill_color='PuBuGn',
                         # YlGrBu - RdYlGn - YlOrBr - RdYlBu - PuBuGn - YlOrRd
                         # Oranges - Greens -Purples - Reds - Greys - Blues
                         # Pastel1 - Pastel2 - Spectral - Set1 - Set2 - Set3 - Dark2
                        fill_opacity=0.7,
                        line_opacity=0.2,
                        threshold_scale=threshold_scale
                        )

    folium.TileLayer("MapQuest Open Aerial", attr="Data Attr").add_to(choro_map)
    folium.TileLayer("stamenwatercolor", attr='attr').add_to(choro_map)
    folium.TileLayer("cartodbdark_matter", attr='attr').add_to(choro_map)
    folium.TileLayer("Mapbox Control Room", attr='attr').add_to(choro_map)
    folium.LayerControl().add_to(choro_map)

    date = datetime.datetime.now()
    now = datetime.datetime.ctime(date)
    map_prefix = str(now).replace(' ','_')
    map_prefix = map_prefix.replace(':', '-')
    filename = query_type + '_query_' + query + '_at_' + map_prefix + '_choropleth_map.html'
    ui.message(str(now))
    choro_map.save('./output_maps/' + filename)
    choro_map.render()
    mgr.build_query_results_dict()
    menu_controller(ui.top_menu())


def query_all_from_date_range():
    ui.message('in query_all_from_date_range')


def quit_program():
    # log.log_info_message('quit_program() called')
    sys.exit('Farewell digital world...\n')




if __name__ == '__main__':
    main()

