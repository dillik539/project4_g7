'''This will create a table and add it to a database'''
import sqlite3
db_name = 'cached_articles.db'#name of the database
'''This function add data obtained from api calls to a database
'''
def add_to_db(title, author, source, published_time):
    try:
        with sqlite3.connect(db_name) as db:
            cur = db.cursor()
            #call the function that creates a table.
            create_cachedArticleTable()
            cur.execute('INSERT INTO cachedArticles VALUES (?,?,?,?)', (title, author, source, published_time))
    except sqlite3.Error as error:
        print('An error occured.')
'''create a table if not exists'''
def create_cachedArticleTable():
    with sqlite3.connect(db_name) as db:
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS cachedArticles (Article_ID INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Source TEXT, Published_Date DateTime)')
