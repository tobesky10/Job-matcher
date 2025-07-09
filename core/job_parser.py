import re
import spacy
from spacy.matcher import Matcher
from collections import defaultdict

# Load spaCy model once for efficiency
nlp = spacy.load("en_core_web_md")

def build_job_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    
    # Job title patterns
    job_title_patterns = [
        [{"POS": "ADJ", "OP": "*"}, 
         {"POS": "PROPN", "OP": "+"}, 
         {"POS": "NOUN"}],
        [{"LOWER": {"IN": ["senior", "junior", "lead"]}},
         {"POS": "PROPN", "OP": "+"}],
        [{"POS": "PROPN"}, {"LOWER": "engineer"}],
        [{"POS": "PROPN"}, {"LOWER": "developer"}],
        [{"POS": "PROPN"}, {"LOWER": "manager"}]
    ]
    for pattern in job_title_patterns:
        matcher.add("JOB_TITLE", [pattern])
    
    # Company patterns
    company_patterns = [
        [{"ENT_TYPE": "ORG"}],
        [{"POS": "PROPN", "OP": "+"}, {"LOWER": {"IN": ["inc", "llc", "ltd"]}, "OP": "?"}]
    ]
    for pattern in company_patterns:
        matcher.add("COMPANY", [pattern])
    
    # Location patterns
    location_patterns = [
        [{"ENT_TYPE": "GPE"}],
        [{"ENT_TYPE": "LOC"}],
        [{"LOWER": "remote"}]
    ]
    for pattern in location_patterns:
        matcher.add("LOCATION", [pattern])
    
    return matcher

def extract_dates(text):
    date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b(?:\s*(?:–|-|to)\s*\b(?:Present|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{0,4}\b)?'
    return re.findall(date_pattern, text, re.IGNORECASE)

def extract_key_value_fields(text):
    entities = defaultdict(list)
    patterns = {
        "JOB_TITLE": r"Job Title:\s*(.+)",
        "COMPANY": r"Company:\s*(.+)",
        "LOCATION": r"Location:\s*(.+)",
        "DATE": r"Employment Dates:\s*(.+)",
        "DESCRIPTION": r"Job Description:\s*((?:.|\n)+?)(?=(?:Responsibilities|Qualifications|$))",
    }
    for key, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            cleaned = match.strip()
            if cleaned:
                entities[key].append(cleaned)
    return entities

def parse_job_entry(entry):
    entities = defaultdict(list)
    lines = [line.strip() for line in entry.split('\n') if line.strip()]
    
    if not lines:
        return entities
    
    # Assume first line is job title if not already extracted
    entities["JOB_TITLE"].append(lines[0])
    
    if len(lines) > 1:
        second_line = lines[1]
        # Extract dates first
        dates = extract_dates(second_line)
        for date in dates:
            entities["DATE"].append(date)
        
        # Remove dates from second line to avoid confusion
        clean_text = re.sub(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b', '', second_line, flags=re.IGNORECASE)
        doc = nlp(clean_text)
        
        matcher = build_job_matcher(nlp)
        matches = matcher(doc)
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]
            span_text = doc[start:end].text
            entities[label].append(span_text)
    
    if len(lines) > 2:
        description = "\n".join(lines[2:])
        entities["DESCRIPTION"].append(description)
    
    # Deduplicate lists
    return {k: list(set(v)) for k, v in entities.items()}

def extract_job_section(resume_text):
    pattern = re.compile(
        r'(Professional Experience|Work Experience|Experience)(.*?)(Education|Certifications|Projects|Interests|$)',
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(resume_text)
    return match.group(2).strip() if match else ""

def split_job_entries(exp_section_text):
    entries = re.split(r'\n{2,}|\-{10,}', exp_section_text)
    return [e.strip() for e in entries if e.strip()]

def extract_job_entities(text):
    entities = defaultdict(list)
    
    # Try extracting labeled fields first
    labeled_entities = extract_key_value_fields(text)
    if any(labeled_entities.values()):
        for key, vals in labeled_entities.items():
            entities[key].extend(vals)
        return {k: list(set(v)) for k, v in entities.items()}
    
    # Fallback to free-form parsing of job section
    exp_section = extract_job_section(text)
    if not exp_section:
        return {}
    
    job_entries = split_job_entries(exp_section)
    for entry in job_entries:
        job_data = parse_job_entry(entry)
        for key, vals in job_data.items():
            entities[key].extend(vals)
    
    return {k: list(set(v)) for k, v in entities.items()}

def extract_skills_section(text):
    patterns = [
        r'Skills:\s*((?:.|\n)+?)(?=\n\w+:|$)',
        r'Qualifications:\s*((?:.|\n)+?)(?=\n\w+:|$)',
        r'Requirements:\s*((?:.|\n)+?)(?=\n\w+:|$)'
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills_text = match.group(1).strip()
            return re.split(r'\s*[,;•\-/]\s*', skills_text)
    return []

def is_skill(ent):
    return ent.root.pos_ in ('NOUN', 'PROPN') and ent.root.dep_ not in ('nsubj', 'dobj')

def extract_skills_from_text(text):
    # Try section-based extraction first
    section_skills = extract_skills_section(text)
    if section_skills:
        return [skill.strip() for skill in section_skills if skill.strip()]
    
    # Otherwise, use spaCy entity recognition and heuristics
    doc = nlp(text)
    skills = [
        ent.text for ent in doc.ents 
        if ent.label_ in ("SKILL", "TECH") or is_skill(ent)
    ]
    return list(set(skills))

def safe_get(entities, key, default=''):
    return entities.get(key, [default])[0] if entities.get(key) else default

def parse_job_posting(text):
    """
    Main function to parse job posting text into structured dict.
    """
    entities = extract_key_value_fields(text)
    if not any(entities.values()):
        entities = extract_job_entities(text)
    
    skills = extract_skills_from_text(text)
    
    return {
        'title': safe_get(entities, 'JOB_TITLE', ''),
        'company': safe_get(entities, 'COMPANY', ''),
        'location': safe_get(entities, 'LOCATION', ''),
        'description': safe_get(entities, 'DESCRIPTION', ''),
        'skills': skills
    }
