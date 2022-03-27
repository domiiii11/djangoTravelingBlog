from django.http import HttpResponseNotFound
from django.shortcuts import render
from blog.models import Post, Country


def index(request):
    posts = Post.objects.order_by('release_date')
    numbers = []
    for post in posts:
        numbers.append(post.id)
        print(numbers)
    countries = Country.objects.all()    
    context = {'posts': posts,
               "country": countries,
               "numbers": numbers}
    return render(request, "blog/index.html", context)


def posts(request):
    # Post = Post.objects.get(pk=post_id)
    # print(Post.post_id)
    # Country = Country.objects.get(pk=country_id)
    context = {'post': Post,
               'country': Country}
    return render(request, 'blog/posts.html', context)


def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    context = {'post': post,
               }
    return render(request, 'blog/post.html', context)
