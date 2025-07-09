import spacy

nlp = spacy.load("custom_extended_model")

text = '''Micheal Smith
Email: johndoe@example.com
Phone number: (+234)812-345-6789
LinkedIn: linkedin.com/in/johndoe 
GitHub: github.com/johndoe

Professional Summary

Highly skilled and results-driven Senior Software Engineer with over 10 years of experience in designing, developing, and deploying scalable software solutions. Proficient in full-stack development, cloud computing, and leading cross-functional teams to deliver high-quality products. Passionate about leveraging technology to solve complex problems and drive business growth.

Technical Skills
Programming Languages: Java, Python, JavaScript, TypeScript, C++
Frameworks & Libraries: React, Angular, Node.js, Spring Boot, Django
Cloud Platforms: AWS, Azure, Google Cloud Platform (GCP)
DevOps Tools: Docker, Kubernetes, Jenkins, Terraform
Databases: PostgreSQL, MongoDB, MySQL, Redis
Other Skills: Microservices architecture, RESTful APIs, Agile methodologies, CI/CD pipelines
Professional Experience
Senior Software Engineer'''

doc = nlp(text)

print("Tokens:", [token.text for token in doc])
print("Entities found:")

if doc.ents:
    for ent in doc.ents:
        print(ent.text, ent.label_)
else:
    print("No entities detected.")
