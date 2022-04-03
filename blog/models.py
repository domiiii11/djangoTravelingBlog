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
    class Meta:
        db_table = "gallery"

# country1 = Country(country_name="Greece", capital="Athens", places_to_visit="Cafes and restarants")
# country1.save()

# post1 = Post(author="Me", post_title="My vocations", post_text="Traveling is so wonderfull thing everyone loves it.", release_date=timezone.now(), country_name=country1)

# post1.save()
# print(post1.id)


