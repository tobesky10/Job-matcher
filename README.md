Job Matcher
Job Matcher is an intelligent recruitment platform that leverages Natural Language Processing (NLP) to analyze resumes and job postings, providing highly relevant job and candidate recommendations. This project combines advanced resume parsing, job description analysis, and semantic similarity matching to connect candidates with the best job opportunities efficiently.

Features
Resume and Job Parsing: Uses spaCy and custom regex matchers to extract structured information such as skills, experience, education, certifications, and job titles from unstructured text.

Semantic Similarity Matching: Employs spaCy’s vector embeddings and cosine similarity to match resumes with job postings and vice versa, going beyond simple keyword matching.

Skill Normalization: Automatically normalizes and manages skill entities in the database for consistent matching.

User-Friendly Interface: Clean and responsive frontend built with Django templates and modern CSS for easy resume upload, job posting parsing, and viewing recommendations.

Bidirectional Matching: Supports both candidate recommendations for job postings and job recommendations for resumes.

Extensible Architecture: Modular codebase for easy extension with additional NLP features or integration with external APIs.

Technologies Used
Python 3.10+

Django 4.x – Web framework

spaCy – NLP library for parsing and semantic similarity

PostgreSQL / MySQL – Relational database for storing users, resumes, jobs, and skills

HTML5, CSS3 – Responsive and accessible frontend design

JavaScript – Client-side interactivity and form handling

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/job-matcher.git
cd job-matcher
Create and activate a virtual environment:

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
Configure your database settings in settings.py.

Apply migrations:

bash
python manage.py migrate
Run the development server:

bash
python manage.py runserver
Open your browser at http://localhost:8000 to access the application.

Usage
Upload your resume via the Upload Resume page.

Parse job postings using the Parse Job Posting interface.

View recommended jobs matching your resume or candidates matching a job.

Explore parsed skills and experience extracted automatically.

Project Structure
core/ – Django app containing models, views, templates, and static files.

resume_parser.py – NLP resume parsing logic using spaCy and regex.

job_parser.py – Job posting parsing module.

similarity.py – Semantic similarity functions for matching.

templates/core/ – HTML templates inheriting from a clean base layout.

static/ – CSS and JavaScript assets.

Contributing
Contributions are welcome! Please fork the repository and submit pull requests for bug fixes, features, or improvements.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For questions or support, please contact:

Emmanuel Udeozor

Email: emmanueludeozor0@gmail.com
