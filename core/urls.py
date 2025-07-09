from django.urls import path

from .views import parse_resume, Home, about, frontend, upload_resume_view, register_view, login_view, logout_view, parse_job_view, job_detail,  resume_detail

urlpatterns = [


    path('parse-resume/', parse_resume, name = 'parse_resume'), 
    path('Home/', Home, name = 'Home'), 
    path('about/', about, name='about'),
    path('index/', frontend, name='Index'),
    path('upload-resume/', upload_resume_view, name='upload_resume'),
    path('parse-job/', parse_job_view, name = 'parse_job' ),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('resume/<int:resume_id>/', resume_detail, name='resume_detail'),
    path('job/<int:job_id>/', job_detail, name='job_detail'),
    
]