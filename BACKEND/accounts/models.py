# models.py
from django.contrib.auth.models import User
from django.db import models

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    programme = models.CharField(max_length=200)
    year_of_study = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    discription = models.TextField()

    def __str__(self):
        return self.company_name
