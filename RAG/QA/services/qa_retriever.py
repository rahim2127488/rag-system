import math

from SHARED.retrieval_utils import (
    lexical_coverage,
    calculate_fallback_score,
    get_important_tokens,
    normalize_text
)



MAX_DISTANCE = 0.35

FALLBACK_MAX_DISTANCE = 0.50
FALLBACK_MIN_LEXICAL = 0.75


def cosine_distance(vector_a, vector_b):

    dot_product = sum(
        float(a) * float(b)
        for a, b in zip(
            vector_a,
            vector_b
        )
    )

    magnitude_a = math.sqrt(
        sum(
            float(a) * float(a)
            for a in vector_a
        )
    )

    magnitude_b = math.sqrt(
        sum(
            float(b) * float(b)
            for b in vector_b
        )
    )

    if (
        magnitude_a == 0
        or magnitude_b == 0
    ):
        return 1.0

    similarity = (
        dot_product
        /
        (
            magnitude_a
            *
            magnitude_b
        )
    )

    return 1.0 - similarity



def qa_retrieve(
    collection,
    question,
    question_embedding,
    course,
    lesson,
    top_k=5
):


    results = collection.query(
        query_embeddings=[
            question_embedding
        ],

        n_results=top_k,

        where={
            "$and": [
                {
                    "course": course
                },
                {
                    "lesson": lesson
                },
                {
                    "content_type": "concept"
                }
            ]
        }
    )


    chunks = []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]


    for i in range(
        len(ids)
    ):

        metadata = (
            metadatas[i]
        )

        chunk = {

            "chunk_id":
                ids[i],

            "text":
                documents[i],

            "page":
                metadata.get("page"),

            "course":
                metadata.get("course"),

            "lesson":
                metadata.get("lesson"),

            "concept":
                metadata.get("concept"),

            "document":
                metadata.get("document"),

            "section":
                metadata.get("section"),

            "concept_index":
                metadata.get(
                    "concept_index"
                ),

            "chunk_index":
                metadata.get(
                    "chunk_index"
                ),

            "content_type":
                metadata.get(
                    "content_type"
                ),

            "distance":
                distances[i]
        }

        chunks.append(
            chunk
        )


    if not chunks:
        return []


    strict_chunks = []

    for chunk in chunks:

        if (
            chunk["distance"]
            <= MAX_DISTANCE
        ):

            strict_chunks.append(
                chunk
            )


    if strict_chunks:

        return strict_chunks


    return fallback_retrieve(
        collection=collection,
        question=question,
        question_embedding=question_embedding,
        course=course,
        lesson=lesson,
        top_k=top_k
    )


def fallback_retrieve(
    collection,
    question,
    question_embedding,
    course,
    lesson,
    top_k=5
):


    results = collection.get(
        where={
            "$and": [
                {"course": course},
                {"lesson": lesson},
                {"content_type": "concept"}
            ]
        },

        include=[
            "documents",
            "metadatas",
            "embeddings"
        ]
    )


    ids = results["ids"]
    documents = results["documents"]
    metadatas = results["metadatas"]
    embeddings = results["embeddings"]


    if not ids:
        return []


    candidates = []




    important_tokens = get_important_tokens(
        question
    )

    important_phrase = " ".join(
        important_tokens
    )



    for i in range(len(ids)):

        document = documents[i]

        metadata = metadatas[i]

        stored_embedding = embeddings[i]


        lexical_score = lexical_coverage(
            question,
            document
        )

        if lexical_score == 0:
            continue

        distance = cosine_distance(
            question_embedding,
            stored_embedding
        )


        candidate_normalized = normalize_text(
            document
        )

        phrase_match = (
            len(important_tokens) > 1
            and
            important_phrase in candidate_normalized
        )


        strong_phrase_match = phrase_match


        reasonable_mixed_match = (
            lexical_score >= FALLBACK_MIN_LEXICAL
            and
            distance <= FALLBACK_MAX_DISTANCE
        )


        if not (
            strong_phrase_match
            or
            reasonable_mixed_match
        ):
            continue


        fallback_score = calculate_fallback_score(
            distance,
            lexical_score
        )


        candidate = {

            "chunk_id": ids[i],

            "text": document,

            "page": metadata.get("page"),

            "course": metadata.get("course"),

            "lesson": metadata.get("lesson"),

            "concept": metadata.get("concept"),

            "document": metadata.get("document"),

            "section": metadata.get("section"),

            "concept_index": metadata.get(
                "concept_index"
            ),

            "chunk_index": metadata.get(
                "chunk_index"
            ),

            "content_type": metadata.get(
                "content_type"
            ),

            "distance": distance,

            "lexical_score": lexical_score,

            "fallback_score": fallback_score
        }


        candidates.append(
            candidate
        )



    if not candidates:
        return []



    candidates.sort(
        key=lambda candidate:
            candidate["fallback_score"],
        reverse=True
    )


    return candidates[:top_k]