from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


GENDER_CHOICES = (
    ("Male","Male"),
    ("Female","Female")
)


class User(AbstractUser):
    is_patient = models.BooleanField(default = False)
    is_mentor = models.BooleanField(default = False)

# Create your models here.
class Patient(models.Model):
    patient = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, null = False, blank = False)
    age = models.IntegerField(null = False, blank = False)
    gender = models.CharField(max_length = 20, choices = GENDER_CHOICES)
    dob = models.DateField(blank = False, null = False)


    def __str__(self):
        return f'{self.id}-{self.name}'

class Mentor(models.Model):
    mentor = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    name = models.CharField(max_length = 100, null = False, blank = False)
    age = models.IntegerField(null = False, blank = False)
    gender = models.CharField(max_length = 20,blank = False, null = False)
    specialization = models.CharField(max_length = 200,blank = False, null = False)
    experience = models.IntegerField(blank = False, null = False)
    consultation_charges = models.IntegerField(blank = False, null = False)


class ScoreBoard(models.Model):
    TEST_CHOICES = (
        ("Rapid Color Naming","Rapid Color Naming"),
        ("Reading Comprehension Test","Reading Comprehension Test"),
        ("Handwriting Recognition Test","Handwriting Recognition Test"),
        ("Object Classification Test","Object Classification Test"),
    
    )
    score = models.IntegerField(null = False, blank = False)
    timestamp = models.DateTimeField(auto_now_add = True)
    type_of_test = models.CharField(max_length = 100, choices = TEST_CHOICES)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    




