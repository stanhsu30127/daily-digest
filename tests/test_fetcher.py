from src.fetcher import fetch_rss

def test_fetch_rss_returns_list():
    articles = fetch_rss('https://feeds.bbci.co.uk/news/technology/rss.xml', 'BBC', '科技')
    assert isinstance(articles, list)

def test_fetch_rss_article_has_required_fields():
    articles = fetch_rss('https://feeds.bbci.co.uk/news/technology/rss.xml', 'BBC', '科技')
    article = articles[0]
    assert 'title' in article
    assert 'summary' in article
    assert 'link' in article
    assert 'source' in article
    assert 'category' in article

def test_fetch_rss_source_and_category_are_correct():
    articles = fetch_rss('https://feeds.bbci.co.uk/news/technology/rss.xml', 'BBC', '科技')
    article = articles[0]
    assert article['source'] == 'BBC'
    assert article['category'] == '科技'