import spacy


def extract_skills(text):
    nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    skills = []
    for token in doc:
        if token.pos_ in ('NOUN', 'PROPN'):
            skills.append(token.text)
    return list(set(skills))


def tester():
    with open('core\SampleResume.txt', 'r') as file:
        content = file.read() 
    nlp = spacy.load("en_core_web_sm")
    doc2 = nlp(content)
    for ent in doc2.ents[:20]:
       if ent.label_ != '' or None:
           print(ent.text, ent.label_) 



from spacy.training.example import Example
from spacy.util import minibatch, compounding
import random

TRAIN_DATA = [
    ("Lead Marketing Specialist at MIT.",{'entities': [(5, 25, 'JOB_TITLE'), (29, 32, 'ORG')]}),
("Bachelor's degree in PhD Computer Vision.",{'entities': [(21, 40, 'EDUCATION')]}),
("Lead Data Scientist at Facebook.",{'entities': [(5, 19, 'JOB_TITLE'), (23, 31, 'ORG')]}),
("Certified AWS Solutions Architect with 5 years experience.",{'entities': [(10, 33, 'CERTIFICATION')]}),
("Bachelor's degree in MSc Artificial Intelligence.",{'entities': [(21, 48, 'EDUCATION')]}),
("Skills include CSS, React, and Machine Learning.",{'entities': [(15, 18, 'SKILL'), (20, 25, 'SKILL'), (31, 47, 'SKILL')]}),
("Worked at Facebook and Microsoft.",{'entities': [(10, 18, 'ORG'), (23, 32, 'ORG')]}),
("Graduated with Bachelor of Engineering from Google.",{'entities': [(15, 38, 'EDUCATION'), (44, 50, 'ORG')]}),
("Skills include HTML, Node.js, and Docker.",{'entities': [(15, 19, 'SKILL'), (21, 28, 'SKILL'), (34, 40, 'SKILL')]}),
("Bachelor's degree in Master of Science in Data Science.",{'entities': [(21, 54, 'EDUCATION')]}),
("Certified CISSP with 5 years experience.",{'entities': [(10, 15, 'CERTIFICATION')]}),
("Worked as UX Designer at Adobe.",{'entities': [(10, 21, 'JOB_TITLE'), (25, 30, 'ORG')]}),
("Graduated with MSc Artificial Intelligence from University of California.",{'entities': [(15, 42, 'EDUCATION'), (48, 72, 'ORG')]}),     
("Worked as Product Manager at Adobe.",{'entities': [(10, 25, 'JOB_TITLE'), (29, 34, 'ORG')]}),
("Bachelor's degree in MSc Artificial Intelligence.",{'entities': [(21, 48, 'EDUCATION')]}),
("Worked as Marketing Specialist at Stanford University.",{'entities': [(10, 30, 'JOB_TITLE'), (34, 53, 'ORG')]}),
("Bachelor's degree in MSc Artificial Intelligence.",{'entities': [(21, 48, 'EDUCATION')]}),
("Proficient in CSS, C++, and HTML.",{'entities': [(14, 17, 'SKILL'), (19, 22, 'SKILL'), (28, 32, 'SKILL')]}),
("Certified PMP with 5 years experience.",{'entities': [(10, 13, 'CERTIFICATION')]}),
("Bachelor's degree in BSc Computer Science.",{'entities': [(21, 41, 'EDUCATION')]}),
("Experienced Software Engineer skilled in Django and C++.",{'entities': [(12, 29, 'JOB_TITLE'), (41, 47, 'SKILL'), (52, 55, 'SKILL')]}), 
("Certified PMP with 5 years experience.",{'entities': [(10, 13, 'CERTIFICATION')]}),
("Worked at Facebook and MIT.",{'entities': [(10, 18, 'ORG'), (23, 26, 'ORG')]}),
("Bachelor's degree in MSc Artificial Intelligence.",{'entities': [(21, 48, 'EDUCATION')]}),
("Proficient in C++, Node.js, and Computer Vision.",{'entities': [(14, 17, 'SKILL'), (19, 26, 'SKILL'), (32, 47, 'SKILL')]}),
("Worked at Stanford University and Stanford University.",{'entities': [(10, 29, 'ORG'), (34, 53, 'ORG')]}),
("Completed PMP certification in 2020.",{'entities': [(10, 13, 'CERTIFICATION')]}),
("Worked as Data Scientist at University of California.",{'entities': [(10, 24, 'JOB_TITLE'), (28, 52, 'ORG')]}),
("Worked as UX Designer at Adobe.",{'entities': [(10, 21, 'JOB_TITLE'), (25, 30, 'ORG')]}),
("Lead Data Scientist at Amazon.",{'entities': [(5, 19, 'JOB_TITLE'), (23, 29, 'ORG')]}),
("Worked as Data Scientist at Amazon.",{'entities': [(10, 24, 'JOB_TITLE'), (28, 34, 'ORG')]}),
("Worked at Microsoft and MIT.",{'entities': [(10, 19, 'ORG'), (24, 27, 'ORG')]}),
("Certified Google Cloud Professional Data Engineer with 5 years experience.",{'entities': [(10, 49, 'CERTIFICATION')]}),
("Experienced UX Designer skilled in CSS and Natural Language Processing.",{'entities': [(12, 23, 'JOB_TITLE'), (35, 38, 'SKILL'), (43, 70, 'SKILL')]}),
("Graduated with PhD Computer Vision from OpenAI.",{'entities': [(15, 34, 'EDUCATION'), (40, 46, 'ORG')]}),
("Certified AWS Solutions Architect with 5 years experience.",{'entities': [(10, 33, 'CERTIFICATION')]}),
("Proficient in C++, Java, and Node.js.",{'entities': [(14, 17, 'SKILL'), (19, 23, 'SKILL'), (29, 36, 'SKILL')]}),
("Graduated with BSc Computer Science from Adobe.",{'entities': [(15, 35, 'EDUCATION'), (41, 46, 'ORG')]}),
("Lead Product Manager at Stanford University.",{'entities': [(5, 20, 'JOB_TITLE'), (24, 43, 'ORG')]}),
("Certified AWS Solutions Architect with 5 years experience.",{'entities': [(10, 33, 'CERTIFICATION')]}),
("Skills include Docker, Docker, and Django.",{'entities': [(15, 21, 'SKILL'), (23, 29, 'SKILL'), (35, 41, 'SKILL')]}),
("Certified Google Cloud Professional Data Engineer with 5 years experience.",{'entities': [(10, 49, 'CERTIFICATION')]}),
("Completed Certified Scrum Master certification in 2020.",{'entities': [(10, 32, 'CERTIFICATION')]}),
("Skills include AWS, Python, and Natural Language Processing.",{'entities': [(15, 18, 'SKILL'), (20, 26, 'SKILL'), (32, 59, 'SKILL')]}), 
("Bachelor's degree in Bachelor of Engineering.",{'entities': [(21, 44, 'EDUCATION')]}),
("Skills include React, Docker, and C++.",{'entities': [(15, 20, 'SKILL'), (22, 28, 'SKILL'), (34, 37, 'SKILL')]}),
("Completed PMP certification in 2020.",{'entities': [(10, 13, 'CERTIFICATION')]}),
("Certified AWS Solutions Architect with 5 years experience.",{'entities': [(10, 33, 'CERTIFICATION')]}),
("Worked as Marketing Specialist at Amazon.",{'entities': [(10, 30, 'JOB_TITLE'), (34, 40, 'ORG')]}),
("Worked at University of California and Facebook.",{'entities': [(10, 34, 'ORG'), (39, 47, 'ORG')]}),
("Proficient in CSS, Docker, and Machine Learning.",{'entities': [(14, 17, 'SKILL'), (19, 25, 'SKILL'), (31, 47, 'SKILL')]}),
("Proficient in Java, SQL, and Natural Language Processing.",{'entities': [(14, 18, 'SKILL'), (20, 23, 'SKILL'), (29, 56, 'SKILL')]}),    
("Worked as Marketing Specialist at OpenAI.",{'entities': [(10, 30, 'JOB_TITLE'), (34, 40, 'ORG')]}),
("Completed Certified Scrum Master certification in 2020.",{'entities': [(10, 32, 'CERTIFICATION')]}),
("Proficient in Node.js, JavaScript, and Node.js.",{'entities': [(14, 21, 'SKILL'), (23, 33, 'SKILL'), (39, 46, 'SKILL')]}),
("Experienced Lead Developer skilled in React and SQL.",{'entities': [(12, 26, 'JOB_TITLE'), (38, 43, 'SKILL'), (48, 51, 'SKILL')]}),     
("Graduated with Bachelor of Engineering from Microsoft.",{'entities': [(15, 38, 'EDUCATION'), (44, 53, 'ORG')]}),
("Completed Google Cloud Professional Data Engineer certification in 2020.",{'entities': [(10, 49, 'CERTIFICATION')]}),
("Graduated with BSc Computer Science from IBM.",{'entities': [(15, 35, 'EDUCATION'), (41, 44, 'ORG')]}),
("Experienced Data Scientist skilled in Natural Language Processing and Docker.",{'entities': [(12, 26, 'JOB_TITLE'), (38, 65, 'SKILL'), (70, 76, 'SKILL')]}),
("Bachelor's degree in MSc Artificial Intelligence.",{'entities': [(21, 48, 'EDUCATION')]}),
("Certified AWS Solutions Architect with 5 years experience.",{'entities': [(10, 33, 'CERTIFICATION')]}),
("Worked as Marketing Specialist at Facebook.",{'entities': [(10, 30, 'JOB_TITLE'), (34, 42, 'ORG')]}),
("Lead Lead Developer at Google.",{'entities': [(5, 19, 'JOB_TITLE'), (23, 29, 'ORG')]}),
("Worked as Marketing Specialist at OpenAI.",{'entities': [(10, 30, 'JOB_TITLE'), (34, 40, 'ORG')]}),
("Bachelor's degree in MSc Artificial Intelligence.",{'entities': [(21, 48, 'EDUCATION')]}),
("Experienced Lead Developer skilled in Kubernetes and SQL.",{'entities': [(12, 26, 'JOB_TITLE'), (38, 48, 'SKILL'), (53, 56, 'SKILL')]}),("Bachelor's degree in Master of Science in Data Science.",{'entities': [(21, 54, 'EDUCATION')]}),
("Experienced UX Designer skilled in CSS and Natural Language Processing.",{'entities': [(12, 23, 'JOB_TITLE'), (35, 38, 'SKILL'), (43, 70, 'SKILL')]}),
("Skills include Computer Vision, Node.js, and JavaScript.",{'entities': [(15, 30, 'SKILL'), (32, 39, 'SKILL'), (45, 55, 'SKILL')]}),     
("Experienced Data Scientist skilled in Kubernetes and React.",{'entities': [(12, 26, 'JOB_TITLE'), (38, 48, 'SKILL'), (53, 58, 'SKILL')]}),
("Experienced UX Designer skilled in Machine Learning and Java.",{'entities': [(12, 23, 'JOB_TITLE'), (35, 51, 'SKILL'), (56, 60, 'SKILL')]}),
("Proficient in Java, JavaScript, and Machine Learning.",{'entities': [(14, 18, 'SKILL'), (20, 30, 'SKILL'), (36, 52, 'SKILL')]}),        
("Experienced Data Scientist skilled in CSS and Django.",{'entities': [(12, 26, 'JOB_TITLE'), (38, 41, 'SKILL'), (46, 52, 'SKILL')]}),    
("Certified Certified Scrum Master with 5 years experience.",{'entities': [(10, 32, 'CERTIFICATION')]}),
("Skills include Python, Java, and C++.",{'entities': [(15, 21, 'SKILL'), (23, 27, 'SKILL'), (33, 36, 'SKILL')]}),
("Proficient in SQL, AWS, and Natural Language Processing.",{'entities': [(14, 17, 'SKILL'), (19, 22, 'SKILL'), (28, 55, 'SKILL')]}),     
("Graduated with Master of Science in Data Science from Stanford University.",{'entities': [(15, 48, 'EDUCATION'), (54, 73, 'ORG')]}),    
("Proficient in Docker, SQL, and Node.js.",{'entities': [(14, 20, 'SKILL'), (22, 25, 'SKILL'), (31, 38, 'SKILL')]}),
("Completed Google Cloud Professional Data Engineer certification in 2020.",{'entities': [(10, 49, 'CERTIFICATION')]}),
("Graduated with BSc Computer Science from Facebook.",{'entities': [(15, 35, 'EDUCATION'), (41, 49, 'ORG')]}),
("Skills include Java, C++, and Java.",{'entities': [(15, 19, 'SKILL'), (21, 24, 'SKILL'), (30, 34, 'SKILL')]}),
("Completed Certified Scrum Master certification in 2020.",{'entities': [(10, 32, 'CERTIFICATION')]}),
("Worked at Stanford University and University of California.",{'entities': [(10, 29, 'ORG'), (34, 58, 'ORG')]}),
("Worked at Stanford University and University of California.",{'entities': [(10, 29, 'ORG'), (34, 58, 'ORG')]}),
("Bachelor's degree in Bachelor of Engineering.",{'entities': [(21, 44, 'EDUCATION')]}),
("Lead UX Designer at Stanford University.",{'entities': [(5, 16, 'JOB_TITLE'), (20, 39, 'ORG')]}),
("Certified Certified Scrum Master with 5 years experience.",{'entities': [(10, 32, 'CERTIFICATION')]}),
("Worked as Data Scientist at MIT.",{'entities': [(10, 24, 'JOB_TITLE'), (28, 31, 'ORG')]}),
("Experienced Lead Developer skilled in Kubernetes and React.",{'entities': [(12, 26, 'JOB_TITLE'), (38, 48, 'SKILL'), (53, 58, 'SKILL')]}),
("Skills include Computer Vision, Machine Learning, and Java.",{'entities': [(15, 30, 'SKILL'), (32, 48, 'SKILL'), (54, 58, 'SKILL')]}),  
("Worked at Stanford University and Facebook.",{'entities': [(10, 29, 'ORG'), (34, 42, 'ORG')]}),
("Bachelor's degree in Master of Science in Data Science.",{'entities': [(21, 54, 'EDUCATION')]}),
("Graduated with Bachelor of Engineering from Adobe.",{'entities': [(15, 38, 'EDUCATION'), (44, 49, 'ORG')]}),
("Bachelor's degree in PhD Computer Vision.",{'entities': [(21, 40, 'EDUCATION')]}),
("Graduated with Master of Science in Data Science from OpenAI.",{'entities': [(15, 48, 'EDUCATION'), (54, 60, 'ORG')]}),
("Skills include React, Java, and HTML.",{'entities': [(15, 20, 'SKILL'), (22, 26, 'SKILL'), (32, 36, 'SKILL')]}),
("Bachelor's degree in Bachelor of Engineering.",{'entities': [(21, 44, 'EDUCATION')]}),
("Bachelor's degree in PhD Computer Vision.",{'entities': [(21, 40, 'EDUCATION')]}),
("Bachelor's degree in BSc Computer Science.",{'entities': [(21, 41, 'EDUCATION')]}),
("Completed Google Cloud Professional Data Engineer certification in 2020.",{'entities': [(10, 49, 'CERTIFICATION')]}),
]

def train_ner(train_data, iterations=30):
    nlp = spacy.blank("en")  # create blank English model
    ner = nlp.add_pipe("ner")

    # Add labels
    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    optimizer = nlp.begin_training()

    for itn in range(iterations):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
        for batch in batches:
            examples = []
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                examples.append(Example.from_dict(doc, annotations))
            nlp.update(examples, drop=0.35, losses=losses, sgd=optimizer)
        print(f"Iteration {itn+1}, Losses: {losses}")

    nlp.to_disk("custom_ner_model")
    print("Model saved to custom_ner_model")

if __name__ == "__main__":
    train_ner(TRAIN_DATA)
