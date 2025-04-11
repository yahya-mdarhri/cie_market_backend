from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Inventor(models.Model):
  Inventor_id = models.CharField(max_length=10, unique=True, primary_key=True) # 10 characters is really limited since 'inv-'+number , so 1000000 fileds are possible
  preferred_name = models.CharField(max_length=150, null=False)
  name_variants = models.ArrayField(
    models.CharField(max_length=30),
    blank=True,
    null=True,
    default=list,
  )
  # affiliation : adding affiliation field later when its model is ready
  email = models.EmailField(unique=True)
  image = models.ImageField(upload_to='inventors/images/', default=None, blank=True, null=True)
  orcid = models.CharField(max_length=19, unique=True, default=None, blank=True, null=True)
  phone_number = models.CharField(max_length=11, blank=True, null=True, default=None)

  def __str__(self):
    return self.preferred_name

