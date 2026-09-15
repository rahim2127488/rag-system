import time

from SHARED.dependencies import collection, generate_embedding
from RAG.QA.services.qa_retriever import qa_retrieve


# ============================================================
# CONFIG
# ============================================================

COURSE = "OOP"
LESSON = "Chapter 6"


# ============================================================
# 1. VERIFY STORED METADATA
# ============================================================

print("\n")
print("=" * 80)
print("VERIFYING STORED METADATA")
print("=" * 80)

sample = collection.get(
    where={"course": COURSE},
    limit=10,
    include=["metadatas"]
)

if not sample["metadatas"]:
    print("No metadata found for course:", COURSE)
else:
    for metadata in sample["metadatas"]:
        print(metadata)


# ============================================================
# 2. QA TEST QUESTIONS
# ============================================================

questions = [
    {
        "question": "What is an interface in Java?",
        "expected_concept": "The Interface Concept"
    },

    {
        "question": "What are the properties of interfaces?",
        "expected_concept": "Properties of Interfaces"
    },

    {
        "question": "What is a functional interface?",
        "expected_concept": "Functional Interfaces"
    },

    {
        "question": "How do method references work?",
        "expected_concept": "Method References"
    },

    {
        "question": "What is an anonymous inner class?",
        "expected_concept": "Anonymous Inner Classes"
    },

    {
        "question": "What is quantum entanglement?",
        "expected_concept": None
    }
]


# ============================================================
# 3. RUN TESTS
# ============================================================

for test in questions:

    question = test["question"]
    expected = test["expected_concept"]

    print("\n")
    print("=" * 80)
    print("QUESTION:", question)
    print("EXPECTED CONCEPT:", expected)
    print("=" * 80)

    # --------------------------------------------------------
    # Create embedding
    # --------------------------------------------------------

    question_embedding = generate_embedding(question)


    # --------------------------------------------------------
    # Measure retrieval time
    # --------------------------------------------------------

    start_time = time.perf_counter()

    chunks = qa_retrieve(
        collection=collection,
        question_embedding=question_embedding,
        course=COURSE,
        lesson=LESSON,
        top_k=5
    )

    end_time = time.perf_counter()

    retrieval_time = end_time - start_time


    # --------------------------------------------------------
    # No results
    # --------------------------------------------------------

    if not chunks:
        print("NO RESULTS")

        print(
            "Retrieval time:",
            round(retrieval_time * 1000, 2),
            "ms"
        )

        continue


    # --------------------------------------------------------
    # Display Top 5
    # --------------------------------------------------------

    for index, chunk in enumerate(chunks, start=1):

        print(f"\nTOP {index}")
        print("-" * 40)

        print("Concept:", chunk["concept"])
        print("Section:", chunk["section"])
        print("Page:", chunk["page"])
        print("Chunk index:", chunk["chunk_index"])
        print("Distance:", round(chunk["distance"], 4))

        print(
            "Text:",
            chunk["text"][:300]
        )


    # ========================================================
    # 4. TOP 1 CHECK
    # ========================================================

    top_1_concept = chunks[0]["concept"]

    if expected is None:

        print("\nEXPECTED RESULT:")
        print("This question should eventually be rejected as unrelated.")

        print(
            "Best distance:",
            round(chunks[0]["distance"], 4)
        )

    else:

        if top_1_concept == expected:

            print("\nTOP 1: CORRECT ✅")

        else:

            print("\nTOP 1: INCORRECT ❌")
            print("Expected:", expected)
            print("Received:", top_1_concept)


    # ========================================================
    # 5. TOP 3 CHECK
    # ========================================================

    if expected is not None:

        top_3_concepts = [
            chunk["concept"]
            for chunk in chunks[:3]
        ]

        if expected in top_3_concepts:

            print("TOP 3: CORRECT ✅")

        else:

            print("TOP 3: INCORRECT ❌")


    # ========================================================
    # 6. TOP 5 CHECK
    # ========================================================

    if expected is not None:

        top_5_concepts = [
            chunk["concept"]
            for chunk in chunks[:5]
        ]

        if expected in top_5_concepts:

            print("TOP 5: CORRECT ✅")

        else:

            print("TOP 5: INCORRECT ❌")


    # ========================================================
    # 7. RETRIEVAL TIME
    # ========================================================

    print(
        "\nRetrieval time:",
        round(retrieval_time * 1000, 2),
        "ms"
    )