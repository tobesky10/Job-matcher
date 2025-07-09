import spacy
from .models import JobPosting, Resume


nlp = spacy.load("en_core_web_md")

def find_matching_jobs_for_resume(resume, threshold=0.5):
    resume_text = (resume.experience or '') + ' ' + (resume.education or '') 
    resume_doc = nlp(resume_text)

    matches = []
    for job in JobPosting.objects.all():
        job_text = (job.title or '') + ' ' + (job.description or '') 
        job_doc = nlp(job_text)
        similarity_score = resume_doc.similarity(job_doc)
        if similarity_score > threshold:
            matches.append({
                'id': job.id,
                'title': job.title,
                'company': job.company.name,
                'similarity': round(similarity_score, 3),
                'location': job.location,
                'skills':list(job.skills.values_list('name', flat=True)),
                'description': job.description[:200] + '...' if job.description else ''
            })
    matches.sort(key=lambda x: x['similarity'], reverse=True)
    print(matches)
    return matches

def find_resume_for_job(job, threshold=0.5):
    job_text = (job.title or '') + ' ' + (job.description or '')
    job_doc = nlp(job_text )

    matches = []
    for resume in Resume.objects.all():
        resume_text = (resume.experience or '') + ' ' + (resume.education or '')
        resume_doc = nlp(resume_text)
        similarity = job_doc.similarity(resume_doc)
        if similarity > threshold:
            matches.append({
                'id': resume.id,
                'user': resume.user.email,
                'similarity': round(similarity, 3),
                'skills': list(resume.skills.values_list('name', flat=True)),
            })

    matches.sort(key=lambda x: x['similarity'], reverse=True)
    return matches