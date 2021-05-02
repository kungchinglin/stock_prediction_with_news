import sqlite3
import time
import nltk
import re
from scrapingFromURL import knownDomains, getTextFromURL, contentsCleanUp
from newsScraping import tickToStock


conn = sqlite3.connect('newsStorage.sqlite')
cur = conn.cursor()


cur.execute('''SELECT COUNT(*) FROM Articles''')

num = cur.fetchone()[0]

batch = 50

for i in range(num//batch+1):

    cur.execute('''SELECT N.Tick, A.Title, A.Contents
                FROM Articles A
                JOIN NewsURL N
                ON A.Title = N.Title
                LIMIT ?
                OFFSET ?
            ''', (batch, i * batch))

    rows = cur.fetchall()

    for tick, title, article in rows:
        stockName = tickToStock[tick]

        matches = re.findall('([^.]*{}[^.]*\.) |([^.]*{}[^.]*\.) '.format(stockName, tick), article)

        for j in range(len(matches)):
            matches[j] = matches[j][0].strip(' \"\'')
        
        shortArt = ' '.join(matches)
        
        shortArt = re.sub(stockName, 'it', shortArt)
        shortArt = re.sub(tick, 'it', shortArt)

        cur.execute('''UPDATE Articles
                    SET Shortened = ?
                    WHERE Title = ?''', (shortArt, title))
    
    conn.commit()
    print("Finished batch {}".format(i))







