import spacy
from spacy.training.example import Example
from spacy.util import minibatch, compounding
import random

# Sample training data with built-in and custom entities
TRAIN_DATA = [
    ("John Doe is a software engineer skilled in Python and Django.", 
     {"entities": [(0, 8, "PERSON"), (38, 44, "SKILL"), (49, 55, "SKILL")]}),
    ("Jane Smith completed AWS Solutions Architect certification.", 
     {"entities": [(0, 10, "PERSON"), (20, 46, "CERTIFICATION")]}),
    ("Michael Johnson graduated with a BSc Computer Science from MIT.", 
     {"entities": [(0, 15, "PERSON"), (36, 57, "EDUCATION"), (63, 66, "ORG")]}),
    ("Emily Davis is a Data Scientist at Google.", 
     {"entities": [(0, 11, "PERSON"), (18, 31, "JOB_TITLE"), (35, 41, "ORG")]}),
    ("Certified Scrum Master Sarah Lee has 5 years experience.", 
     {"entities": [(0, 23, "CERTIFICATION"), (24, 33, "PERSON")]}),
    # Add more annotated examples here...
]

def main(iterations=20):
    # Load the pre-trained English model
    nlp = spacy.load("en_core_web_sm")
    ner = nlp.get_pipe("ner")

    # Add new custom labels to the NER pipe
    new_labels = ["SKILL", "CERTIFICATION", "EDUCATION", "JOB_TITLE"]
    for label in new_labels:
        ner.add_label(label)

    # Disable other pipes during training to speed up
    pipe_exceptions = ["ner"]
    unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    optimizer = nlp.resume_training()

    with nlp.disable_pipes(*unaffected_pipes):
        for itn in range(iterations):
            random.shuffle(TRAIN_DATA)
            losses = {}
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                examples = []
                for text, annotations in batch:
                    doc = nlp.make_doc(text)
                    examples.append(Example.from_dict(doc, annotations))
                nlp.update(examples, drop=0.35, losses=losses, sgd=optimizer)
            print(f"Iteration {itn+1}, Losses: {losses}")

    # Save the fine-tuned model
    nlp.to_disk("custom_extended_model")
    print("Model saved to 'custom_extended_model'")

if __name__ == "__main__":
    main()
