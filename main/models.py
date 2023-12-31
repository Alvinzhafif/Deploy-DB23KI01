from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import uuid
class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The phone_number is not given")
        user = self.model(phone_number = phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone_number, password, **extra_fields)
class User(AbstractUser):
    phone_number = models.CharField(unique=True, default=uuid.uuid4, max_length=15)
    password = models.CharField(max_length=50, blank=False)
    is_admin = models.BooleanField(default=False)
    is_child = models.BooleanField(default=False)
    is_caregiver = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    username = models.CharField(max_length=150, blank=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()
    

class ChildProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.TextField(default='', blank=False)
    last_name = models.TextField(default='', blank=False)
    address = models.TextField(blank=False)
    gender = models.CharField(max_length=10, blank=False)
    dob = models.DateField(blank=False, null=True)
    father_name = models.CharField(max_length=100, blank=False)
    father_occupation = models.CharField(max_length=100, blank=False)
    mother_name = models.CharField(max_length=100, blank=False)
    mother_occupation = models.CharField(max_length=100, blank=False)
  

class CaregiverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.TextField(default='', blank=False)
    last_name = models.TextField(default='', blank=False)
    address = models.TextField(blank=False)
    gender = models.CharField(max_length=10, blank=False)
    dob = models.DateField(blank=False, null=True)
    nik = models.CharField(max_length=20, blank=False)
    npwp = models.CharField(max_length=20, blank=False)
    bank_name = models.CharField(max_length=100, blank=False)
    bank_account_number = models.CharField(max_length=30, blank=False)
class Certificate(models.Model):
    caregiver = models.ForeignKey(CaregiverProfile, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=100, blank=False)
    number = models.CharField(max_length=50, blank=False)
    year = models.IntegerField(blank=False)
    organizer = models.CharField(max_length=100, blank=False)

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.TextField(default='', blank=False)
    last_name = models.TextField(default='', blank=False)
    address = models.TextField(blank=False)
    gender = models.CharField(max_length=10, blank=False)
    dob = models.DateField(blank=False, null=True)
    nik = models.CharField(max_length=20, blank=False)
    npwp = models.CharField(max_length=20, blank=False)
    bank_name = models.CharField(max_length=100, blank=False)
    bank_account_number = models.CharField(max_length=30, blank=False)
    driver_license_number = models.CharField(max_length=50, blank=False)
    available_working_days = models.ManyToManyField('WorkingDay')
class WorkingDay(models.Model):
    day_name = models.CharField(max_length=20, blank=False) 

    def __str__(self):
        return self.day_name


