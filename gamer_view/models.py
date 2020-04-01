from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg



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
	username=models.CharField(max_length=20)
	password=models.CharField(max_length=20)

	def __str__(self):
		return self.user
    
	
	
class Reviews(models.Model):
	game_id=models.PositiveIntegerField(unique=True,db_index=True,
				   validators=[MinValueValidator(0),MaxValueValidator(10)])
	REVIEW_ID = models.PositiveIntegerField(unique=True,db_index=True,
					validators=[MinValueValidator(0),MaxValueValidator(10)])
	review=models.CharField(max_length=500)
	madeby_name=models.CharField(max_length=20)
	timecreated=models.DateTimeField(auto_now=True)
	rating=models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(10)])
	def __str__(self):
	    return self.reviews    

class Page(models.Model):
	categories_choice=(
		(0,'FPS'),
		(1,'MOBA'),	
		(2,'Action'),
		(3, 'MMORPG'),
		(4,'Strategy'),
		(5,'Sport'),	
	)
	gameid=models.PositiveIntegerField(unique=True,db_index=True,
				   validators=[MinValueValidator(0),MaxValueValidator(10)])
	gamename=models.CharField(max_length=20,unique=True)
					   
	# This to choice different type.
	category=models.CharField(max_length=20,choices=categories_choice)
					   
					   
	# This is average rating.
	average_rating=Reviews.objects.values('game_id').annotate(Avg('rating'))
					   			   
					   
	addby_name=models.CharField(max_length=20)
	time_created=models.DateTimeField(auto_now_add=True)
	Description=models.CharField(max_length=500)
	image = models.ImageField(upload_to='game_images', blank=True)
	view=picture = models.PositiveIntegerField(validators=[MinValueValidator(0),MaxValueValidator(10)])
	def __str__(self):
	    return self.page.gamename
	
	
	
	
	
    
