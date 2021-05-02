import sqlite3
from bs4 import BeautifulSoup
import requests
import time
import re
from newsScraping import tickToStock

def storeParagraphsAsList(paragraphs, stopWord):
    Texts = []

    for paragraph in paragraphs:
        if stopWord in paragraph.text:
            break
        Texts.append(paragraph.text)
    
    return Texts

def getTextFromURL(data, knownDomains):
    url, domain = data

    response = requests.get(url,headers={'user-agent': 'my-app/0.0.1'})

    soup = BeautifulSoup(response.text, 'lxml')

    if domain not in knownDomains:
        paragraphs = soup.findAll('p')
    else:
        contentSearchBy, tag, stopWord = knownDomains[domain]

        if not tag:
            print("Locked behind paywall!")
            return []

        if not contentSearchBy:
            pass
        elif contentSearchBy[0] == 'id':
            content_div = soup.find(id = contentSearchBy[1])
        else:
            content_div = soup.find(contentSearchBy[0], {"class": contentSearchBy[1]})
        
        try:
            paragraphs = content_div.findAll(tag)
        except:
            paragraphs = soup.findAll('p')
        
        return storeParagraphsAsList(paragraphs, stopWord)


def contentsCleanUp(contents):
    newContents = re.sub('\s{2,}', ' ', contents)

    return newContents


def interceptExtract(contents, tick, tickToStock):
    stockName = tickToStock[tick]

    matches = re.findall('([^.]*{}[^.]*\.) |([^.]*{}[^.]*\.) '.format(stockName, tick), contents)

    for j in range(len(matches)):
        matches[j] = matches[j][0].strip(' \"\'')
        
    shortArt = ' '.join(matches)
        
    shortArt = re.sub(stockName, 'it', shortArt)
    shortArt = re.sub(tick, 'it', shortArt)

    return shortArt


def createArticleTable(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS Articles
                (Title TEXT UNIQUE,
                Contents TEXT)
                ''')


def fetchDomains(cur):
    cur.execute('''SELECT DISTINCT Domain from NewsURL
            ''')
    domains = cur.fetchall()

    return domains

def fetchRows(cur):
    cur.execute('''SELECT news.Tick, news.Title, news.Url, news.Domain 
                FROM NewsURL news
                LEFT JOIN Articles art
                ON news.Title = art.Title
                WHERE art.Title IS NULL
                
                ''')

    rows = cur.fetchall()

    return rows

knownDomains = {}
knownDomains['www.investors.com'] = (('div', "single-post-content post-content drop-cap"), 'p', "YOU MAY ALSO LIKE")
knownDomains['finance.yahoo.com'] = (('div', "caas-body-wrapper"), 'p', "Subscribe now")
knownDomains['www.barrons.com'] = (('id', "js-article__body"), 'p', "Write to")
knownDomains['www.investopedia.com'] = (('id', "article-body_1-0"), 'p', "abcdefghijklmn")
knownDomains['www.thestreet.com'] = ([], 'p', "Learn more now.")
knownDomains['www.fool.com'] = (('span', "article-content"), 'p', "Learn more now.")
knownDomains['www.ft.com'] = ([], "", "")
knownDomains['www.marketwatch.com'] = (('id', "js-article__body"), 'p', "abcdefghijklmn")
knownDomains['in.finance.yahoo.com'] = knownDomains['finance.yahoo.com']
knownDomains['www.millionacres.com'] = (('div', "block-paragraph"), 'p', "abcdefghijklmn")
knownDomains['qz.com'] = (('id', "article-content"), 'p', "abcdefghijklmn")
knownDomains['realmoney.thestreet.com'] = (('id', "article__body article-author-rail__body"), 'div', "abcdefghijklmn")



if __name__ == "__main__":

    conn = sqlite3.connect('newsStorage.sqlite')
    cur = conn.cursor()

    createArticleTable(cur)

    rows = fetchRows(cur)

    for i,data in enumerate(rows):
        tick, title, data = data[0], data[1], data[2:]
        Texts = getTextFromURL(data, knownDomains)
        contents = ' '.join(Texts)

        contents = contentsCleanUp(contents)

        shortArt = interceptExtract(contents, tick, tickToStock)

        print(contents[:20])

        cur.execute('''INSERT OR IGNORE INTO Articles 
                    (Title, Contents, Shortened) VALUES (?,?,?)
                    ''', (title,contents,shortArt))
        
        if i % 10 == 0:
            print("Sleeping now. index at {}".format(i))
            time.sleep(1)
            conn.commit()

    conn.close()


