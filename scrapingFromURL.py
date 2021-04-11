import sqlite3
from bs4 import BeautifulSoup
import requests


conn = sqlite3.connect('newsStorage.sqlite')
cur = conn.cursor()

cur.execute('''SELECT DISTINCT Domain from NewsURL
            ''')


domains = cur.fetchall()

print(domains)

cur.execute('''SELECT * FROM NewsURL
                WHERE Domain = ?
                LIMIT 5''', domains[6])


rows = cur.fetchall()



url = rows[2][4]

print(url)


StopWords = {}
StopWords['yahoo'] = "Subscribe now"
StopWords['investor'] = "YOU MAY ALSO LIKE"
StopWords['barrons'] = "Write to"
StopWords['investopedia'] = "abcdefghijklmn"
StopWords['thestreet'] = "Learn more now."


def storeParagraphsAsList(paragraphs, stopWord):
    Texts = []

    for paragraph in paragraphs:
        if stopWord in paragraph.text:
            break
        Texts.append(paragraph.text)
    
    return Texts

def getTextFromURL_ft(url):
    print("Locked behind paywall!")
    return []

def getTextFromURL_fool(url):
    response = requests.get(url,headers={'user-agent': 'my-app/0.0.1'})

    soup = BeautifulSoup(response.text, 'lxml')

    contents = soup.find('span', {"class": "article-content"})

    paragraphs = contents.findAll('p')

    return storeParagraphsAsList(paragraphs, StopWords['thestreet'])



def getTextFromURL_thestreet(url):
    response = requests.get(url,headers={'user-agent': 'my-app/0.0.1'})

    soup = BeautifulSoup(response.text, 'lxml')


    paragraphs = soup.findAll('p')

    return storeParagraphsAsList(paragraphs, StopWords['thestreet'])



def getTextFromURL_investopedia(url):
    response = requests.get(url,headers={'user-agent': 'my-app/0.0.1'})

    soup = BeautifulSoup(response.text, 'lxml')

    content_div = soup.find(id = 'article-body_1-0')


    paragraphs = content_div.findAll('p')

    return storeParagraphsAsList(paragraphs, StopWords['investopedia'])   



def getTextFromURL_barrons(url):
    response = requests.get(url,headers={'user-agent': 'my-app/0.0.1'})

    soup = BeautifulSoup(response.text, 'lxml')

    content_div = soup.find(id = 'js-article__body')


    paragraphs = content_div.findAll('p')

    return storeParagraphsAsList(paragraphs, StopWords['barrons'])    


def getTextFromURL_yahoo(url):

    response = requests.get(url,headers={'user-agent': 'my-app/0.0.1'})

    soup = BeautifulSoup(response.text, 'lxml')

    content_div = soup.find('div', {"class": "caas-body-wrapper"})


    paragraphs = content_div.findAll('p')

    return storeParagraphsAsList(paragraphs, StopWords['yahoo'])


def getTextFromURL_investors(url):

    response = requests.get(url,headers={'user-agent': 'my-app/0.0.1'})

    soup = BeautifulSoup(response.text, 'lxml')

    content_div = soup.find('div', {"class": "single-post-content post-content drop-cap"})


    paragraphs = content_div.findAll('p')

    return storeParagraphsAsList(paragraphs, StopWords['investor'])

