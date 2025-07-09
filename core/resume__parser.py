import re
import spacy
from spacy.matcher import Matcher
from collections import defaultdict

# Load spaCy model once for efficiency
nlp = spacy.load("en_core_web_md")

def build_resume_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    
    # Patterns for skills (extend as needed)
    skill_patterns = [
        [{"LOWER": {"IN": ["java", "python", "javascript", "typescript", "c++"]}}],
        [{"LOWER": {"IN": ["react", "angular", "vue"]}, "OP": "?"}],
        [{"LOWER": {"IN": ["aws", "azure", "gcp"]}}],
        [{"LOWER": "docker"}, {"LOWER": "kubernetes", "OP": "?"}],
        [{"LOWER": "postgresql"}, {"LOWER": "mongodb", "OP": "?"}],
        [{"LOWER": "jenkins"}],
        [{"LOWER": "terraform"}],
        [{"LOWER": "spring"}, {"LOWER": "boot", "OP": "?"}],
        [{"LOWER": "django"}],
        [{"LOWER": "redis"}],
        [{"LOWER": "microservices"}],
        [{"LOWER": "restful"}, {"LOWER": "apis"}],
        [{"LOWER": "agile"}],
        [{"LOWER": "ci/cd"}, {"OP": "?"}],
    ]
    for i, pattern in enumerate(skill_patterns):
        matcher.add(f"SKILL_{i}", [pattern])
    
    # Patterns for job titles (similar to job parser)
    job_title_patterns = [
        [{"POS": "ADJ", "OP": "*"}, {"POS": "PROPN", "OP": "+"}, {"POS": "NOUN"}],
        [{"LOWER": {"IN": ["senior", "junior", "lead"]}}, {"POS": "PROPN", "OP": "+"}],
        [{"POS": "PROPN"}, {"LOWER": {"IN": ["engineer", "developer", "manager"]}}],
    ]
    for i, pattern in enumerate(job_title_patterns):
        matcher.add(f"JOB_TITLE_{i}", [pattern])
    
    # Patterns for organizations
    company_patterns = [
        [{"ENT_TYPE": "ORG"}],
        [{"POS": "PROPN", "OP": "+"}, {"LOWER": {"IN": ["inc", "llc", "ltd"]}, "OP": "?"}]
    ]
    for i, pattern in enumerate(company_patterns):
        matcher.add(f"ORG_{i}", [pattern])
    
    return matcher

