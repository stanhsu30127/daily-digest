from src.fetcher import fetch_rss

bbc_articles = fetch_rss('http://feeds.bbci.co.uk/news/rss.xml', 'BBC')
ndtv_articles = fetch_rss('https://feeds.feedburner.com/ndtvnews-top-stories', 'NDTV')

#all_articles = bbc_articles + ndtv_articles

for article in bbc_articles[:5]:
    print(article['source'])
    print(article['title'])
    print(article['summary'])
    print('---')
for article in ndtv_articles[:5]:
    print(article['source'])
    print(article['title'])
    print(article['summary'])
    print('---')