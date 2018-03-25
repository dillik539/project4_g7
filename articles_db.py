'''This will create a table and add it to a database'''
import sqlite3, traceback
db_name = 'cached_articles.db'#name of the database
'''This function add data obtained from api calls to a database
'''
def add_to_db(Id, title, author, source, published_time):
    try:
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            #call the function that creates a table.
            create_cachedArticleTable()
            cursor.execute('INSERT INTO cachedArticles VALUES (?,?,?,?,?)', (Id, title, author, source, published_time))
    except sqlite3.Error as error:
        print(error)
        traceback.print_exc()

'''create a table if not exists'''
def create_cachedArticleTable():
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS cachedArticles (Article_ID INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Source TEXT, Published_Date DateTime)')
'''This function get the information from the cached data.'''
def get_cached_data():
    with sqlite3.connect(db_name) as db:
        cursor =db.cursor()
    '''This returns a list of tuples. Each tuple contains an Id, title, author, source, and published_time'''
    return cursor.execute('SELECT * FROM cachedArticles').fetchall()
    # for row in cursor.execute('SELECT * FROM cachedArticles'):
    #     print(row)
    #     print('Article_ID: ', row[0])
    #     print('Author:', row[1])
    #     print('Title: ', row[2])
    #     print('Source: ', row[3])
    #     print('publishedAt: ', row[4])
