from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Inventor(models.Model):
  # 10 characters is really limited since 'inv-'+number , so 10^6 fileds are possible, the possilty to 
  # to use default auto incrementing id 
  Inventor_id = models.CharField(max_length=10, unique=True, primary_key=True) 
  preferred_name = models.CharField(max_length=150, null=False)
  name_variants = models.ArrayField(
    models.CharField(max_length=30),
    blank=True,
    null=True,
    default=list,
  )
  affiliation = models.ForeignKey('affiliation', on_delete=models.CASCADE, null=True, blank=True)
  email = models.EmailField(unique=True, default=None)
  image = models.ImageField(upload_to='inventors/images/', default=None, blank=True, null=True)
  orcid = models.CharField(max_length=19, unique=True, default=None, blank=True, null=True)
  phone_number = models.CharField(max_length=11, blank=True, null=True, default=None)

  def __str__(self):
    return self.preferred_name

class Affiliation(models.Model):
  name = models.CharField(max_length=255, null=False)
  parent_id = models.CharField(max_length=20, null=True, blank=True)