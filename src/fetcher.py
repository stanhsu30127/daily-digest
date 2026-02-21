import urllib.request
import xml.etree.ElementTree as ET

def fetch_rss(url, source_name, category):
    with urllib.request.urlopen(url) as response:
        xml_data = response.read()
    
    root = ET.fromstring(xml_data)
    
    # 標準 RSS 格式
    channel = root.find('channel')
    if channel is not None:
        items = channel.findall('item')
    # Atom 格式（The Verge）
    elif root.tag.endswith('feed'):
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        items = root.findall('atom:entry', ns)
    # RDF 格式（Nikkei Asia）
    else:
        ns = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
              'rss': 'http://purl.org/rss/1.0/'}
        items = root.findall('rss:item', ns)

    articles = []
    for item in items:
        title = item.findtext('title')
        summary = item.findtext('description')
        link = item.findtext('link')

        # Atom fallback
        if title is None:
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            title = item.findtext('atom:title', namespaces=ns)
            summary = item.findtext('atom:summary', namespaces=ns)
            link_el = item.find('atom:link', ns)
            link = link_el.get('href') if link_el is not None else None

        # RDF fallback
        if title is None:
            ns = {'rss': 'http://purl.org/rss/1.0/'}
            title = item.findtext('rss:title', namespaces=ns)
            link = item.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about')
            summary = ''

        if title:
            articles.append({
                'title': title,
                'summary': summary or '',
                'link': link or '',
                'source': source_name,
                'category': category,
            })
    
    return articles