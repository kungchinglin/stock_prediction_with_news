'''
This file cleans up the articles already stored in the database. The functionality will be built into the scraping code, so there is no need to re-execute this.

'''


import sqlite3
from bs4 import BeautifulSoup
import requests
import time
import nltk
from scrapingFromURL import knownDomains, getTextFromURL, contentsCleanUp



conn = sqlite3.connect('newsStorage.sqlite')
cur = conn.cursor()

cur.execute('''SELECT COUNT(*) FROM Articles''')

num = cur.fetchone()[0]

print(num)

batch = 50

for i in range(num//batch+1):

    cur.execute('''SELECT *
                FROM Articles
                LIMIT ?
                OFFSET ?
            ''', (batch, i * batch))

    rows = cur.fetchall()

    for title, article in rows:
        cleanArticle = contentsCleanUp(article)
        cur.execute('''UPDATE Articles
                    SET Contents = ?
                    WHERE Title = ?''', (cleanArticle, title))
    
    conn.commit()
    print("Finished batch {}".format(i))







