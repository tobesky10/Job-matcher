import random

# Define entity lists
'''SKILLS = [
    "Python", "Django", "Java", "C++", "Machine Learning", "React",
    "Node.js", "Docker", "SQL", "Kubernetes", "AWS", "HTML", "CSS",
    "JavaScript", "Computer Vision", "Natural Language Processing"
]

ORGS = [
    "OpenAI", "Google", "Facebook", "Amazon", "Microsoft", "IBM",
    "Adobe", "Stanford University", "MIT", "University of California"
]

EDUCATIONS = [
    "BSc Computer Science", "MSc Artificial Intelligence",
    "PhD Computer Vision", "Bachelor of Engineering",
    "Master of Science in Data Science"
]

CERTIFICATIONS = [
    "AWS Solutions Architect", "PMP", "Certified Scrum Master",
    "CISSP", "Google Cloud Professional Data Engineer"
]

JOB_TITLES = [
    "Software Engineer", "Data Scientist", "Product Manager",
    "UX Designer", "Marketing Specialist", "Lead Developer"
]

# Sentence templates with placeholders and corresponding entity types
TEMPLATES = [
    ("Experienced {} skilled in {} and {}.", ["JOB_TITLE", "SKILL", "SKILL"]),
    ("Worked at {} and {}.", ["ORG", "ORG"]),
    ("Graduated with {} from {}.", ["EDUCATION", "ORG"]),
    ("Certified {} with 5 years experience.", ["CERTIFICATION"]),
    ("Proficient in {}, {}, and {}.", ["SKILL", "SKILL", "SKILL"]),
    ("Lead {} at {}.", ["JOB_TITLE", "ORG"]),
    ("Completed {} certification in 2020.", ["CERTIFICATION"]),
    ("Skills include {}, {}, and {}.", ["SKILL", "SKILL", "SKILL"]),
    ("Worked as {} at {}.", ["JOB_TITLE", "ORG"]),
    ("Bachelor's degree in {}.", ["EDUCATION"]),
]

def generate_training_example():
    # Choose a random template
    template, labels = random.choice(TEMPLATES)

    # For each label, pick a random entity from the corresponding list
    replacements = []
    for label in labels:
        if label == "SKILL":
            replacements.append(random.choice(SKILLS))
        elif label == "ORG":
            replacements.append(random.choice(ORGS))
        elif label == "EDUCATION":
            replacements.append(random.choice(EDUCATIONS))
        elif label == "CERTIFICATION":
            replacements.append(random.choice(CERTIFICATIONS))
        elif label == "JOB_TITLE":
            replacements.append(random.choice(JOB_TITLES))

    # Fill the template with entities
    text = template.format(*replacements)

    # Compute entity offsets
    entities = []
    start = 0
    for ent_text, label in zip(replacements, labels):
        start = text.find(ent_text, start)
        end = start + len(ent_text)
        entities.append((start, end, label))
        start = end  # Move past this entity for next search

    return ( text, {"entities": entities})

def generate_dataset(n=100):
    dataset = []
    for _ in range(n):
        example = generate_training_example()
        dataset.append(example)
    return (dataset)

if __name__ == "__main__":
    data = generate_dataset(100)
    for text, annotations in data[:100]:  # print first 100 examples
        print("("+'"'+text+'"' + ","+str(annotations)+")"+",")
        '''

# Entity lists including built-in and custom labels
SKILLS = ["Python", "Django", "Java", "Machine Learning", "React"]
ORGS = ["OpenAI", "Google", "Facebook", "Amazon"]
PERSONS = ["John Doe", "Jane Smith", "Michael Johnson", "Emily Davis"]
CERTIFICATIONS = ["AWS Solutions Architect", "PMP", "Certified Scrum Master"]
EDUCATIONS = ["BSc Computer Science", "MSc Artificial Intelligence"]
JOB_TITLES = ["Software Engineer", "Data Scientist", "Product Manager"]

# Templates with placeholders for all entity types
TEMPLATES = [
    ("{} is a {} skilled in {} and {} at {}.", ["PERSON", "JOB_TITLE", "SKILL", "SKILL", "ORG"]),
    ("{} completed the {} certification and graduated with a {}.", ["PERSON", "CERTIFICATION", "EDUCATION"]),
    ("Experienced {} with skills in {} and {}.", ["JOB_TITLE", "SKILL", "SKILL"]),
    ("{} works at {} as a {}.", ["PERSON", "ORG", "JOB_TITLE"]),
]

def generate_training_example():
    template, labels = random.choice(TEMPLATES)

    replacements = []
    for label in labels:
        if label == "PERSON":
            replacements.append(random.choice(PERSONS))
        elif label == "JOB_TITLE":
            replacements.append(random.choice(JOB_TITLES))
        elif label == "SKILL":
            replacements.append(random.choice(SKILLS))
        elif label == "ORG":
            replacements.append(random.choice(ORGS))
        elif label == "CERTIFICATION":
            replacements.append(random.choice(CERTIFICATIONS))
        elif label == "EDUCATION":
            replacements.append(random.choice(EDUCATIONS))

    text = template.format(*replacements)

    entities = []
    start = 0
    for ent_text, label in zip(replacements, labels):
        start = text.find(ent_text, start)
        end = start + len(ent_text)
        entities.append((start, end, label))
        start = end

    return (text, {"entities": entities})

def generate_dataset(n=100):
    return [generate_training_example() for _ in range(n)]

if __name__ == "__main__":
    data = generate_dataset(10)
    for text, annotations in data:
        print(text)
        print(annotations)
        print()

