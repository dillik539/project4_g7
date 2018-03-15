import requests

from newsapi import NewsApiClient
'''newsapi.org has a python module called newsapi. Install this module using this code:
pip install newsapi-python and import as above'''

#initiate the module's object that takes api key as argument
newsapi = NewsApiClient(api_key = 'daaba2aab3d54874a0a154c18715e82c')

'''call the predefined function in newsapi module. q is a parameter to search headlines with
specific string'''

top_headlines = newsapi.get_top_headlines(q = 'white house')

'''from_parameter and to are parameters that specify the dates to search from and to respectively.
This predefined function provides everything containing specified string with in a date range'''

all_articles = newsapi.get_everything(q = 'us economy', from_parameter = '2017-01-01', to = '2017-12-31')

def get_top_headlines():
    '''get top headlines data from newsapi.org. This website provides
    the live news articles from all over the web.process json data to obtain desired results.
    it is a nested data of dictionaries and lists. loops through a list to get title, author,
    source, and published time for all the headlines news'''

    for i in range(len(top_headlines['articles'])):
        title = top_headlines['articles'][i]['title']
        author = top_headlines['articles'][i]['author']
        source = top_headlines['articles'][i]['source']['name']
        published_time = top_headlines['articles'][i]['publishedAt']
        print('Title: ', title)
        print('Author: ', author)
        print('Source Name: ', source)
        print('Published time: ', published_time)
        print()

def get_all_articles():
    '''this provides not only the headlines, but everything- headlines, body, paragraph, etc
    that contains the specified search string'''

    for i in range(len(all_articles['articles'])):
        title = all_articles['articles'][i]['title']
        author = all_articles['articles'][i]['author']
        source = all_articles['articles'][i]['source']['name']
        published_time = all_articles['articles'][i]['publishedAt']
        print('Title: ', title)
        print('Author: ', author)
        print('Source Name: ', source)
        print('Published time: ', published_time)
        print()

def main():
    get_top_headlines()
    get_all_articles()
main()
