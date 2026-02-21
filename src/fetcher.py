import urllib.request
import xml.etree.ElementTree as ET

def fetch_rss(url, source_name, category):
    with urllib.request.urlopen(url) as response:
        xml_data = response.read()
    
    root = ET.fromstring(xml_data)
    channel = root.find('channel')
    
    articles = []
    for item in channel.findall('item'):
        article = {
            'title': item.findtext('title'),
            'summary': item.findtext('description'),
            'link': item.findtext('link'),
            'source': source_name,
            'category': category,
        }
        articles.append(article)
    
    return articles