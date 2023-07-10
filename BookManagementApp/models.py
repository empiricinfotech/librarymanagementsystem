from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import datetime 
from datetime import timedelta
# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=299)
    author = models.CharField(max_length=299)
    publication = models.CharField(max_length=299)
    bookNo = models.IntegerField(unique=True)
    qty= models.IntegerField()
    available_qty = models.IntegerField(default=None,null=False)
    issued_qty = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    email = models.EmailField(('email address'), unique=True)
        
    def __str__(self):
        return self.email  
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
def expiry():
    return datetime.datetime.today() + timedelta(days=14)

STATUS_CHOICES = (
    ("Issued","Issued"),
    ("Return","Return"),
    ("Requested","Requested")
    )

class IssuedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length = 20,choices = STATUS_CHOICES,default = 'Issued')
    requested_date = models.DateField(auto_now=True)
    issued_date = models.DateTimeField(auto_now=False,blank=True, null=True)
    expiry_date = models.DateField(default=expiry ,null=True)
    
    def __str__(self):
        return self.book.name
    
    class Meta:
        ordering = ['status']
    
    
    