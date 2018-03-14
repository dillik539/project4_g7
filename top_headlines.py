import requests
'''get top headlines data from newsapi.org. This website provides
the live news articles from all over the web'''
contents = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=daaba2aab3d54874a0a154c18715e82c")
'''covert obtained data to json'''
data = contents.json()

def get_top_headlines():
    '''process json data to obtain desired results. it is a nested data of dictionaries
    and lists. loops through a list to get title, author, source, and published time
    for all the headlines news'''
    for i in range(len(data['articles'])):
        title = data['articles'][i]['title']
        author = data['articles'][i]['author']
        source = data['articles'][i]['source']['name']
        published_time = data['articles'][i]['publishedAt']
        print('Title: ', title)
        print('Author: ', author)
        print('Source Name: ', source)
        print('Published time: ', published_time)
        print()

def main():
    get_top_headlines()
main()
