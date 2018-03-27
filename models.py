from django.db import models
from django.utils.text import slugify

# Each subclass of models.Model is associated with a table in the server DB.

class MetagenomicSample(models.Model):
    # Model for metagenomic sample data.
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=110, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(MetagenomicSample, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
        

class Docker(models.Model):
    # Model for Docker data.
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=110, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(MetagenomicSample, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
        

class User(models.Model):
    # Model for user data.
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    
    def __str__(self):
        fullName = str(self.firstName, self.lastName)
        return fullName