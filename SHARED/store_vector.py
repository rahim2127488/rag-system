from SHARED.dependencies import get_collection

collection = get_collection()

def store(ids, documents, embeddings, metadatas):
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas

    )
    return collection.count()


