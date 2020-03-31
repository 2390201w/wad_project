from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
    
    
    
class User(models.Model):
	userid=models.CharField(max_length=20,unique=True)
	usename=models.CharField(max_length=20)
	password=models.CharField(max_length=20)

    def __str__(self):
        return self.user
    
class Reviews(models.Model):
    REVIEWI_ID = models.IntegerField(unique=True,db_index=True)
	review=models.CharField(max_length=500)
	madeby_name=models.CharField(max_length=20)
	timecreated=models.DateTimeField(auto_now=True)
	rating=models.SmallIntegerField
	def __str__(self):
	    return self.reviews    

    
    
