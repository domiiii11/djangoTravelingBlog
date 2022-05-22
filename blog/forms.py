from concurrent.futures import InvalidStateError
from django import forms
from blog.models import Country, Post, Image
import datetime

choices_ = Country.objects.all()
print(choices_)
(print("choices FORM"))
# choices_ = {country.id : country.country_name for country in choices_}
# # for element in choices_: ids.append(element.id)
choices_ = Country.objects.all()
# choices__ = {country.id: country.country_name for country in choices_}
choices__ = [(country.id , country.country_name) for country in choices_]

class ImageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    country = forms.MultipleChoiceField(label='Country', choices=choices_)
    image = forms.ImageField()

class CountryForm(forms.Form):
    country_name = forms.CharField(label='Country', max_length=100)
    capital = forms.CharField(label='Capital', max_length=100)
    places_to_visit = forms.CharField(label='Places to visit', max_length=100)

class PostForm(forms.Form):
    author = forms.CharField(label='Author', max_length=100)
    post_title = forms.CharField(label='Post title', max_length=100)
    post_text = forms.CharField(label='Post text', max_length=3000)
    release_date = forms.DateField(label= 'Release date', initial=datetime.date.today)
    country = forms.MultipleChoiceField(label= 'Country', choices=choices__)

