from django.contrib import admin

from .models import Post, Country

admin.site.register(Post)
admin.site.register(Country)