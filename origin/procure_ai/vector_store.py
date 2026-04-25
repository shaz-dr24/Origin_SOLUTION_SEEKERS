import faiss
import numpy as np

# Lazy loaded embedding model
model = None

def get_model():
    global model
    if model is None:
        print("🔄 Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model


class VectorStore:
    def __init__(self, index, documents, embeddings):
        self.index = index
        self.documents = documents
        self.embeddings = embeddings


# --------------------------------------------------
# BUILD VECTOR DATABASE
# --------------------------------------------------
def build_vector_store(documents):
    print("📦 Building Vector DB...")

    model_instance = get_model()

    texts = [doc.page_content for doc in documents]

    embeddings = model_instance.encode(texts)
    embeddings = np.array(embeddings).astype("float32")

    # ⭐ NORMALIZE → enables cosine similarity search
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # cosine similarity
    index.add(embeddings)

    print("✅ Vector DB ready")

    return VectorStore(index=index, documents=documents, embeddings=embeddings)


# --------------------------------------------------
# 🔎 SEMANTIC SEARCH (USED BY RETRIEVER)
# --------------------------------------------------
def search_vector_store(vector_db, query, top_k=3):
    model_instance = get_model()

    query_embedding = model_instance.encode([query]).astype("float32")
    faiss.normalize_L2(query_embedding)

    scores, indices = vector_db.index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        results.append(vector_db.documents[idx].page_content)

    return "\n".join(results)