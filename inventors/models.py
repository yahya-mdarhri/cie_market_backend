from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Affiliation(models.Model):
  name = models.CharField(max_length=255, null=False)
  parent_id = models.CharField(max_length=20, null=True, blank=True)

class Inventor(models.Model):
  # 10 characters is really limited since 'inv-'+number , so 10^6 fileds are possible, the possilty to 
  # to use default auto incrementing id 
  Inventor_id = models.CharField(max_length=10, unique=True, primary_key=True) 
  preferred_name = models.CharField(max_length=150, null=False)
  name_variants = ArrayField(
    models.CharField(max_length=30),
    blank=True,
    null=True,
    default=list,
  )
  affiliation = models.ManyToManyField(Affiliation, related_name='+', blank=True)  # inventor -> affiliations (1-way)
  email = models.EmailField(unique=True, default=None)
  image = models.ImageField(upload_to='inventors/images/', default=None, blank=True, null=True)
  orcid = models.CharField(max_length=19, unique=True, default=None, blank=True, null=True)
  phone_number = models.CharField(max_length=11, blank=True, null=True, default=None)

  def __str__(self):
    return self.preferred_name

class Ticket(models.Model):
  title = models.CharField(max_length=255, null=False)
  summary = models.CharField(max_length=255, null=False)
  context = models.TextField(null=False)
  problem_identification = models.TextField(null=False)
  drawings = models.CharField(max_length=255, null=True, blank=True)
  inventors = models.ManyToManyField(Inventor, related_name='+') # ticket -> inventors (1-way)
  co_applications = ArrayField(
    models.CharField(max_length=255),
    null=True,
    blank=True,
    default=list,
  )
  status = models.CharField(max_length=255, null=False)
  meeting_date = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)

