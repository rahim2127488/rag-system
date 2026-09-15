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

    #  Remove spaces and empty lines from the beginning and end.
    #cleaned_text = raw_text.strip()


    # Replace tab characters with normal spaces.
    #cleaned_text = cleaned_text.replace("\t", " ")


    # Replace two or more spaces with one space.
    #cleaned_text = re.sub(r" {2,}", " ", cleaned_text)



    # Replace three or more line breaks with two line breaks.
    #cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)




    #return cleaned_text


