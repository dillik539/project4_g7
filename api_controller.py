# This is a pip install
from newsapi import NewsApiClient
# This is from file articles.py
from article import Article

# This is the api Key
## TODO: Make the actual key on another page and import it it
newsapi = NewsApiClient(api_key = 'daaba2aab3d54874a0a154c18715e82c')
# top_headlines = newsapi.get_top_headlines(q = 'white house')
# all_articles = newsapi.get_everything(q = 'us economy', from_parameter = '2017-01-01', to = '2017-12-31')


class ApiController:

    def query_api(self, query_argument, query_type, start_date=None, end_date=None):

        valid_date_range = self.validate_dates(start_date, end_date)

        if not valid_date_range:

            if query_type is 'headlines':
                return self.build_articles_list(newsapi.get_top_headlines(q = query_argument))

            elif query_type is 'all':
                return self.build_articles_list(newsapi.get_everything(q = query_argument))

        if valid_date_range and query_type is 'all':

            return self.build_articles_list(newsapi.get_everything(
                q=query_argument, from_parameter=start_date, to=end_date
            ))





    def build_articles_list(self, api_query):

        articles_list = []

        for i in range(len(api_query['articles'])):
            raw_article_data = api_query['articles'][i]
            new_article_object = self.build_article_object(raw_article_data)
            articles_list.append(new_article_object)

        return articles_list


    @staticmethod
    def build_article_object(raw_article_data):

        title = raw_article_data['title']
        author = raw_article_data['author']
        source = raw_article_data['source']['name']
        published_time= raw_article_data['publishedAt']
        return Article(title, author, source, published_time)


    @staticmethod
    def validate_dates(start_date, end_date):
        return False
        pass
        # # TODO:  -- this function should actually be in the user_interface - use a datetime object to validate inputs
        # # TODO:  -- should be in YYYY-MM-DD format
