from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'blog'

urlpatterns = [
    path("",views.index, name="index"),
    path("edit/<int:post_id>", views.edit_post, name="edit"),
    path("posts/<int:post_id>", views.post, name="post")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)