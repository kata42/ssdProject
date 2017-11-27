from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, default='M',choices=GENDER_CHOICES)
    profileFilled  = models.IntegerField(default=0)
    bdate = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d',blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    organization = models.CharField(max_length=250)
    speciality = models.CharField(max_length=250)
    rating = models.IntegerField(default=0)
    phoneNumber = models.IntegerField(default=1234567890)
    address = models.CharField(max_length=250,default=None)

    def __str__(self):
        return str(self.user.username)

class specialities(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    speciality_name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.speciality_name)

class insurances(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    insurance_name = models.CharField(max_length=250)

    def __str__(self):
        return str(self.insurance_name)
