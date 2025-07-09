from django.db import models
from django.contrib.auth.models import AbstractUser

mode = (('Personal',"Personal"),
         ('Business',"Business"))

class User(AbstractUser):

    email = models.EmailField(unique=True)
    mode = models.CharField(max_length=10, choices=mode, default="Personal")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Skill(models.Model):
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='job_postings')
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='DefaultCompanyName')
    skills = models.ManyToManyField(Skill, related_name='resumes')
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume of {self.user.username}"
