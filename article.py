

class Article(object):

    def __init__(self, title, author, source, published_time, description, article_url, image_url):

        self.title = title
        self.author = author
        self.source = source
        self.published_time = published_time
        self.description = description
        self.url = article_url
        self.image = image_url

    def __str__(self):
        return 'Title: {} \n' \
               '    Author: {}\n' \
               '    Source: {}\n' \
               '    Published: {}\n' \
               '    Description: {}\n' \
               '    Article URL: {}\n' \
               '    Image URL: {}\n\n' \
               ''.format(
            self.title, self.author, self.source, self.published_time, self.description, self.url, self.image
        )



