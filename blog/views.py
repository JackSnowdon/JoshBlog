from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Post
from .forms import PostForm


def blog_home(request):
    posts = Post.objects.all().order_by('-created_on')
    return render(request, "blog_index.html", {"posts": posts})

@login_required
def add_post(request):
    if request.user.profile.staff_access:
        if request.method == "POST":
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.created_on = datetime.now()
                post.last_modified = datetime.now()
                user = request.user
                post.done_by = user.profile
                post.save()
                return redirect("blog_home")
        else:
            post_form = PostForm()
        return render(request, "add_post.html", {"post_form": post_form})
    else:
        return redirect("blog_home")


@login_required
def edit_post(request, pk):
    if request.user.profile.staff_access:
        this_post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            post_form = PostForm(request.POST, instance=this_post)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.last_modified = datetime.now()
                post.save()
                return redirect("blog_home")
        else:
            post_form = PostForm(instance=this_post)
        return render(request, "edit_post.html", {"post_form": post_form})
    else:
        return redirect("blog_home")
