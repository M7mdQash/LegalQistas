from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Post



def posts_view(request):

    posts = Post.objects.all()

    return render(request, 'posts/posts.html', {
        'posts': posts
    })


@login_required
def create_post_view(request):

    if request.method == "POST":

        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        is_published = True if request.POST.get('is_published') else False

        base_slug = slugify(title)
        slug = base_slug

        counter = 1

        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        Post.objects.create(
            user=request.user,
            title=title,
            slug=slug,
            content=content,
            image=image,
            is_published=is_published
        )

        return redirect('posts:posts_view')

    return render(request, 'posts/create_posts.html')

def post_detail_view(request, slug):

    post = get_object_or_404(Post, slug=slug)

    return render(request, 'posts/detail_posts.html', {
        'post': post
    })

def update_post_view(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if request.user != post.user:
        return redirect('posts:posts_view')

    if request.method == "POST":

        post.title = request.POST.get('title')
        post.content = request.POST.get('content')

        if request.FILES.get('image'):
            post.image = request.FILES.get('image')

        post.save()

        return redirect('posts:post_detail_view', slug=post.slug)

    return render(request, 'posts/update_posts.html', {
        'post': post
    })

def delete_post_view(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if request.user == post.user:
        post.delete()

    return redirect('posts:posts_view')