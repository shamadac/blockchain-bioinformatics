from django.db import models
from django.utils.text import slugify
from django.forms import ModelForm

from bigchaindb_driver.crypto import generate_keypair
from hashlib import sha256
from .pyscripts.bigchain import assets

# Each subclass of models.Model is associated with a table in the server DB.
       

class Docker(models.Model):
    # Model for Docker data.
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=110, unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Docker, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
        

class User(models.Model):
    # Model for user data.
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    unique_id = models.CharField(max_length=100)
    
    def __str__(self):
        fullName = str(self.firstName + "" + self.lastName)
        return fullName
    
    def save(self, *args, **kwargs):

        # Make public & private keypair
        user_keys = generate_keypair()
        priv = user_keys.private_key
        pub = user_keys.public_key
        
        # Set user's unique ID to be hash of public & private keys
        b = bytes(priv + pub, "utf8")
        hash = sha256(b)
        hex_dig = hash.hexdigest()     
        self.unique_id = hex_dig
        asset_type = "New user"
        assets.register(hex_dig, hex_dig, pub, priv, asset_type)
        super(User, self).save(*args, **kwargs)


# Each subclass of ModelForm is a form that is associated with a given model.

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = [
                    'firstName',
                    'lastName',
                    'email',
                  ]

class DockerSubmissionForm(ModelForm):
    class Meta:
        model = Docker
        fields = [
                    'title',
                    'description',
                  ]