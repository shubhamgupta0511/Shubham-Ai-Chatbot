import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load CSV
df = pd.read_csv("Book1.csv")

# use all columns as knowledge
df["combined"] = df.astype(str).agg(" ".join, axis=1)

# embedding model (local AI understanding)
model = SentenceTransformer("all-MiniLM-L6-v2")

# convert knowledge into vectors
knowledge_embeddings = model.encode(df["combined"].tolist())


def search_knowledge(user_question, top_k=5):

    question_embedding = model.encode([user_question])
    similarities = cosine_similarity(question_embedding, knowledge_embeddings)[0]

    # sort highest similarity cases
    top_indices = similarities.argsort()[-top_k:][::-1]

    cases = []
    for idx in top_indices:
        if similarities[idx] > 0.25:  # lower threshold → allows new incidents
            cases.append(df.iloc[idx]["combined"])

    return "\n---\n".join(cases)

