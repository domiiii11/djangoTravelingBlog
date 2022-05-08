from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'blog'

urlpatterns = [
    path("",views.index, name="main"),
    path("create/", views.create_post, name="create"),
    path("edit/<int:post_id>", views.edit_post, name="edit"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("boostrap/", views.boostrap, name="boostrap"),
    path("scss-style/", views.scss, name="scss-style")
    
]



