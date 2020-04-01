from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from django.template.defaultfilters import slugify


# Create your models here.
class Category(models.Model):
    category=models.CharField(max_length=30, unique=True)
    slug=models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(selfname)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural= 'Categories'

    def __str__(self):
        return self.category

class Page(models.Model):
    gamename=models.CharField(max_length=20,unique=True)

    # links the page to category M:1
    category= models.ForeignKey(Category, on_delete=models.CASCADE)
					   
					   
    # This is average rating.
    # wont work cos reviews is not created before page
   # average_rating=Reviews.objects.values('gamename').annotate(Avg('rating'))
					   			   
					   
    addby_name=models.CharField(max_length=20)
    time_created=models.DateTimeField(auto_now_add=True)
    Description=models.CharField(max_length=500)
    image = models.ImageField(upload_to='game_images', blank=True)
    views=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.page.gamename	

    
class Reviews(models.Model):

    # Links the review to Page(Game) M:1 
    gamename=models.ForeignKey(Page, on_delete=models.CASCADE)
    
    REVIEW_ID = models.PositiveIntegerField(unique=True,db_index=True,
                                    validators=[MinValueValidator(0)])
    
    review=models.CharField(max_length=500)
    madeby_name=models.CharField(max_length=20)
    timecreated=models.DateTimeField(auto_now=True)
    rating=models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])

    def __str__(self):
        return self.review

	
	
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

	
    
