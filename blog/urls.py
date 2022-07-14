from django.urls import path
from blog import views
from django.urls import reverse
from django.contrib.auth.decorators import login_required

app_name = 'blog'

urlpatterns = [
    path("", views.index, name="main"),
    path("create-post/", views.create_post, name="create-post"),
    path("create-place-to-visit/", views.create_place_to_visit, name="create-place-to-visit"),
    path("upload-image/", views.upload_image, name="upload-image"),
    path("edit-post/<int:post_id>", views.edit_post, name="edit"),
    path("post/<int:post_id>", views.load_post, name="post"),   
    path("scss-style/", views.scss, name="scss-style"),
    path("boot/", views.boot, name="boot"),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='login'),

    
]


