import sqlite3
from bs4 import BeautifulSoup
import requests




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



def storeParagraphsAsList(paragraphs, stopWord):
    Texts = []

    for paragraph in paragraphs:
        if stopWord in paragraph.text:
            break
        Texts.append(paragraph.text)
    
    return Texts

def getTextFromURL(data, knownDomains):
    url, domain = data[4], data[5]

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

conn = sqlite3.connect('newsStorage.sqlite')
cur = conn.cursor()

cur.execute('''SELECT DISTINCT Domain from NewsURL
            ''')


domains = cur.fetchall()


cur.execute('''SELECT * FROM NewsURL''')


rows = cur.fetchall()

for data in rows:
    Texts = getTextFromURL(data, knownDomains)
    print(Texts)


