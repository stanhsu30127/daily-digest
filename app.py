from flask import Flask, render_template, request, Response
from functools import wraps
from src.fetcher import fetch_rss
from src.filter import filter_and_translate
from src.dedup import deduplicate
from datetime import date
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

cache = {
    'date': None,
    'data': None
}

def check_auth(password):
    return password == os.getenv('APP_PASSWORD')

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.password):
            return Response('請輸入密碼', 401,
                {'WWW-Authenticate': 'Basic realm="DailyDigest"'})
        return f(*args, **kwargs)
    return decorated

RSS_SOURCES = [
    ('https://feeds.bbci.co.uk/news/technology/rss.xml', 'BBC', '科技'),
    ('https://feeds.bbci.co.uk/news/world/rss.xml', 'BBC', '國際'),
    ('https://feeds.bbci.co.uk/news/business/rss.xml', 'BBC', '財經'),
    ('https://asia.nikkei.com/rss/feed/nar', 'Nikkei Asia', '財經'),
    ('https://news.google.com/rss/search?q=when:24h+allinurl:reuters.com&ceid=US:en&hl=en-US&gl=US', 'Reuters', '國際'),
]

@app.route('/')
@require_auth
def index():
    today = date.today()

    if cache['date'] == today and cache['data'] is not None:
        return render_template('index.html', categorized=cache['data'])

    all_articles = []
    for url, source, category in RSS_SOURCES:
        try:
            all_articles += fetch_rss(url, source, category)
        except Exception as e:
            print(f"❌ {source}: {e}")

    all_articles = deduplicate(all_articles)
    categorized = filter_and_translate(all_articles)

    cache['date'] = today
    cache['data'] = categorized

    return render_template('index.html', categorized=categorized)

if __name__ == '__main__':
    app.run(debug=True)