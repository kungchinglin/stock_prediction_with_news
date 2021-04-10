from urllib.parse import urlparse
import sqlite3

'''
This is a one-time program to patch up the oversight I had. I originally stored the url data without getting the domain name, so I wrote another program to update all existing rows.

Now that I patched up the codes, there is no need to run this one anymore.
'''


conn = sqlite3.connect('newsStorage.sqlite')
cur = conn.cursor()

cur.execute('''SELECT * from NewsURL
            ''')

rows = cur.fetchall()

try:
    cur.execute(''' ALTER TABLE NewsURL
                    ADD COLUMN Domain TEXT
                    ''')
except:
    pass



for row in rows:
    tick, date, time, title, url = row[:5]

    domainName = urlparse(url).netloc

    cur.execute(''' UPDATE NewsURL
                SET Domain = ?
                WHERE Tick = ? AND Date = ? AND Time = ? AND Title = ?
                ''',(domainName, tick, date, time, title))
    

conn.commit()

conn.close()





