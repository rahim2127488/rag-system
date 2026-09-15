import re

def get_lines(pages):

    all_lines = []

    for page in pages:

        text = page["text"]
        lines = text.split("\n")

        for line in lines:

            line = line.strip()

            if line:
                all_lines.append({
                    "text" : line,
                    "page" : page["page"]
                })

    return all_lines


def heading_score(line):

    score = 0
    text = line["text"]

    word_count = len(text.split())

    if word_count <= 10:
        score+=1

    if text.isupper():
        score+=1

    if re.match(r"^\d+(\.\d+)*\.?\s+", text):
        score += 2
    return score

def find_structure_pages(pages):
    structure_pages = []

    for page in pages:
        text = page["text"].lower()

        if "contents" in text or "table of contents" in text or "outline" in text:
            structure_pages.append(page)

    return structure_pages


def extract_structure_candidates(structure_pages):
    candidates = []

    for page in structure_pages:
        lines = page["text"].split("\n")

        for line in lines:
            line = line.strip()

            line = line.lstrip("•*- ")

            if re.match(r"^\d+(\.\d+)*\.?\s", line):
                if line not in candidates:
                    candidates.append(line)

    return candidates

def find_heading_candidates(pages):
    candidates = []
    lines = get_lines(pages)

    for line in lines:
        score = heading_score(line)
        if score>=1:
            print(f"{line["text"]} | page: {line["page"]} | score: {score}")


    return candidates

def get_section_number(text):
    match = re.match(r"^(\d+(?:\.\d+)+)\.?\s+", text)

    if match:
        return match.group(1)

    return None

def find_numbered_headings(pages):
    headings = []

    lines = get_lines(pages)

    for line in lines:
        section_number = get_section_number(line["text"])

        if section_number:
            heading = {
                "section" : section_number,
                "title" : line["text"],
                "page" : line["page"]
            }
            headings.append(heading)
            
    return headings

def remove_section_number(title):
    return re.sub(r"^\d+(?:\.\d+)+\.?\s+", "", title).strip()

def build_concepts(headings):
    concepts = []

    for heading in headings:
        section = heading["section"]

        existing_concept = None

        for concept in concepts:
            if concept["section"] == section:
                existing_concept = concept
                break

        if existing_concept:
            if heading["page"] not in existing_concept["pages"]:
                existing_concept["pages"].append(heading["page"])

        else : 
            concept = {
                "section": section,
                "concept": remove_section_number(heading["title"]),
                "pages": [heading["page"]],
                "concept_index": len(concepts)
            }

            concepts.append(concept)

    return concepts

def assign_concepts_to_pages(pages, concepts):

    pages_with_concepts = []

    current_concept = None

    for page in pages:

        page_text = page["text"]

        for concept in concepts:

            section = concept["section"]

            pattern = rf"^{re.escape(section)}\.?\s+"

            if re.search(pattern, page_text, re.MULTILINE):
                current_concept = concept

        page_data = {
            "page": page["page"],
            "text": page_text,
            "concept": current_concept["concept"] if current_concept else None,
            "section": current_concept["section"] if current_concept else None,
            "concept_index": current_concept["concept_index"] if current_concept else None
        }

        pages_with_concepts.append(page_data)

    return pages_with_concepts
    