from INGESTION.bidaya import text_extractor
from INGESTION.clean import clean_text
from SHARED.store_vector import store
from SHARED.embeddings import generate_embedding
from INGESTION.chunk import split_text_into_chunks
from pathlib import Path
from INGESTION.concept_detector import (
    find_structure_pages,
    extract_structure_candidates,
    find_numbered_headings,
    build_concepts,
    assign_concepts_to_pages
)


def process_pdf(input_pdf, course_name, lesson_name):
    extracting = text_extractor(input_pdf)


    if extracting is None:
        print("extraction failed")
        return

    cleaning = clean_text(extracting)

    structure_pages = find_structure_pages(cleaning)

    structure_candidates = extract_structure_candidates(structure_pages)

    numbered_headings = find_numbered_headings(cleaning)

    concepts = build_concepts(numbered_headings)

    pages_with_concepts = assign_concepts_to_pages(cleaning, concepts)



    chunks = split_text_into_chunks(pages_with_concepts,500,100)
    ids = []
    documents = []
    metadatas = []
    embeddings = []
    
    pdf_path = Path(input_pdf)
    document_name = pdf_path.name
    for chunk_number , chunk in enumerate(chunks, start=0):
        documents.append(chunk["text"])
        ids.append(f"{pdf_path.stem}_chunk_{chunk["chunk_index"]}")
        embeddings.append(generate_embedding(chunk["text"]))
        metadata = {
            "document": document_name,
            "course": course_name,
            "lesson": lesson_name,
            "page": chunk["page"],
            "chunk_index": chunk["chunk_index"]

        }


        if chunk["concept"] is not None:
            metadata["concept"] = chunk["concept"]

        if chunk["section"] is not None:
            metadata["section"] = chunk["section"]

        if chunk["concept_index"] is not None:
            metadata["concept_index"] = chunk["concept_index"]

        metadatas.append(metadata)

    






        
    storing = store(ids, documents, embeddings, metadatas) 
    return storing   


