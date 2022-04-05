import datetime
from django.db import models
from django.utils import timezone

class Country(models.Model):    
    country_name = models.CharField(max_length=300)
    capital = models.CharField(max_length=300)
    places_to_visit = models.CharField(max_length=300)
    
    def __str__(self):
        return self.capital

class Post(models.Model):
    author = models.CharField(max_length=300)
    post_title = models.CharField(max_length=300)
    post_text = models.CharField(max_length=300)
    release_date = models.DateTimeField()
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_text

    def was_published_recently(self):
        return self.release_date >= timezone.now() - datetime.timedelta(days=1)

class Image(models.Model): 
    title = models.CharField(max_length=200)
    img = models.ImageField(upload_to="media")
    country_name = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

        

country1 = Country.objects.get(pk=1)
picture1 = Image(title="Beautiful beach.", img="media/0.jpg", country_name=country1)
picture = Image.objects.get(pk=1)
