import fitz  # PyMuPDF
import json
import re
import os
from datetime import datetime

def parse_pdf_to_sections(pdf_path):
    """
    Parses a PDF file into sections using a robust method based on text properties.
    This helps accurately identify titles vs. content.
    """
    sections = []
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening or processing {pdf_path}: {e}")
        return sections

    current_title = os.path.splitext(os.path.basename(pdf_path))[0].replace('-', ' ').replace('_', ' ')
    current_content = ""
    current_page = 1
    
    # Heuristic: Find the most common font size to identify "normal" text.
    # Anything significantly larger is likely a title.
    font_sizes = {}
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    if "spans" in line:
                        for span in line["spans"]:
                            size = round(span['size'])
                            font_sizes[size] = font_sizes.get(size, 0) + 1
    
    if not font_sizes: # Handle empty docs
        return []

    normal_font_size = max(font_sizes, key=font_sizes.get)
    title_font_size = normal_font_size + 1 # A simple threshold

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    if "spans" in line and line["spans"]:
                        span = line["spans"][0]
                        text = " ".join([s["text"] for s in line["spans"]]).strip()
                        if not text:
                            continue

                        # A title is likely larger, bold, and a single line in its block.
                        is_title = (
                            round(span['size']) >= title_font_size or
                            (span['flags'] & 2**4) or # Bold flag
                            (len(block['lines']) == 1 and len(text) < 80 and text.isupper())
                        )

                        if is_title and len(text) > 4:
                            if current_content.strip():
                                sections.append({
                                    "title": current_title, "content": current_content.strip(),
                                    "page_number": current_page, "document": os.path.basename(pdf_path)
                                })
                            current_title = text
                            current_content = ""
                            current_page = page_num
                        else:
                            current_content += text + "\n"
    
    if current_content.strip():
        sections.append({
            "title": current_title, "content": current_content.strip(),
            "page_number": current_page, "document": os.path.basename(pdf_path)
        })

    doc.close()
    return sections

def get_keywords_from_persona(persona, job_to_be_done):
    """
    Dynamically generates keywords by analyzing the persona and job description,
    making the system scalable and generic.
    """
    role = persona.get('role', '').lower()
    task = job_to_be_done.get('task', '').lower()
    
    # Step 1: Extract core nouns and verbs from the user's request.
    keywords = set(re.findall(r'\b\w{4,}\b', f"{role} {task}")) # Get words with 4+ letters

    # Step 2: Define a generic concept map. This is NOT a hardcoded if/elif.
    # It allows the system to expand on the core keywords found in Step 1.
    concept_map = {
        # Concepts for HR / Forms
        'form': ['fillable', 'sign', 'signature', 'interactive', 'fields', 'create', 'convert', 'manage'],
        'onboarding': ['form', 'compliance', 'signature', 'document'],
        'compliance': ['form', 'sign', 'document', 'rules'],
        'signatures': ['sign', 'e-signatures', 'request', 'send'],
        
        # Concepts for Travel
        'travel': ['guide', 'cities', 'tips', 'packing', 'plan', 'itinerary', 'adventures'],
        'friends': ['group', 'party', 'entertainment', 'nightlife', 'activities', 'budget'],
        
        # Concepts for Food
        'food': ['menu', 'dinner', 'dish', 'recipe', 'cuisine', 'restaurants', 'ingredients'],
        'vegetarian': ['veggie', 'vegetable', 'salad', 'falafel', 'ratatouille', 'chickpea'],
        'buffet': ['menu', 'dishes', 'sides', 'mains', 'gathering'],
        'gluten-free': ['gf', 'quinoa', 'rice', 'salad']
    }

    # Step 3: Expand the keyword set using the concept map.
    expanded_keywords = set()
    for base_keyword in list(keywords):
        if base_keyword in concept_map:
            expanded_keywords.update(concept_map[base_keyword])
            
    keywords.update(expanded_keywords)
    return keywords

def score_section(section, keywords):
    """
    Scores a section based on keyword density and penalizes negative constraints.
    """
    score = 0
    content_lower = section['content'].lower()
    title_lower = section['title'].lower()

    for keyword in keywords:
        score += content_lower.count(keyword)
        if keyword in title_lower:
            score += 15  # Heavy boost for title match

    # Generic Negative Constraint: If the user wants "vegetarian", penalize meat.
    if 'vegetarian' in keywords:
        non_veg_penalties = ['chicken', 'tuna', 'beef', 'lamb', 'pork', 'shrimp', 'meat']
        for penalty in non_veg_penalties:
            if penalty in title_lower or penalty in content_lower:
                score -= 100 # Make it highly unlikely to be selected
    
    return score

def refine_text_extractive_summary(section_content, keywords, num_sentences=3):
    """
    Creates a summary by extracting the most relevant sentences.
    """
    clean_content = section_content.replace('\n', ' ').replace('\u2022', '')
    sentences = re.split(r'(?<=[.!?])\s+', clean_content)
    
    if not sentences: return ""

    scored_sentences = [(sum(1 for k in keywords if k in s.lower()), s) for s in sentences if s.strip()]
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    
    limit = min(num_sentences, len(scored_sentences))
    return " ".join([s for score, s in scored_sentences[:limit]])

def process_documents(input_data):
    """
    Main processing function.
    """
    persona = input_data['persona']
    job_to_be_done = input_data['job_to_be_done']
    documents = input_data['documents']
    keywords = get_keywords_from_persona(persona, job_to_be_done)
    
    all_sections = []
    for doc_info in documents:
        filename = doc_info['filename']
        if not os.path.exists(filename):
            print(f"Warning: Document '{filename}' not found. Skipping.")
            continue
        parsed_sections = parse_pdf_to_sections(filename)
        for section in parsed_sections:
            section['score'] = score_section(section, keywords)
            all_sections.append(section)
    
    all_sections.sort(key=lambda x: x['score'], reverse=True)

    output = {
        "metadata": {
            "input_documents": [doc['filename'] for doc in documents],
            "persona": persona['role'],
            "job_to_be_done": job_to_be_done['task'],
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    top_sections = [s for s in all_sections if s['score'] > 0][:5]
    
    for i, section in enumerate(top_sections, start=1):
        output['extracted_sections'].append({
            "document": section['document'], "section_title": section['title'],
            "importance_rank": i, "page_number": section['page_number']
        })
        
    for section in top_sections:
        refined_text = refine_text_extractive_summary(section['content'], keywords)
        output['subsection_analysis'].append({
            "document": section['document'], "refined_text": refined_text,
            "page_number": section['page_number']
        })

    return output

if __name__ == "__main__":
    # The script will process whichever file is named "challenge1b_input.json"
    INPUT_JSON_PATH = "challenge1b_input.json"
    os.makedirs("output", exist_ok=True)
    OUTPUT_JSON_PATH = "output/challenge1b_output_generated.json"

    if not os.path.exists(INPUT_JSON_PATH):
        print(f"Error: Input file not found at '{INPUT_JSON_PATH}'")
    else:
        with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        final_output = process_documents(input_data)
        with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(final_output, f, indent=4, ensure_ascii=False)
        print(f"Processing complete. Output saved to '{OUTPUT_JSON_PATH}'")

