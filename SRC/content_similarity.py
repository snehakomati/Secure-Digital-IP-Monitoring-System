from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def check_similarity(doc1_path, doc2_path):

    with open(doc1_path, "r", encoding="utf-8") as f:
        doc1 = f.read()

    with open(doc2_path, "r", encoding="utf-8") as f:
        doc2 = f.read()

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])

    similarity_score = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return similarity_score