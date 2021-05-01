import sqlite3
import time
from scrapingFromURL import knownDomains, getTextFromURL, contentsCleanUp



conn = sqlite3.connect('newsStorage.sqlite')
cur = conn.cursor()

keyword = "Access to this page has been denied"

cur.execute(''' SELECT news.Title, news.Url, news.Domain 
            FROM NewsURL news
            JOIN Articles art
            ON news.Title = art.Title
            WHERE art.Contents LIKE ?
            ''', ("%"+keyword+"%",))

rows = cur.fetchall()

curRows = rows
iterations = 0

while curRows and iterations < 2:
    tempRows = []
    for row in curRows:
        title, data = row[0], row[1:]

        Texts = getTextFromURL(data,knownDomains)
        Texts = [text.strip(' \n') for text in Texts]
        print(Texts)
        time.sleep(2)


        contents = ' '.join(Texts)

        contents = contentsCleanUp(contents)


        if keyword in contents:
            tempRows.append(row)
        else:
            cur.execute('''UPDATE Articles
                    SET Contents = ?
                    WHERE Title = ?
                    ''', (contents, title))

    conn.commit()    
    curRows = tempRows
    iterations += 1







