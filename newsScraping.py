from urllib.request import urlopen, Request
from urllib.parse import urlparse
import sqlite3
import requests
from bs4 import BeautifulSoup



# The code is inspired from https://towardsdatascience.com/stock-news-sentiment-analysis-with-python-193d4b4378d4.



def gatherNewsOnline(newsTables, ticker):

    for tick in ticker:
        url = url_finviz + tick

        response = requests.get(url,headers={'user-agent': 'my-app/0.0.1'})
        soup = BeautifulSoup(response.text, features="lxml")

        #newsTable = soup.find_all(id='news-table')

        newsTable = soup.find(id="news-table")

        newsTables[tick] = newsTable

def storeTitleAndURL(newsTables, ticker):

    for tick in ticker:
        df = newsTables[tick]
        df_tr = df.findAll('tr')

        for i,tableRow in enumerate(df_tr):
            title = tableRow.a.text
            href = tableRow.a['href']
            domainName = urlparse(href).netloc

            newsTime = tableRow.td.text.split()
            
            if len(newsTime) == 1:
                hmsTime = newsTime[0]
            else:
                date, hmsTime = newsTime
            

            cur.execute('''INSERT OR IGNORE INTO NewsURL (Tick, Date, Time, Title, Url, Domain) VALUES (?,?,?,?,?,?) ''',(tick, date, hmsTime, title, href,domainName))
        
        conn.commit()
        print("Finished gathering data for {}".format(tick))



url_finviz = "https://finviz.com/quote.ashx?t="

tickToStock = {'AAPL': 'Apple', 'TSLA': 'Tesla', 'GOOG': 'Google', 'AMZN': 'Amazon', 'FB': 'Facebook', 'UAL': 'United Airlines', 'JPM': 'JPMorgan',
                'GS': 'Goldman Sachs', 'NFLX': 'Netflix', 'KMX': 'Carmax', 'GME': 'Gamestop', 'AMC': 'AMC', 'TLSA': 'Tiziana'}

ticker = list(tickToStock.keys())


if __name__ == "__main__":

    conn = sqlite3.connect('newsStorage.sqlite')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS NewsURL
        (Tick TEXT,
        Date TEXT,
        Time TEXT,
        Title TEXT,
        Url TEXT,
        Domain TEXT,
        PRIMARY KEY (Tick, Date, Title))''')

    conn.commit()





    newsTables = {}

    gatherNewsOnline(newsTables, ticker)
    storeTitleAndURL(newsTables, ticker)


    conn.close()





