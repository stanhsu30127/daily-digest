from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def deduplicate(articles):
    if not articles:
        return articles
    
    titles = [article['title'] for article in articles]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(titles)
    
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    kept = []
    removed = set()
    for i in range(len(articles)):
        if i in removed:
            continue
        kept.append(articles[i])
        for j in range(i + 1, len(articles)):
            if similarity_matrix[i][j] > 0.5:
                removed.add(j)
    
    return kept