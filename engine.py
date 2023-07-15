import numpy as np
import tensorflow_hub as hub
import json


def embed_sentences(sentences):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    # Generate embeddings for the sentences
    embeddings = model(sentences)
    return embeddings


def compute_similarity(embedding1, embedding2):
    # Compute cosine similarity between two embeddings
    res = np.tensordot(embedding1, embedding2, 1)
    return res


class Engine:
    def __init__(self, query=""):
        self.query = query
        self.documents = []
        with open('/Users/ryansong612/Desktop/research-LLM/output/all.json', 'r') as file:
            data = json.load(file)
            for subject in data:
                for article in data[subject]:
                    document = {"subject": subject,
                                "title": article["title"],
                                "abstract": article["abstract"]}
                    self.documents.append(document)
        self.last_results = []

    def search(self, search_query=None):
        if search_query is None:
            query = self.query
        else:
            query = search_query
        query_vector = embed_sentences([query])[0]
        crawled_articles = [
            self.documents[i]["title"]
            + self.documents[i]["abstract"]
            for i in range(len(self.documents))
        ]

        article_embeddings = embed_sentences(crawled_articles)

        similarities = {
            index: compute_similarity(query_vector, article_embedding)
            for index, article_embedding in enumerate(article_embeddings)
        }

        similarities_dup = similarities.copy()
        results_limit = 15
        top_results = []

        for i in range(results_limit):
            max_similarity_index = max(similarities_dup.keys(), key=similarities_dup.__getitem__)
            top_results.append(max_similarity_index)
            del similarities_dup[max_similarity_index]

        for top_result in top_results:
            self.last_results.append(f"Index: {top_result}\n"
                                     f"Relevance: {similarities[top_result] * 100:.2f}%\n"
                                     f"{self.documents[top_result]}\n")
        return self.last_results

    def last_search(self):
        return self.last_results


if __name__ == "__main__":
    engine = Engine()
    results = engine.search("deep learning")
    for result in results:
        print(result)
