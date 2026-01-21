from django.db import models

# Create your models here.
class Studentprofile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    programme = models.CharField(max_length=200, blank=True)
    year_of_study = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True,
        default='profile_pictures/default.png'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Companyprofile(models.Model):
    company_name = models.CharField(max_length=100)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.company_name        