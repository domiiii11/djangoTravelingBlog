from django.http import HttpResponseNotFound
from django.shortcuts import render

def index(request):
    number_list = []
    for i in range(3):
        number_list.append(i)
    context = {'cards_content': number_list}
    return render(request, "blog/index.html", context)
    

def posts(request):
    return render(request, 'blog/posts.html')
    

def post(request, post_id): 
    context = {'card_id': post_id}
    return render(request, 'blog/post.html', context)
    