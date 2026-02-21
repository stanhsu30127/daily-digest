from flask import Flask, render_template
from src.fetcher import fetch_rss

app = Flask(__name__)

RSS_SOURCES = [
    ('https://feeds.bbci.co.uk/news/technology/rss.xml', 'BBC', '科技'),
    ('https://feeds.bbci.co.uk/news/world/rss.xml', 'BBC', '國際'),
    ('https://feeds.bbci.co.uk/news/business/rss.xml', 'BBC', '財經'),
]

@app.route('/')
def index():
    all_articles = []
    for url, source, category in RSS_SOURCES:
        all_articles += fetch_rss(url, source, category)
    
    # 依類別整理成 dict
    categorized = {}
    for article in all_articles:
        cat = article['category']
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(article)
    
    return render_template('index.html', categorized=categorized)

if __name__ == '__main__':
    app.run(debug=True)