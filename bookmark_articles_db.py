'''This will create a table and add it to a database'''
import sqlite3, traceback
db_name = 'bookmarked_articles.db'#name of the database
'''This function add data obtained from api calls to a database
'''
def add_to_db(Id, title, author, source, published_time):
    try:
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            #call the function that creates a table.
            create_bookmarkedArticleTable()
            cursor.execute('INSERT INTO bookmarkedArticles VALUES (?,?,?,?,?)', (Id, title, author, source, published_time))
    except sqlite3.Error as error:
        print(error)
        traceback.print_exc()

'''create a table if not exists'''


def create_bookmarkedArticleTable():
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS bookmarkedArticles (Article_ID INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Source TEXT, Published_Date DateTime)')
'''This function get the information from the bookmarked data.'''
def get_bookmarked_data():
    with sqlite3.connect(db_name) as db:
        cursor =db.cursor()
    '''This will return a list of tuples of bookmarked articles'''
    return cursor.execute('SELECT * FROM bookmarkedArticles').fetchall()
