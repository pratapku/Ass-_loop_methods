import datetime
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.conf import settings

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,AbstractUser
)
from django.utils import timezone


# Create your models here
class MyUserManager(BaseUserManager):
    def create_user(self, email,  password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    name = models.CharField( max_length=50)
    roll = models.CharField( max_length=50)
    M_number = models.CharField(max_length=11)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    date_of_birth = models.CharField( max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    expiry_date = models.DateTimeField(null=True, blank=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def is_out_of_credits(self):
        "Is the user out  of credits?"
        return self.credits > 0
class Post(models.Model):
    author = models.CharField( max_length=50)
    body = models.TextField(max_length=200)
    
    created_on = models.DateTimeField(default=timezone.now)

class comment (models.Model):
    txt = models.TextField(max_length=201)
    created_on = models.DateTimeField(default=timezone.now)
    author = models.CharField( max_length=50)
    post =models.ForeignKey('Post', on_delete=models.CASCADE)
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
class Sub_category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
class Product(models.Model):
    Available =(
        ('In stack','In stack'),
        ('Out of stack','Out of stack')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
   
    available  = models.CharField(max_length = 100,choices =Available,null ='True')
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Ecommerce/ping')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class contect_us(models.Model):
    name = models.CharField(max_length =100)
    email = models.EmailField(max_length =100)
    subject = models.TextField(max_length =100)
    message=models.TextField(max_length =1000)
    def __str__(self):
        return self.name