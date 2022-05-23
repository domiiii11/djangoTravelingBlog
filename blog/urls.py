from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'blog'

urlpatterns = [
    path("",views.index, name="main"),
    path("create-post/", views.create_post, name="create-post"),
    path("create-place-to-visit/", views.create_place_to_visit, name="create-place-to-visit"),
    path("upload-image/", views.upload_image, name="upload-image"),
    path("edit-post/<int:post_id>", views.edit_post, name="edit"),
    path("post/<int:post_id>", views.load_post, name="post"),   
    path("scss-style/", views.scss, name="scss-style"),
    path("boot/", views.boot, name="boot"),
    
]



