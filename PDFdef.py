import fitz
import string
import json
import difflib

def preprocess_definitions(definitions):
    """
    Lowercase keys for matching but store original casing and definitions.
    Returns: {lower: (original, definition)}
    """
    return {k.lower(): (k, v) for k, v in definitions.items()}

def clean_and_structure_words(words):
    """Clean and structure words: (index, cleaned_word, original_rect)."""
    return [
        (i, w[4].lower().strip(string.punctuation), fitz.Rect(w[0], w[1], w[2], w[3]))
        for i, w in enumerate(words)
    ]

def find_fuzzy_match(phrase, definitions_clean, cutoff=0.9):
    """Find a close match to the phrase in the definitions."""
    candidates = definitions_clean.keys()
    matches = difflib.get_close_matches(phrase, candidates, n=1, cutoff=cutoff)
    return matches[0] if matches else None

def find_and_annotate_phrases(page, cleaned_words, definitions_clean, max_phrase_len):
    """Find phrases in text and annotate them in the PDF page."""
    i = 0
    while i < len(cleaned_words):
        matched = False
        for length in range(max_phrase_len, 0, -1):
            if i + length > len(cleaned_words):
                continue

            phrase = ' '.join(cleaned_words[i + j][1] for j in range(length))
            match = find_fuzzy_match(phrase, definitions_clean)

            if match:
                original_phrase, definition = definitions_clean[match]
                print(f"Fuzzy matched '{phrase}' to '{original_phrase}' at indexes {i} to {i+length-1}")
                
                rects = [cleaned_words[i + j][2] for j in range(length)]
                union_rect = rects[0]
                for r in rects[1:]:
                    union_rect |= r

                shape = page.new_shape()
                shape.draw_rect(union_rect)
                shape.commit()

                annot = page.add_rect_annot(union_rect)
                annot.set_info(content=definition, title=original_phrase)
                annot.set_colors(stroke=(0, 0, 0), fill=(0.5, 0.5, 0.5))
                annot.set_border(width=0.5)
                annot.set_opacity(0.3)
                annot.update()

                i += length
                matched = True
                break

        if not matched:
            i += 1

def annotate_pdf(doc_path, output_path, definitions_path):
    """Annotate PDF with definitions."""
    with open(definitions_path) as f:
        definitions = json.load(f)

    doc = fitz.open(doc_path)
    definitions_clean = preprocess_definitions(definitions)
    max_phrase_len = max(len(k.split()) for k in definitions_clean)

    for page in doc:
        words = page.get_text("words")
        cleaned_words = clean_and_structure_words(words)
        find_and_annotate_phrases(page, cleaned_words, definitions_clean, max_phrase_len)

    doc.save(output_path)


# Collect user input for the name of the pdf
pdf_name = input("Enter the name of the PDF file: ")

# Run the annotator
annotate_pdf(pdf_name, pdf_name[:-4] + "_annotated.pdf", "definitions.json")
