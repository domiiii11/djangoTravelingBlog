import os
from django.shortcuts import render
from blog.models import Post, PlaceToVisit, Image
from blog.forms import PostForm, PlaceToVisitForm, ImageForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.http import JsonResponse
from blog.custom_storage import MediaStorage
from django.core.files.storage import default_storage
import boto3

# @receiver(user_logged_out)
# def on_user_logged_out(sender, request, **kwargs):
#     messages.add_message(request, messages.INFO, 'Your session has expired please log in again to continue.')

choices_ = PlaceToVisit.objects.all()
choices__ = {place_to_visit.id: place_to_visit.places_to_visit for place_to_visit in choices_}


today = str(timezone.now())[0:3]

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',aws_access_key_id="AKIAZM5DWU7RCO5UEBPV",
    aws_secret_access_key="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")
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response




@login_required
def index(request):
    print("AAAA")
    current_user = request.user
    print(current_user.id)
    posts = Post.objects.order_by('release_date')
    posts_dictionary = {}
    for post in posts:
        print(post)
        images = Image.objects.filter(places_to_visit=post.places_to_visit)
        image_list = [image for image in images]
        if image_list:
            first_image = image_list[0]
            image_url = first_image.img.url[47:] 
            image_url_ = create_presigned_url("django-blog-bucket112", image_url) 
            print(image_url)            
            posts_dictionary[post] = image_url_
        else:
            posts_dictionary[post] = None
    context = {'posts_dictionary': posts_dictionary}
    return render(request, "blog/index.html", context)

@login_required
def create_post(request):
    post_form = PostForm()
    (print("choices VIEW"))
    print("post-method-not-success")
    print(choices__)
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
@login_required
def load_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    images = Image.objects.filter(places_to_visit=post.places_to_visit)
    image_url_list = [image.img.url[47:] for image in images]
    image_presigned_url_ = [create_presigned_url("django-blog-bucket112", image_url) for image_url in image_url_list]
    print(image_presigned_url_)
    context = {'post': post,
                'images': image_presigned_url_}
    return render(request, 'blog/load-post.html', context)

@login_required                                                     
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

@login_required
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

# @login_required
# def upload_image(request):
#     image_form = ImageForm()
#     if request.method == 'POST':
#         image_form = ImageForm(request.POST, request.FILES) 
#         if image_form.is_valid():
#             title_ = image_form.cleaned_data['title']
#             place_to_visit_id = image_form.cleaned_data['place_to_visit']
#             place_to_visit_ = PlaceToVisit.objects.get(id=int(place_to_visit_id[0]))
#             img_ = image_form.cleaned_data.get('image')
#             image = Image(title=title_, img=img_, places_to_visit=place_to_visit_)
#             image.save()
#             return HttpResponseRedirect(reverse('blog:main'))
#     else:
#         return render(request, 'blog/upload-image.html', {'image_form': image_form,
#                                                      'choices': choices__})


@login_required
def upload_image(request):
    # upload_view = FileUploadView()
    image_form = ImageForm()
    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES) 
        if image_form.is_valid():            
            title_ = image_form.cleaned_data['title']
            place_to_visit_id = image_form.cleaned_data['place_to_visit']
            place_to_visit_ = PlaceToVisit.objects.get(id=int(place_to_visit_id[0]))
            img_ = image_form.cleaned_data.get('image')
            # upload_view.post(request)           
            image = Image(title=title_, img=img_, places_to_visit=place_to_visit_)
            image.save()
            return HttpResponseRedirect(reverse('blog:main'))
    else:
        return render(request, 'blog/upload-image.html', {'image_form': image_form,
                                                     'choices': choices__})
    

def user_login(request):
    if request.method == 'POST':
        username_ = request.POST['username']
        print(username_)
        password_ = request.POST['password']
        print(password_)
        user = authenticate(request, username=username_, password=password_)
        if user is not None:
            print(user)
            login(request, user)
            return HttpResponseRedirect(reverse('blog:main'))
        else:
            wrong_data = "Wrong username or password."
  
            return render(request, 'blog/blog-login.html')
    else:
        return render(request, 'blog/blog-login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('blog:login'))    


def authentication(request):
    if not request.user.is_authenticated:
        return redirect('blog:login')
    else:
        return HttpResponse("Hello, You are logged in.")

# class FileUploadView(View):
#     def post(self, requests, **kwargs):
#         file_obj = requests.FILES.get('image', '')

#         # do your validation here e.g. file size/type check

#         # organize a path for the file in bucket
#         file_directory_within_bucket = 'user_upload_files/{username}'.format(username=requests.user)

#         # synthesize a full file path; note that we included the filename
#         file_path_within_bucket = os.path.join(
#             file_directory_within_bucket,
#             file_obj.name
#         )

#         media_storage = MediaStorage()

#         if not media_storage.exists(file_path_within_bucket): # avoid overwriting existing file
#             media_storage.save(file_path_within_bucket, file_obj)
#             file_url = media_storage.url(file_path_within_bucket)

#             return JsonResponse({
#                 'message': 'OK',
#                 'fileUrl': file_url,
#             })
#         else:
#             return JsonResponse({
#                 'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
#                     filename=file_obj.name,
#                     file_directory=file_directory_within_bucket,
#                     bucket_name=media_storage.bucket_name
#                 ),
#             }, status=400)


# def retrieve_image(url, parameters    
#     media_storage = MediaStorage()
#     file_url = media_storage.url(name="IMG_20210821_104612.jpg", parameters={'Bucket': bucket_name,
#                                                             'Key': "IMG_20210821_104612.jpg"},expire=3600, http_method="get_object")
#     print(file_url)
#     return file_url


