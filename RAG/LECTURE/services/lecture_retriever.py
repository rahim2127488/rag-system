def lecture_retrieve(collection, course, lesson, concept):

    results = collection.get(
        where={
            "$and" : [
                {"course" : course},
                {"lesson" : lesson},
                {"concept": concept},
                {"content_type": "concept"}
            ]
        }
    )

    chunks = []

    for i in range(len(results["ids"])):

        metadata = results["metadatas"][i]

        chunk = {
            "chunk_id": results["ids"][i],
            "text": results["documents"][i],
            "page": metadata.get("page"),
            "course": metadata.get("course"),
            "lesson": metadata.get("lesson"),
            "concept": metadata.get("concept"),
            "document": metadata.get("document"),
            "section": metadata.get("section"),
            "concept_index": metadata.get("concept_index"),
            "chunk_index": metadata.get("chunk_index")
        }

        chunks.append(chunk)

    chunks.sort(
        key=lambda chunk: chunk["chunk_index"]
    )

    return chunks