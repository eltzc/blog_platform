from django.contrib import admin
from django.urls import path
from blog_app.views import home, preferences, view_post, create_post, delete_post

urlpatterns = [
    path('', home, name='home'),
    path('preferences/', preferences, name='preferences'),
    path('post/<int:post_id>/', view_post, name='view_post'),
    path('create/', create_post, name='create_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
]
