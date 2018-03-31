from django.db import models
from django.utils.text import slugify
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from bigchaindb_driver.crypto import generate_keypair
from hashlib import sha256
from .pyscripts.bigchain import assets
from .pyscripts.encrypt import encryption

# Each subclass of models.Model is associated with a table in the server DB.
       

class Docker(models.Model):
    # Model for Docker data.
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=110, unique=True)
    unique_id = models.CharField(max_length=100)
    
    developer = models.ForeignKey('DockerMarket.User', on_delete='CASCADE')
    file = models.FileField(upload_to="DockerMarket/dockers")
    password = models.CharField(max_length=50, blank=True)
    
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
                
        # Register docker as a digital asset on the blockchain
        asset_type = "New docker"
        assets.register(hex_dig, hex_dig, pub, priv, asset_type)
        
        # Generate slug for url mapping
        self.slug = slugify(self.title)
        
        # Encrypt & save file
        key = encryption.getKey(self.password)
        self.file = encryption.cipher("encrypt", key, self.file)
        
        # First save
        super(Docker, self).save(*args, **kwargs)
        
        # Save docker access details to Developer's keys & clear password field
        self.developer.keys.create(
            unique_id=hex_dig,
            key=key,
            )
        
        self.password = ""
        
        # Second save
        super(Docker, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
        

class User(models.Model):
    # Model for user data.
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    unique_id = models.CharField(max_length=100)
    
    keys = models.ManyToManyField('DockerMarket.Key', blank=True)
    
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
        
        # Register docker as a digital asset on the blockchain
        assets.register(hex_dig, hex_dig, pub, priv, asset_type)
        
        super(User, self).save(*args, **kwargs)


# Each subclass of ModelForm is a form that is associated with a given model.

class Key(models.Model):
    unique_id = models.CharField(max_length=100, primary_key=True)
    key = models.BinaryField()

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
                    'developer',
                    'file',
                    'password',
                  ]