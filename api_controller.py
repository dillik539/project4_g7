from newsapi import NewsApiClient
from article import Article
from source import Source
import os
import log_controller
# import urllib.request
import requests

# news_api_key = os.environ.get('NEWS_CLIENT_API_KEY')
news_api_key = os.environ.get('NEWS_API_KEY')
newsapi = NewsApiClient(api_key = 'daaba2aab3d54874a0a154c18715e82c')
log = log_controller

class ApiController:

    def query_api(self, query_argument, query_type, start_date=None, end_date=None):

        valid_date_range = self.validate_dates(start_date, end_date)

        if not valid_date_range:
            if query_type is 'headlines':
                return self.build_articles_list(newsapi.get_top_headlines(q = query_argument, page_size=100))
            # elif query_type is 'all':
            #     return self.build_articles_list(newsapi.get_everything(q = query_argument, page_size=100))
            elif query_type is 'all':
                endpoint = 'https://newsapi.org/v2/everything?q=Putin&apiKey=daaba2aab3d54874a0a154c18715e82c&pageSize=100'
                # endpoint = 'https://newsapi.org/v2/everything?q=' + query_argument + '&apiKey=' + news_api_key
                article_count_raw = requests.get(endpoint)
                article_count = article_count_raw.json()
                print('Total Results: '  + str(article_count.json()['totalResults']))
                # for(p = 1, article_count - (p * 100) > 100, p += 100 ))
                if article_count <= 100:
                    return self.build_articles_list(requests.get(endpoint).json()['articles'])
                else if article_count > 100:
                    articles = []
                    for i in range(1, ((article_count - 100) / 100)):

                return self.build_articles_list(newsapi.get_everything(q=query_argument, page_size=100))

        if valid_date_range and query_type is 'all':
            return self.build_articles_list(
                newsapi.get_everything(q=query_argument, from_parameter=start_date, to=end_date)
            )


    def build_articles_list(self, api_query):
        articles_list = []

        for i in range(len(api_query['articles'])):
            raw_article_data = api_query['articles'][i]
            new_article_object = self.build_article_object(raw_article_data)
            articles_list.append(new_article_object)

        # log.log_info_message(str(articles_list))
        return articles_list


    @staticmethod
    def build_article_object(raw_article_data):

        title = raw_article_data['title']
        author = raw_article_data['author']
        source = raw_article_data['source']['name']
        published_time = raw_article_data['publishedAt']
        description = raw_article_data['description']
        article_url = raw_article_data['url']
        try:
            image_url = raw_article_data['urlToImage']
        except TypeError:
            # log.log_error_message('img_url=None caused TypeError')
            image_url = None
        return Article(title, author, source, published_time, description, article_url, image_url)


    @staticmethod
    def build_sources():
        sources_list = []
        sources = newsapi.get_sources()
        for source in sources['sources']:
            source_id = source['id']
            name = source['name']
            description = source['description']
            url = source['url']
            category = source['category']
            language = source['language']
            country = source['country']
            new_source = Source(source_id, name, description, url, category, language, country)
            sources_list.append(new_source)
        return sources_list


    @staticmethod
    def validate_dates(start_date, end_date):
        if start_date and end_date:
            pass
        return False

        # todo -- use a datetime object to validate inputs
        # todo -- should be in YYYY-MM-DD format
