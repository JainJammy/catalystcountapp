from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Sets the user's password
        user.save(using=self._db)
        return user
"""creating custom user model for user signup"""    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
"""creating models for query builder"""   
class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    year_founded = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    employees = models.IntegerField(null=True, blank=True)