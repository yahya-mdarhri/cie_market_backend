from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Inventor(AbstractUser):
  preferred_name = models.CharField(max_length=255, blank=True, null=True)
  # name variants : adding this field later when its datatype is decided
  # affiliation : adding affiliation field later when its model is ready
  email = models.EmailField(unique=True)
  image = models.ImageField(upload_to='inventor_images/', blank=True, null=True)
  orcid = models.UUIDField(unique=True, blank=True, null=True)
  phone_number = models.CharField(max_length=20, blank=True, null=True)

  def __str__(self):
    return self.preferred_name

