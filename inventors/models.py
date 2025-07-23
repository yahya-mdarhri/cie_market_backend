import uuid
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Affiliation(models.Model):
  id = models.CharField(primary_key=True, max_length=20)
  name = models.CharField(max_length=255, null=False)
  parent_id = models.CharField(max_length=20, null=True, blank=True)

  def __str__(self):
    return self.name

  class Meta:
    db_table = 'affiliations'

class Inventor(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  preferred_name = models.CharField(max_length=150, null=False)
  name_variants = ArrayField(
    models.CharField(max_length=30),
    blank=True,
    null=True,
    default=list,
  )
  affiliation = models.ForeignKey(
    Affiliation,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='inventors'
  )
  email = models.EmailField(default=None,null=True, blank=True)
  image = models.ImageField(upload_to='avatars/', default=None, blank=True, null=True)
  orcid = models.CharField(max_length=19, default=None, blank=True, null=True)
  phone_number = models.CharField(max_length=11, blank=True, null=True, default=None)

  def __str__(self):
    return self.preferred_name
  
  class Meta:
    db_table = 'inventors'

class Ticket(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255, null=False)
  summary = models.CharField(max_length=255, null=False)
  context = models.TextField(null=False)
  problem_identification = models.TextField(null=False)
  drawings = models.FileField(upload_to='drawings/', null=True, blank=True)  # <-- single file field
  inventors = models.ManyToManyField(Inventor, related_name='+') # ticket -> inventors (1-way)
  co_applications = ArrayField(
    models.CharField(max_length=255),
    null=True,
    blank=True,
    default=list,
  )
  status = models.CharField(max_length=7, null=False, default='pending')
  meeting_date = models.DateTimeField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  is_draft = models.BooleanField(default=True)

  class Meta:
    db_table = 'tickets'

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
  SECTOR = (
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
  )
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=255, null=False, blank=False)
  deposit_number = models.BigIntegerField(null=False, unique=True)
  deposit_document = models.CharField(max_length=255, null=False, blank=False) # maybe a file field
  deposit_date = models.DateField(null=True, blank=True)
  research_report_document = models.CharField(max_length=255, null=False, blank=False) # maybe a file field
  research_report_result = models.CharField(max_length=1, choices=RESEARCH_REPORT_RESULT, default='A') # Note_1
  research_report_date = models.DateField(null=True, blank=True)
  delivery_document = models.CharField(max_length=255, null=False, blank=False) # maybe a file field
  delivery_date = models.DateField(null=True, blank=True)
  status = models.CharField(max_length=1, choices=PATENT_STATUS, null=False, default='A') # Note_1
  inventors = models.ManyToManyField(Inventor, related_name='inventors') # no reverse relation
  TRL_level = models.BigIntegerField(null=True, blank=True)
  CRL_level = models.BigIntegerField(null=True, blank=True)
  affiliation = models.ForeignKey(
    Affiliation,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='patents'
  )
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

  class Meta:
    db_table = 'patents'