from django.http import HttpResponseNotFound
from django.shortcuts import render
from blog.models import Post, Country
    

def index(request):
    number_list = []
    for i in range(3):
        number_list.append(i)
    context = {'cards_content': number_list}
    return render(request, "blog/index.html", context)
    

def posts(request, Post, Country):
    
    return render(request, 'blog/posts.html', context)
    

def post(request, Post, Country): 
    context = {'card_id': Post}
    return render(request, 'blog/post.html', context)
    