from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
#from django.db.models import Prefetch
from .job_parser import parse_job_posting
from .resume__parser import parse_resume  
from django.contrib.auth.decorators import login_required
from .forms import ResumeUploadForm, Profileform, Loginform
from .models import Resume, Skill, JobPosting, Company
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .Rater import find_matching_jobs_for_resume, find_resume_for_job
# Create your views here.
User = get_user_model()


'''def recommend_candidates_for_job(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    job_doc = nlp(job.description or '')

    matches = []
    for resume in Resume.objects.all():
        resume_text = (resume.experience or '') + ' ' + (resume.education or '')
        resume_doc = nlp(resume_text)
        similarity = job_doc.similarity(resume_doc)
        if similarity > 0.5:
            matches.append({
                'id': resume.id,
                'user': resume.user.username,
                'similarity': round(similarity, 3),
                'skills': list(resume.skills.values_list('name', flat=True)),
            })

    matches.sort(key=lambda x: x['similarity'], reverse=True)

    return render(request, 'core/candidate_recommendations.html', {
        'job': job,
        'matches': matches,
        'mode': 'candidates_for_job'
    })'''

def register_view(request):
    form = Profileform()

    if request.method == 'POST':
        form = Profileform(request.POST)
        if form.is_valid():
            firstname= request.POST.get('first_name')
            lastname= request.POST.get('last_name')
            email= request.POST.get('email')
            password= request.POST.get('password')
            mode = request.POST.get('dropdown')

            user = User.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=firstname,
                password=password,
                email=email,
                mode = mode)
            
            if mode == "Personal":
                return redirect('Index')
            else:
                return redirect('parse_job')

        else:
            messages.error(request, "An Error during registration.")

    context = {'form': form}
    return render(request, 'core/register.html', context)



def login_view(request):
    form = Loginform()
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('Index')  # Redirect to user profile or dashboard
        else:
            messages.error(request, "Invalid username or password.")
    context = {'form' : form}
    return render(request, 'core/login.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

#View that handles resume uploads
def upload_resume_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ResumeUploadForm(request.POST, request.FILES)
            if form.is_valid():
                # Extract raw text from file or textarea
                resume_text = form.cleaned_data['resume_text']
                resume_file = form.cleaned_data['resume_file']

                if resume_file:
                    # Read file content (assuming text-based files; extend for PDFs etc.)
                    resume_text = resume_file.read().decode('utf-8', errors='ignore')
                parsed_entities = parse_resume(resume_text)

                # Parse skills using your existing parser
                skills_list = parsed_entities.get("SKILL", [])

                # Normalize and get or create Skill objects
                skill_objs = []
                for skill_name in skills_list:
                    skill_name_clean = skill_name.strip()
                    if skill_name_clean:
                        skill_obj, _ = Skill.objects.get_or_create(
                            name__iexact=skill_name_clean,
                            defaults={'name': skill_name_clean}
                        )
                        skill_objs.append(skill_obj)

                # Extract experience and education text from parsed entities
                # Join multiple descriptions or entries into strings
                experience_text = " ".join(parsed_entities.get("DESCRIPTION", []))
                education_text = " ".join(parsed_entities.get("EDUCATION", []))

                # Create Resume linked to current user with parsed fields
                resume = Resume.objects.create(
                    user=request.user,
                    experience=experience_text,
                    education=education_text
                )

                # Link skills
                resume.skills.set(skill_objs)
                resume.save()

                # Call similarity logic to find matching jobs for this resume
                job_matches = find_matching_jobs_for_resume(resume)

                return render(request, 'core/recommendations.html', {
                    'matches': job_matches,
                    'resume': resume,
                    'skills_objs': skill_objs
                })
              
        else:
            form = ResumeUploadForm()
    else:
        return redirect('login')
    
    context = {'form': form
               }

    return render(request, 'core/upload-resume.html',context )


@login_required
def parse_job_view(request):
    if request.method == "POST":
        job_text = request.POST.get('job_text', '').strip()
        job_file = request.FILES.get('job_file')
        
        if job_file:
            try:
                job_text = job_file.read().decode('utf-8', errors='ignore').strip()
            except Exception as e:
                messages.error(request, f"Failed to read uploaded file: {e}")
                return redirect('parse_job')
        
        if not job_text:
            messages.error(request, "Please provide job text or upload a file.")
            return redirect('parse_job')
        
        try:
            parsed_data = parse_job_posting(job_text)
            
            # Defensive: Provide a default company name if missing or empty
            company_name = parsed_data.get('company', '').strip()
            if not company_name:
                company_name = "DefaultCompanyName"
            
            # Get or create Company instance
            company, created = Company.objects.get_or_create(name=company_name, defaults={'user': request.user})
            
            # Defensive: Provide default title if missing
            job_title = parsed_data.get('title', '').strip() or "Unknown Position"
            
            # Create JobPosting instance
            job = JobPosting.objects.create(
                title=job_title,
                company=company,
                description=parsed_data.get('description', '').strip(),
                location=parsed_data.get('location', '').strip()
            )
            
            # Process skills, normalize and link
            skill_objs = []
            for skill_name in parsed_data.get('skills', []):
                skill_name_clean = skill_name.strip()
                if skill_name_clean:
                    skill, _ = Skill.objects.get_or_create(
                        name__iexact=skill_name_clean,
                        defaults={'name': skill_name_clean}
                    )
                    skill_objs.append(skill)
            
            job.skills.set(skill_objs)
            job.save()

            
            
            messages.success(request, "Job parsed and saved successfully!")
            candidate_matches = find_resume_for_job(job)

            return render(request, 'core/candidate_recommendations.html', {
            'job': job,
            'matches': candidate_matches})

        
        except Exception as e:
            messages.error(request, f"Error parsing job: {str(e)}")
            print(f"Job parsing error: {str(e)}")  # For debugging/logging

        
        
    return render(request, 'core/parse_job.html')


def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    return render(request, 'core/resume_detail.html', {'resume': resume})

def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)
    return render(request, 'core/job_detail.html', {'job': job})


'''@csrf_exempt
def parse_resume(request):
    #print("request method:", request.method)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            resume_text = data.get('resume_text')
            skills = extract_skills(resume_text)
            return JsonResponse({'skills': skills})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'POST request required'}, status=400)'''


def Home(request):
    return HttpResponse(
        '<h2>Welcome to our Jobtracker Web Application.  </h2>'
    )

def about(request):
    return render(request, "core/about.html")

def frontend(request):
    return render(request, 'core/index.html')
