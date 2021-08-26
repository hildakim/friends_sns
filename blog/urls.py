from django.contrib import admin
from django.urls import path
from .views import *

app_name = "blog"

urlpatterns = [
    # path('', feed, name="feed"),
    
    path('personal/<str:id>', personal, name="personal"),

    # path('comment/<str:id>', create_comment, name="create_comment"),

    path('detail/<str:post_id>/comment', create_comment, name="create_comment"),
    path('detail/<str:post_id>/comment/<str:comment_id>', create_re_comment, name="re_comment"),

    path('like/', post_likes, name="post_likes"),
    path('follow/', follow, name="follow"),
    path('post/<str:id>', detail, name="detail"),
    path('new/', new, name="new"),
    path('edit/<str:id>', edit, name="edit"),
    path('delete/<str:id>', delete, name="delete"),
    path('search/', search, name='search'),
]