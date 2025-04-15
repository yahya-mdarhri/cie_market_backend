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
  drawings = models.CharField(max_length=255, null=True, blank=True) # maybe a file field
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

class Patent(models.Model):
  RESEARCH_REPORT_RESULT = ( # will be change
    ('A', 'MAI'), # manque de activité invontive
    ('B', 'MR'),# manque de reuvendication
    ('C', 'B1'), # brevet accordé
    ('D','REFUSE'), # refuse
  )
  PATENT_STATUS = ( # will be change
    ('A', 'A1'),
    ('B', 'B1'), # add trigger if Research report result is B1 this status will be b1
  )
  CONTRACT_TYPE = ( # will be change
    ('A', 'Option A'),
    ('B', 'Option B'),
    ('C', 'Option C'),
  )
  NATURE = ( # will be change
    ('A', 'METHOD'),
    ('B', 'SYSTEM'),
    ('C', 'PRODUCT'),
    ('D', 'DEVICE'),
    ('E', 'MATERIAL'),
  )
  SECTOR = {
    ("A", "Aerospace & Defense"),
    ("B", "Agriculture"),
    ("C", "Automotive & Transportation"),
    ("D", "Biotechnology"),
    ("E", "Chemicals & Materials"),
    ("F", "Consumer Goods"),
    ("G", "Electronics"),
    ("H", "Energy & Renewables"),
    ("I", "Healthcare & Pharmaceuticals"),
    ("J", "Information Technology & Software"),
    ("K", "Manufacturing & Industrial Equipment"),
    ("L", "Telecommunications"),
  }

  title = models.CharField(max_length=255, null=False, blank=False)
  deposit_number = models.BigIntegerField(null=False, unique=True)
  deposit_document = models.CharField(max_length=255, null=False, blank=False) # maybe a file field
  deposit_date = models.DateField(null=False)
  research_report_document = models.CharField(max_length=255, null=False, blank=False) # maybe a file field
  research_report_result = models.CharField(max_length=1, choices=RESEARCH_REPORT_RESULT, default='A') # Note_1
  research_report_date = models.DateField(null=False)
  delivery_document = models.CharField(max_length=255, null=False, blank=False) # maybe a file field
  delivery_date = models.DateField(null=False)
  status = models.CharField(max_length=1, choices=PATENT_STATUS, null=False, default='A') # Note_1
  inventors = models.ManyToManyField(Inventor, related_name='+') # no reverse relation
  TRL_level = models.BigIntegerField(null=True, blank=True)
  CRL_level = models.BigIntegerField(null=True, blank=True)
  affiliation = models.ManyToManyField(Affiliation, related_name='+', blank=True) # no reverse relation
  abstract = models.TextField(null=False, blank=False)
  contract_type = models.CharField(max_length=1, choices=CONTRACT_TYPE, null=False, default='A') # Note_1
  sector = models.CharField(max_length=1, choices=SECTOR, null=False, default='A') # Note_1
  nature = models.CharField(max_length=1, choices=NATURE, null=False, default='A') # Note_1
  schemas = ArrayField(
    models.CharField(max_length=255),#  may change to file field
    null=True,
    blank=True,
    default=list,
  )


  # Note_1: are only app enum level , but stored as char field in the database | may be change to an actual enum later


# class AffiliationsUir(models.Model):
#     id = models.CharField(primary_key=True, max_length=20)
#     name = models.CharField(max_length=255)
#     parent_id = models.CharField(max_length=20, blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'affiliations_uir'


# class Inventors(models.Model):
#     id = models.CharField(primary_key=True, max_length=10)
#     preferred_name = models.CharField(max_length=150)
#     name_variants = models.TextField(blank=True, null=True)
#     affiliation = models.CharField(max_length=200, blank=True, null=True)
#     email = models.CharField(unique=True, max_length=150, blank=True, null=True)
#     image = models.CharField(max_length=300, blank=True, null=True)
#     orcid = models.CharField(unique=True, max_length=19, blank=True, null=True)
#     phone = models.CharField(max_length=11, blank=True, null=True)
#     password = models.CharField(max_length=300)

#     class Meta:
#         managed = False
#         db_table = 'inventors'