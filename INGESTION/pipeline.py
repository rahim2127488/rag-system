from pathlib import Path

from bidaya import text_extractor
from clean import clean_text
from SHARED.embeddings import generate_embedding
from SHARED.store_vector import store
from chunk import split_text_into_chunks

from concept_detector import (
    find_structure_pages,
    extract_structure_candidates,
    find_numbered_headings,
    build_concepts,
    build_fallback_concepts,
    merge_and_order_concepts,
    assign_concepts_to_pages
)


def process_pdf(
    input_pdf,
    course_name,
    lesson_name
):

    pdf_path = Path(input_pdf)

    print("\n" + "=" * 70)
    print("STARTING PDF PROCESSING")
    print("=" * 70)

    print(
        "PDF:",
        pdf_path
    )


    print("\n[1] Extracting PDF...")

    extracting = text_extractor(
        pdf_path
    )

    if extracting is None:

        print(
            "Extraction failed."
        )

        return None



    print("[2] Cleaning text...")

    cleaning = clean_text(
        extracting
    )


    print("[3] Detecting structure pages...")

    structure_pages = (
        find_structure_pages(
            cleaning
        )
    )

    structure_candidates = (
        extract_structure_candidates(
            structure_pages
        )
    )

    print(
        "Structure pages:",
        len(structure_pages)
    )

    print(
        "Structure candidates:",
        len(structure_candidates)
    )



    print(
        "[4] Detecting numbered concepts..."
    )

    numbered_headings = (
        find_numbered_headings(
            cleaning
        )
    )

    numbered_concepts = (
        build_concepts(
            numbered_headings
        )
    )

    print(
        "Numbered concepts:",
        len(numbered_concepts)
    )


    print(
        "[5] Detecting fallback concepts..."
    )

    fallback_concepts = (
        build_fallback_concepts(
            pages=cleaning,
            numbered_concepts=numbered_concepts,
            pdf_path=pdf_path
        )
    )

    print(
        "Fallback concepts:",
        len(fallback_concepts)
    )


    print(
        "[6] Merging concepts..."
    )

    concepts = (
        merge_and_order_concepts(
            numbered_concepts,
            fallback_concepts
        )
    )


    print("\n" + "=" * 70)
    print("FINAL CONCEPTS")
    print("=" * 70)

    for concept in concepts:

        concept_type = (
            "FALLBACK"
            if concept.get(
                "is_fallback",
                False
            )
            else "NUMBERED"
        )

        print(
            concept["concept_index"],
            "→ PAGE",
            concept["pages"][0],
            "→",
            concept["concept"],
            f"[{concept_type}]"
        )



    print(
        "\n[7] Assigning concepts to pages..."
    )

    pages_with_concepts = (
        assign_concepts_to_pages(
            cleaning,
            concepts
        )
    )


    print(
        "[8] Splitting pages into chunks..."
    )

    chunks = split_text_into_chunks(
        pages_with_concepts,
        500,
        100
    )

    print(
        "Chunks created:",
        len(chunks)
    )


    print(
        "[9] Generating embeddings..."
    )

    ids = []
    documents = []
    metadatas = []
    embeddings = []

    document_name = (
        pdf_path.name
    )


    for chunk_number, chunk in enumerate(
        chunks,
        start=0
    ):


        documents.append(
            chunk["text"]
        )


        chunk_id = (
            f"{pdf_path.stem}"
            f"_chunk_"
            f"{chunk['chunk_index']}"
        )

        ids.append(
            chunk_id
        )

        embedding = (
            generate_embedding(
                chunk["text"]
            )
        )

        embeddings.append(
            embedding
        )


        metadata = {

            "document": (
                document_name
            ),

            "course": (
                course_name
            ),

            "lesson": (
                lesson_name
            ),

            "page": (
                chunk["page"]
            ),

            "chunk_index": (
                chunk["chunk_index"]
            ),

            "content_type": (
                chunk["content_type"]
            )
        }


        if (
            chunk["concept"]
            is not None
        ):

            metadata["concept"] = (
                chunk["concept"]
            )


        if (
            chunk["section"]
            is not None
        ):

            metadata["section"] = (
                chunk["section"]
            )


        if (
            chunk["concept_index"]
            is not None
        ):

            metadata[
                "concept_index"
            ] = (
                chunk[
                    "concept_index"
                ]
            )


        metadatas.append(
            metadata
        )


    print(
        "[10] Storing in ChromaDB..."
    )

    storing = store(
        ids,
        documents,
        embeddings,
        metadatas
    )


    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)

    print(
        "Document:",
        document_name
    )

    print(
        "Concepts:",
        len(concepts)
    )

    print(
        "Chunks:",
        len(chunks)
    )


    return storing


