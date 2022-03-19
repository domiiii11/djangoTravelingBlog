from django.urls import path

from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("posts", views.posts, name="posts"),
    path("posts/<str:post_id>", views.post, name="post")
]
