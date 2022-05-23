from django.http import HttpResponseNotFound
from django.shortcuts import render
from blog.models import Post, PlaceToVisit, Image
from blog.forms import PostForm, PlaceToVisitForm, ImageForm
import datetime

choices_ = PlaceToVisit.objects.all()
choices__ = {place_to_visit.id: place_to_visit.place_to_visit_name for place_to_visit in choices_}

def index(request):
    posts = Post.objects.order_by('release_date')
    posts_dictionary = {}
    for post in posts:
        images = Image.objects.filter(place_to_visit_name=post.place_to_visit_name)
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
            place_to_visit_id = post_form.cleaned_data['place_to_visit']
            place_to_visit_ = PlaceToVisit.objects.get(id=int(place_to_visit_id[0]))
            post = Post(author=author_, post_title=post_title_, post_text=post_text_, release_date=release_date_,
                        place_to_visit_name=place_to_visit_)
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
            place_to_visit_id = form.cleaned_data['place_to_visit']
            place_to_visit_ = PlaceToVisit.objects.get(id=int(place_to_visit_id[0]))
            particular_object.place_to_visit_name = place_to_visit_
            particular_object.save()
    else:
        form = PostForm()
    return render(request, 'blog/edit.html', {'form': form})


def create_place_to_visit(request):
    if request.method == 'POST':
        place_to_visit_form = PlaceToVisitForm(request.POST)
        print(place_to_visit_form.is_valid())
        if place_to_visit_form.is_valid():
            place_to_visit_name_ = place_to_visit_form.cleaned_data['place_to_visit_name']
            capital_ = place_to_visit_form.cleaned_data['capital']
            places_to_visit_ = place_to_visit_form.cleaned_data['places_to_visit']
            place_to_visit = PlaceToVisit(place_to_visit_name=place_to_visit_name_,
                              capital=capital_, places_to_visit=places_to_visit_)
            place_to_visit.save()
    else:
        place_to_visit_form = PlaceToVisitForm()
        print(place_to_visit_form)
    return render(request, 'blog/create-place-to-visit.html', {'place_to_visit_form': place_to_visit_form})

def upload_image(request):
    image_form = ImageForm()
    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES)  
        print(image_form)  
        if image_form.is_valid():
            title_ = image_form.cleaned_data['title']
            place_to_visit_id = image_form.cleaned_data['place_to_visit']
            place_to_visit_ = PlaceToVisit.objects.get(id=int(place_to_visit_id[0]))
            img_ = image_form.cleaned_data.get('image')
            image = Image(title=title_, img=img_, place_to_visit_name=place_to_visit_)
            image.save()
    return render(request, 'blog/upload-image.html', {'image_form': image_form,
                                                     'choices': choices__})

def boot(request):
    return render(request, 'blog/boot.html')

def load_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    image = Image.objects.filter(place_to_visit_name=post.place_to_visit_name)[0]
    context = {'post': post,
                'image': image}
    return render(request, 'blog/load-post.html', context)


def scss(request):
    return render(request, 'blog/indexc.html')
