from src.fetcher import fetch_rss

RSS_SOURCES = [
    ('https://feeds.bbci.co.uk/news/technology/rss.xml', 'BBC', '科技'),
    ('https://feeds.bbci.co.uk/news/world/rss.xml', 'BBC', '國際'),
    ('https://feeds.bbci.co.uk/news/business/rss.xml', 'BBC', '財經'),
]

all_articles = []
for url, source, category in RSS_SOURCES:
    all_articles += fetch_rss(url, source, category)

current_category = None
for article in all_articles:
    if article['category'] != current_category:
        current_category = article['category']
        print(f"\n=== {current_category} ===")
    print(f"{article['source']} | {article['title']}")
    print(article['summary'])
    print('---')