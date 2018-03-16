
class Article(object):

    def __init__(self, title, author, source, published_time):

        self.title = title
        self.author = author
        self.source = source
        self.published_time = published_time

    def __str__(self):
        return 'Title: {} \n' \
               '    Author: {}\n' \
               '    Source: {}\n' \
               '    Published: {}\n\n'.format(
            self.title, self.author, self.source, self.published_time
        )