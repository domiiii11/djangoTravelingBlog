from django.http import HttpResponseNotFound
from django.shortcuts import render
from blog.models import Post, PlaceToVisit, Image
from blog.forms import PostForm, PlaceToVisitForm, ImageForm
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse



choices_ = PlaceToVisit.objects.all()
choices__ = {place_to_visit.id: place_to_visit.places_to_visit for place_to_visit in choices_}

def index(request):
    posts = Post.objects.order_by('release_date')
    posts_dictionary = {}
    for post in posts:
        print(post)
        images = Image.objects.filter(places_to_visit=post.places_to_visit)
        image_list = [image for image in images]
        print(image_list)
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
            author_ = post_form.cleaned_data['author']
            post_title_ = post_form.cleaned_data['post_title']
            post_text_ = post_form.cleaned_data['post_text']
            place_to_visit_id = post_form.cleaned_data['place_to_visit']
            place_to_visit_ = PlaceToVisit.objects.get(id=int(place_to_visit_id[0]))
            post = Post(author=author_, post_title=post_title_, post_text=post_text_,
                        places_to_visit=place_to_visit_)
            post.save()
    return render(request, 'blog/create-post.html', {'post_form': post_form,
                                                     'choices': choices__})

def load_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    images = Image.objects.filter(places_to_visit=post.places_to_visit)
    image_list = [image for image in images]
    print(images)
    context = {'post': post,
                'images': image_list}
    return render(request, 'blog/load-post.html', context)
                                                     
def edit_post(request, post_id):
    post_form = PostForm()
    old_post_object = Post.objects.get(pk=post_id)
    print(old_post_object.author)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            old_post_object.author = post_form.cleaned_data['author']
            old_post_object.post_title = post_form.cleaned_data['post_title']
            old_post_object.post_text = post_form.cleaned_data['post_text']
            place_to_visit_id = post_form.cleaned_data['place_to_visit']
            place_to_visit_ = PlaceToVisit.objects.get(id=int(place_to_visit_id[0]))
            old_post_object.place_to_visit_name = place_to_visit_
            old_post_object.save()
            return HttpResponseRedirect(reverse('blog:main'))
    else:        
        return render(request, 'blog/edit.html', {'old_post_object': old_post_object,
                                                'post_form': post_form,
                                                'choices': choices__})


def create_place_to_visit(request):
    if request.method == 'POST':
        place_to_visit_form = PlaceToVisitForm(request.POST)
        if place_to_visit_form.is_valid():
            country_name_ = place_to_visit_form.cleaned_data['country_name']
            places_to_visit_ = place_to_visit_form.cleaned_data['place_to_visit']
            place_to_visit = PlaceToVisit(country_name=country_name_, places_to_visit=places_to_visit_)
            place_to_visit.save()
            return HttpResponseRedirect(reverse('blog:main'))
    else:
        place_to_visit_form = PlaceToVisitForm()
    return render(request, 'blog/create-place-to-visit.html', {'place_to_visit_form': place_to_visit_form})

def upload_image(request):
    image_form = ImageForm()
    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES) 
        if image_form.is_valid():
            title_ = image_form.cleaned_data['title']
            place_to_visit_id = image_form.cleaned_data['place_to_visit']
            place_to_visit_ = PlaceToVisit.objects.get(id=int(place_to_visit_id[0]))
            img_ = image_form.cleaned_data.get('image')
            image = Image(title=title_, img=img_, places_to_visit=place_to_visit_)
            image.save()
            return HttpResponseRedirect(reverse('blog:main'))
    else:
        return render(request, 'blog/upload-image.html', {'image_form': image_form,
                                                     'choices': choices__})

def boot(request):
    return render(request, 'blog/boot.html')




def scss(request):
    return render(request, 'blog/indexc.html')

