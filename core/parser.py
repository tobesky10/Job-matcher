import spacy

# Load the trained custom NER model
nlp = spacy.load("custom_extended_model")

def extract_entities(text):
    """
    Extract entities from text using the custom NER model.
    Returns a dictionary of entity labels mapped to lists of entity texts.
    """
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_, []).append(ent.text)
    return entities

if __name__ == "__main__":
    sample_resume = """
    Micheal Timothy
    I have Experience in software engineer with skills in Python, Django, and machine learning.
    Worked at OpenAI and Google.
    Education: BSc Computer Science from MIT.
    """
    extracted = extract_entities(sample_resume)
    print("Extracted entities:", extracted)
