from flask import Flask, render_template
from src.fetcher import fetch_rss
from src.filter import filter_and_translate
from src.dedup import deduplicate

app = Flask(__name__)

RSS_SOURCES = [
    # BBC
    ('https://feeds.bbci.co.uk/news/technology/rss.xml', 'BBC', '科技'),
    ('https://feeds.bbci.co.uk/news/world/rss.xml', 'BBC', '國際'),
    ('https://feeds.bbci.co.uk/news/business/rss.xml', 'BBC', '財經'),

    # Nikkei Asia（亞太財經）
    ('https://asia.nikkei.com/rss/feed/nar', 'Nikkei Asia', '財經'),

    # Reuters
    ('https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com&ceid=US:en&hl=en-US&gl=US', 'Reuters', '國際'),
]

@app.route('/')
def index():
    all_articles = []
    for url, source, category in RSS_SOURCES:
        try:
            all_articles += fetch_rss(url, source, category)
        except Exception as e:
            print(f"❌ {source}: {e}")

    print(f"去重前：{len(all_articles)} 篇")
    all_articles = deduplicate(all_articles)
    print(f"去重後：{len(all_articles)} 篇")

    categorized = filter_and_translate(all_articles)
    return render_template('index.html', categorized=categorized)

if __name__ == '__main__':
    app.run(debug=True)