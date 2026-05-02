from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.utils.text import slugify
from .models import Post



def posts_view(request:HttpRequest):

    return render(request, 'posts/posts.html')

def create_post_view(request):

    if request.method == "POST":

        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        is_published = True if request.POST.get('is_published') else False

        slug = slugify(title)

        Post.objects.create(
            user=request.user,
            title=title,
            slug=slug,
            content=content,
            image=image,
            is_published=is_published
        )

        return redirect('posts_view')

    return render(request, 'posts/create_posts.html')