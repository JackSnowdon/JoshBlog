from django.urls import path
from .views import *

urlpatterns = [
    path("blog_home/", blog_home, name="blog_home"),
    path("add_post/", add_post, name="add_post"),
    path(r'edit_post/<int:pk>', edit_post, name="edit_post"),

]