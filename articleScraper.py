import requests
from bs4 import BeautifulSoup
from GoogleNews import GoogleNews

def getArticles(searchQuery, dateRange = False, startDate = '', endDate = ''):
    # returns first page of GoogleNews article results for the given query
    # in the form of a list of dictionary (dict w info per article) 
    # Dict Keys = [title, media, date, desc, link, img]
    if dateRange:
        googlenews = GoogleNews(lang='en', start = startDate, end = endDate)
    else:
        googlenews = GoogleNews(lang='en', period = 'd')
    googlenews.search(searchQuery)
    articlesInfo = googlenews.result(sort=True)
    return articlesInfo

def filterArticlesByTitle(articlesInfoList, keyword):
    # filters out articles that arent specifically about keyword
    # based on if keyword/topic is in title
    relevantArticles = []
    for a in articlesInfoList:
        if keyword in a['title']:
            relevantArticles.append(a)
    return relevantArticles

def articleTextScraper(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        article = soup.find('article').find_all('p')
        articleTextList = [s.text for s in article]
        articleText = '\n'.join(articleTextList)
    except:
        try:
            divElements = [value
                    for value in soup.select('div[class*="article"]').find_all('p')]
        except:
            try:
                divElements = [value
                        for value in soup.select('div[class*="article"]').find('p')]
            except:
                return 'Scraper method failed!'
        articleText = [s.text for s in divElements] 
        articleText = articleText[0]
    return articleText

def linkArticleTextToInfo(relevantArticles):
    for idx,articleInfo in enumerate(relevantArticles):
        relevantArticles[idx]['article_text'] = articleTextScraper(relevantArticles[idx]['link'])
    
    return relevantArticles

if __name__=='__main__':
    ## Test method for all functions in this script
    ## Searches for articles on AMD in the last day then
    ## scrapes text and tabulates all info retrieved
    afo = getArticles('AMD')
    articles = filterArticlesByTitle(afo, 'AMD')
    at = linkArticleTextToInfo(articles)
    keys = list(at[0].keys())

    print('Length of article list: ' + str(len(at)))
    print('Below is data per key of first article')
    for k in keys:
        print('\n')
        print(k + ':')
        print(at[0][k])