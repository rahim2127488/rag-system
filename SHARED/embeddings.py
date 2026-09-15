from sentence_transformers import SentenceTransformer
from SHARED.config import settings

model_name = settings.embedding_model
model = SentenceTransformer(model_name)

def generate_embedding(text):
    embedding = model.encode(
        text
    )

    vector=embedding.tolist()

    return vector