def extract_dates(text):
    date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b(?:\s*(?:–|-|to)\s*\b(?:Present|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{0,4}\b)?'
    return re.findall(date_pattern, text, re.IGNORECASE)

def extract_section(text, start_keywords, end_keywords):
    """
    Extracts a section of text between start_keywords and end_keywords.
    Both are lists of regex patterns.
    """
    start_pattern = '|'.join(start_keywords)
    end_pattern = '|'.join(end_keywords)
    pattern = re.compile(
        rf'({start_pattern})(.*?)(?=({end_pattern})|$)',
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(text)
    return match.group(2).strip() if match else ''

def split_entries(section_text):
    """
    Splits a section into entries by double newlines or long dashes.
    """
    entries = re.split(r'\n{2,}|\-{10,}', section_text)
    return [e.strip() for e in entries if e.strip()]

def parse_experience_entry(entry, matcher):
    entities = defaultdict(list)
    doc = nlp(entry)
    
    # Match job titles, orgs, skills
    matches = matcher(doc)
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        span_text = doc[start:end].text
        if label.startswith("SKILL"):
            entities["SKILL"].append(span_text)
        elif label.startswith("JOB_TITLE"):
            entities["JOB_TITLE"].append(span_text)
        elif label.startswith("ORG"):
            entities["ORG"].append(span_text)
    
    # Extract dates
    dates = extract_dates(entry)
    entities["DATE"].extend(dates)
    
    # Add full entry as description
    entities["DESCRIPTION"].append(entry)
    
    return {k: list(set(v)) for k, v in entities.items()}

def extract_contact_info(text):
    """
    Extract contact info from the start of the resume.
    """
    entities = defaultdict(list)
    # Extract emails
    entities["EMAIL"] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
    # Extract phones
    entities["PHONE"] = re.findall(r'\+?\d[\d\s\-()]{7,}\d', text)
    # LinkedIn, GitHub
    entities["LINKEDIN"] = re.findall(r'linkedin\.com/[^\s]+', text, re.IGNORECASE)
    entities["GITHUB"] = re.findall(r'github\.com/[^\s]+', text, re.IGNORECASE)
    # PERSON entities from spaCy
    doc = nlp(text)
    persons = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    if persons:
        entities["PERSON"].append(persons[0])  # Take first person found
    return {k: list(set(v)) for k, v in entities.items()}

def parse_resume(text):
    """
    Main function to parse resume text into structured entities dict,
    following a modular section-based approach similar to job parser.
    """
    entities = defaultdict(list)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    matcher = build_resume_matcher(nlp)
    
    # Extract contact info from start (up to 'Professional Summary' or 'Technical Skills')
    contact_text = extract_section(text, ["^.*?(?=Professional Summary|Technical Skills|Experience|Education|$)"], ["Professional Summary", "Technical Skills", "Experience", "Education"])
    contact_entities = extract_contact_info(contact_text)
    for k, v in contact_entities.items():
        entities[k].extend(v)
    
    # Extract Technical Skills section
    skills_text = extract_section(text, ["Technical Skills", "Skills"], ["Professional Experience", "Experience", "Education", "Certifications", "Projects", "Interests", "$"])
    if skills_text:
        skills_doc = nlp(skills_text.lower())
        matches = matcher(skills_doc)
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]
            if label.startswith("SKILL"):
                span = skills_doc[start:end].text
                entities["SKILL"].append(span)
    
    # Extract Professional Experience section
    exp_text = extract_section(text, ["Professional Experience", "Experience", "Work Experience"], ["Education", "Certifications", "Projects", "Interests", "$"])
    if exp_text:
        exp_entries = split_entries(exp_text)
        for entry in exp_entries:
            exp_entities = parse_experience_entry(entry, matcher)
            for k, v in exp_entities.items():
                entities[k].extend(v)
    
    # Extract Education section
    edu_text = extract_section(text, ["Education"], ["Certifications", "Projects", "Interests", "$"])
    if edu_text:
        # Simple extraction of degrees and institutions
        degree_matches = re.findall(r'([A-Za-z\s]+),?\s*(?:Bachelor|Master|PhD|Associate|BA|BS|MS|MBA|Doctorate|Diploma|Certificate)?', edu_text, re.IGNORECASE)
        org_matches = re.findall(r'([A-Za-z\s]+ University|College|Institute|School)', edu_text, re.IGNORECASE)
        entities["EDUCATION"].extend([d.strip() for d in degree_matches if d.strip()])
        entities["ORG"].extend([o.strip() for o in org_matches if o.strip()])
    
    # Extract Certifications section
    cert_text = extract_section(text, ["Certifications", "Certificates"], ["Projects", "Interests", "$"])
    if cert_text:
        certs = re.findall(r'([A-Za-z0-9\s\-]+)(?:,|\(|$)', cert_text)
        entities["CERTIFICATION"].extend([c.strip() for c in certs if c.strip()])
    
    # Extract Projects section
    proj_text = extract_section(text, ["Projects"], ["Interests", "References", "$"])
    if proj_text:
        project_titles = re.findall(r'^([\w\s\-]+):', proj_text, re.MULTILINE)
        entities["PROJECT"].extend([p.strip() for p in project_titles if p.strip()])
    
    # Extract Interests section (optional)
    interests_text = extract_section(text, ["Interests"], ["References", "$"])
    if interests_text:
        interests = re.findall(r'[\w\s\-]+', interests_text)
        entities["INTEREST"].extend([i.strip() for i in interests if i.strip()])
    
    # Deduplicate all entity lists
    return {k: list(set(v)) for k, v in entities.items()}
