from django import forms
import datetime

class NameForm(forms.Form):
    author = forms.CharField(label='Author', max_length=100)
    post_title = forms.CharField(label='Post title', max_length=100)
    post_text = forms.CharField(label='Post text', max_length=100)
    release_date = forms.DateField(label= 'Release date', initial=datetime.date.today)
    country_name = forms.CharField(label='Country', max_length=100)

