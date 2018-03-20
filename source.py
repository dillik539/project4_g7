
class Source(object):

    def __init__(self, id, name, description, url, category, language, country):
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.category = category
        self.language = language
        self.country = country


    def __str__(self):
        return "ID: {}\n' \
               '    Name: {}\n' \
               '    Description: {}\n' \
               '    URL: {}\n' \
               '    Category: {}\n' \
               '    Language: {}\n' \
               '    Country: {}\n\n"\
            .format\
            (self.id,
             self.name,
             self.description,
             self.url,
             self.category,
             self.language,
             self.country)

