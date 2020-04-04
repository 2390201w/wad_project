from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from datetime import datetime

class Category(models.Model):
    
    category=models.CharField(max_length=30, primary_key=True)
    class Meta:
        verbose_name_plural= 'Categories'

    def __str__(self):
        return self.category

class Page(models.Model):
    gamename=models.CharField(max_length=30,unique=True)

    # links the page to category M:1
    cat= models.ForeignKey(Category, on_delete=models.CASCADE)
					   		   
    date_created=models.DateField(default= datetime.now)
    description=models.CharField(max_length=500)
    image = models.ImageField(upload_to='game_images', blank=True)
    views=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.gamename
    
class UserProfile(models.Model):
    
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
class Review(models.Model):
    # Links the review to Page(Game) M:1 
    gamename=models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
      
    review=models.CharField(max_length=500)
    madeby=models.ForeignKey(UserProfile,on_delete=models.CASCADE , null=True)
    datecreated=models.DateField(default=datetime.now)
    rating=models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])

    def __str__(self):
        return f"{self.gamename}:{self.madeby}"    

