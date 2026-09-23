import re

def clean_text(pages) :

    cleaned_text = []

    for page in pages:
        text_cleaned = page["text"].strip()

        text_cleaned = text_cleaned.replace("\t", " ")

        text_cleaned = re.sub(r" {2,}", " ", text_cleaned)

        text_cleaned = re.sub(r"\n{3,}", "\n\n", text_cleaned)

        cleaned_page = {
            "page": page["page"],
            "text": text_cleaned
        }
        cleaned_text.append(cleaned_page)

    return cleaned_text
