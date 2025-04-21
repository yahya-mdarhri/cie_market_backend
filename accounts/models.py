from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.hashers import make_password


from inventors.models import Inventor

class UserManager(BaseUserManager):

  def create_user(self, email: str,password: str = None, **extra_fields) -> 'User':
    if not email:
        raise ValueError('The email must be given')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.password = make_password(password)
    user.save()
    return user
  
  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)

    if extra_fields.get("is_staff") is not True:
        raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
        raise ValueError("Superuser must have is_superuser=True.")

    return self.create_user(email, password, **extra_fields)

class User(PermissionsMixin, AbstractBaseUser):

  EMAIL_FIELD = 'email'
  USERNAME_FIELD = 'email'

  objects = UserManager()

  email = models.EmailField(unique=True)
  inventor = models.OneToOneField(
    Inventor,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name='+'
  )
  password = models.CharField(max_length=128)

  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)

  def __str__(self):
      return self.email

  class Meta:
    db_table = 'users'