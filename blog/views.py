from django.http import HttpResponseNotFound
from django.shortcuts import render
from blog.models import Post, Country
from django import forms
from blog.forms import NameForm
from django.http import HttpResponseRedirect


def index(request):
    posts = Post.objects.order_by('release_date')
    numbers = []
    for post in posts:
        numbers.append(post.id)
        print(numbers)
    countries = Country.objects.all()    
    context = {'posts': posts,
               "country": countries,
               "numbers": numbers}
    return render(request, "blog/index.html", context)


def create_post(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            post_title = form.cleaned_data['post_title']
            post_text = form.cleaned_data['post_text']
            release_date = form.cleaned_data['release_date']
            country = Country(country_name="Greece", capital="Athens", places_to_visit="Cafes and restarants")
            country.save()
            post= Post(author, post_title, post_text, release_date, country)
            post.save()
    else:
            form = NameForm()            
    return render(request, 'blog/edit.html', {'form': form})


def edit_post(request, post_id):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            particular_object = Post.objects.get(pk=post_id)
            particular_object.author  = form.cleaned_data['author']
            particular_object.post_title = form.cleaned_data['post_title']
            particular_object.post_text = form.cleaned_data['post_text']
            particular_object.release_date = form.cleaned_data['release_date']
            country1_ = Country(country_name="Greece", capital="Athens", places_to_visit="Cafes and restarants")
            country1_.save()
            particular_object.country_name = country1_
            particular_object.save()
    else:
            form = NameForm()            
    return render(request, 'blog/edit.html', {'form': form})


def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {'post': post,
               }
    return render(request, 'blog/post.html', context)
