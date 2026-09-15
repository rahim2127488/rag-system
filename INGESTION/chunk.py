def split_text_into_chunks(pages, chunk_size, overlap):

    chunks = []
    chunk_index = 0

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        words = text.split()

        start_position = 0

        while start_position < len(words):
            end_position = start_position + chunk_size

            chunks_words = words[start_position : end_position]

            chunk_text = " ".join(chunks_words)

            chunk = {
                "text" : chunk_text,
                "page" : page_number,
                "chunk_index" : chunk_index,
                "concept": page["concept"],
                "section": page["section"],
                "concept_index": page["concept_index"]
            }

            chunks.append(chunk)

            chunk_index+=1

            start_position = end_position - overlap

    return chunks










    

    

    

    



