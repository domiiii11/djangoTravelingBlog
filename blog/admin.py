from django.contrib import admin

from .models import Post, Country, Image

admin.site.register(Post)
admin.site.register(Country)
admin.site.register(Image)