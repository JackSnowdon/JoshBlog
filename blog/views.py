from django.shortcuts import render, redirect, reverse
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
        return redirect("index")
