MAX_DISTANCE = 0.65


def qa_retrieve(
    collection,
    question_embedding,
    course,
    lesson,
    top_k=5
):

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,

        where={
            "$and": [
                {"course": course},
                {"lesson": lesson}
            ]
        }
    )

    chunks = []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(ids)):

        metadata = metadatas[i]

        chunk = {
            "chunk_id": ids[i],
            "text": documents[i],

            "page": metadata.get("page"),
            "course": metadata.get("course"),
            "lesson": metadata.get("lesson"),
            "concept": metadata.get("concept"),
            "document": metadata.get("document"),
            "section": metadata.get("section"),
            "concept_index": metadata.get("concept_index"),
            "chunk_index": metadata.get("chunk_index"),

            "distance": distances[i]
        }

        chunks.append(chunk)


    # No chunks found
    if not chunks:
        return []


    # Best result is too far away
    if chunks[0]["distance"] > MAX_DISTANCE:
        return []


    return chunks