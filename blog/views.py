from django.http import HttpResponseNotFound
from django.shortcuts import render
from blog.models import Post, Country, Image
from blog.forms import PostForm, CountryForm, ImageForm



def index(request):
    posts = Post.objects.order_by('release_date')
    posts_dictionary = {}
    for post in posts:
        images = Image.objects.filter(country_name = post.country_name)
        image_list = [image for image in images]
        if image_list:
            posts_dictionary[post] = image_list[0]
            print(image_list[0])
        else:
            posts_dictionary[post] = None
    print(posts_dictionary)    
    context = {'posts_dictionary': posts_dictionary}
    return render(request, "blog/index.html", context)


def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        country_form = CountryForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        if post_form.is_valid():
            author_ = post_form.cleaned_data['author']
            post_title_ = post_form.cleaned_data['post_title']
            post_text_ = post_form.cleaned_data['post_text']
            release_date_ = post_form.cleaned_data['release_date']
            country_ = Country(country_name="Greece", capital="Athens",
                               places_to_visit="Cafes and restarants")
            country_.save()
            post = Post(author=author_, post_title=post_title_, post_text=post_text_,
                        release_date=release_date_, country_name=country_)
            post.save()
        if image_form.is_valid():
            title_ = image_form.cleaned_data['title']
            country_id = image_form.cleaned_data['country']
            country_ = Country.objects.get(id=int(country_id[0]))
            img_ = image_form.cleaned_data.get('image')
            image = Image(title=title_, img=img_, country_name=country_)
            image.save()
        if country_form.is_valid():
            country_name_ = country_form.cleaned_data['country_name']
            capital_ = country_form.cleaned_data['capital']
            places_to_visit_ = country_form.cleaned_data['places_to_visit']
            country = Country(country_name=country_name_,
                              capital=capital_, places_to_visit=places_to_visit_)
            country.save()
    else:
        post_form = PostForm()
        country_form = CountryForm()
        image_form = ImageForm()
    return render(request, 'blog/create.html', {'post_form': post_form,
                                                'country_form': country_form,
                                                'image_form': image_form})


def edit_post(request, post_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            particular_object = Post.objects.get(pk=post_id)
            particular_object.author = form.cleaned_data['author']
            particular_object.post_title = form.cleaned_data['post_title']
            particular_object.post_text = form.cleaned_data['post_text']
            particular_object.release_date = form.cleaned_data['release_date']
            country1_ = Country(
                country_name="Greece", capital="Athens", places_to_visit="Cafes and restarants")
            country1_.save()
            particular_object.country_name = country1_
            particular_object.save()
    else:
        form = PostForm()
    return render(request, 'blog/edit.html', {'form': form})


def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {'post': post,
               }
    return render(request, 'blog/post.html', context)
