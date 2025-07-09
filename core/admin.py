from django.contrib import admin
from .models import User, Skill, Company, JobPosting, Resume
# Register your models here.

admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Company)
admin.site.register(JobPosting)
admin.site.register(Resume)
