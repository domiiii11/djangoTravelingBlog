from django.http import HttpResponseNotFound
from django.shortcuts import render
from blog.models import Post, Country, Image
from blog.forms import PostForm, CountryForm, ImageForm
import datetime

choices_ = Country.objects.all()
choices__ = {country.id: country.country_name for country in choices_}

def index(request):
    posts = Post.objects.order_by('release_date')
    posts_dictionary = {}
    for post in posts:
        images = Image.objects.filter(country_name=post.country_name)
        image_list = [image for image in images]
        if image_list:
            posts_dictionary[post] = image_list[0]
        else:
            posts_dictionary[post] = None
    context = {'posts_dictionary': posts_dictionary}
    return render(request, "blog/index.html", context)


def create_post(request):
    post_form = PostForm()
    (print("choices VIEW"))
    print("post-method-not-success")  
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        print("post-method-success")
        print(post_form.is_valid())
        if post_form.is_valid():
            author_ = post_form['author']
            post_title_ = post_form.cleaned_data['post_title']
            post_text_ = post_form.cleaned_data['post_text']
            release_date_ = post_form.cleaned_data['release_date']
            country_id = post_form.cleaned_data['country']
            country_ = Country.objects.get(id=int(country_id[0]))
            post = Post(author=author_, post_title=post_title_, post_text=post_text_, release_date=release_date_,
                        country_name=country_)
            post.save()
    return render(request, 'blog/create-post.html', {'post_form': post_form,
                                                     'choices': choices__})

                                                     
def edit_post(request, post_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            particular_object = Post.objects.get(pk=post_id)
            particular_object.author = form.cleaned_data['author']
            particular_object.post_title = form.cleaned_data['post_title']
            particular_object.post_text = form.cleaned_data['post_text']
            particular_object.release_date = form.cleaned_data['release_date']
            country_id = form.cleaned_data['country']
            country_ = Country.objects.get(id=int(country_id[0]))
            particular_object.country_name = country_
            particular_object.save()
    else:
        form = PostForm()
    return render(request, 'blog/edit.html', {'form': form})


def create_country(request):
    if request.method == 'POST':
        country_form = CountryForm(request.POST)
        print(country_form.is_valid())
        if country_form.is_valid():
            country_name_ = country_form.cleaned_data['country_name']
            capital_ = country_form.cleaned_data['capital']
            places_to_visit_ = country_form.cleaned_data['places_to_visit']
            country = Country(country_name=country_name_,
                              capital=capital_, places_to_visit=places_to_visit_)
            country.save()
    else:
        country_form = CountryForm()
        print(country_form)
    return render(request, 'blog/create-country.html', {'country_form': country_form})

def upload_image(request):
    image_form = ImageForm()
    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES)  
        print(image_form)  
        if image_form.is_valid():
            title_ = image_form.cleaned_data['title']
            country_id = image_form.cleaned_data['country']
            country_ = Country.objects.get(id=int(country_id[0]))
            img_ = image_form.cleaned_data.get('image')
            image = Image(title=title_, img=img_, country_name=country_)
            image.save()
    return render(request, 'blog/upload-image.html', {'image_form': image_form,
                                                     'choices': choices__})

def boot(request):
    return render(request, 'blog/boot.html')

def load_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    image = Image.objects.filter(country_name=post.country_name)[0]
    context = {'post': post,
                'image': image}
    return render(request, 'blog/load-post.html', context)


def scss(request):
    return render(request, 'blog/indexc.html')
