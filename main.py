from src.fetcher import fetch_rss

articles = fetch_rss('http://feeds.bbci.co.uk/news/rss.xml')

for article in articles[:5]:
    print(article['title'])
    print(article['summary'])
    print('---')