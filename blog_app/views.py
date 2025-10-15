from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import os
from django.conf import settings

# Sample data: blog posts
posts = [
    {
        'id': 1,
        'title': 'Tech Trends 2025',
        'content': 'Exploring AI and quantum computing.',
        'category': 'tech',
        'image': 'tech.svg',
    },
    {
        'id': 2,
        'title': 'Healthy Lifestyle Tips',
        'content': 'Daily habits for better health.',
        'category': 'lifestyle',
        'image': 'lifestyle.svg',
    },
    {
        'id': 3,
        'title': 'Travel Adventures',
        'content': 'Best places to visit in Europe.',
        'category': 'travel',
        'image': 'travel.svg',
    },
]

def get_user_prefs(request):
    return {
        'theme': request.COOKIES.get('theme', 'light'),
        'language': request.COOKIES.get('language', 'EN'),
        'last_visited': json.loads(request.COOKIES.get('last_visited', '[]')),
        'preferred_categories': request.COOKIES.get('categories', 'tech,lifestyle,travel').split(','),
    }

def home(request):
    prefs = get_user_prefs(request)
    filtered_posts = [post for post in posts if post['category'] in prefs['preferred_categories']]
    visited_posts = [post for post in posts if post['id'] in prefs['last_visited']]
    context = {
        'posts': filtered_posts,
        'visited_posts': visited_posts,
        'theme': prefs['theme'],
        'language': prefs['language'],
    }
    return render(request, 'blog_app/home.html', context)

def preferences(request):
    if request.method == 'POST':
        response = redirect('home')
        theme = request.POST.get('theme', 'light')
        response.set_cookie('theme', theme, max_age=3600*24*30)
        language = request.POST.get('language', 'EN')
        response.set_cookie('language', language, max_age=3600*24*30)
        categories = ','.join(request.POST.getlist('categories'))
        response.set_cookie('categories', categories, max_age=3600*24*30)
        return response
    prefs = get_user_prefs(request)
    return render(request, 'blog_app/preferences.html', {'theme': prefs['theme'], 'language': prefs['language']})

def view_post(request, post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return HttpResponse("Post not found", status=404)
    last_visited = json.loads(request.COOKIES.get('last_visited', '[]'))
    if post_id not in last_visited:
        last_visited.append(post_id)
    if len(last_visited) > 5:
        last_visited = last_visited[-5:]
    response = render(request, 'blog_app/post.html', {
        'post': post,
        'theme': request.COOKIES.get('theme', 'light'),
        'language': request.COOKIES.get('language', 'EN'),
    })
    response.set_cookie('last_visited', json.dumps(last_visited), max_age=3600*24*30)
    return response

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        # Generate new post ID
        new_id = max([post['id'] for post in posts], default=0) + 1

        # Handle image
        image_name = 'default.svg'  # Default image if none uploaded
        if image:
            image_name = f"post_{new_id}_{image.name}"
            image_path = os.path.join(settings.STATICFILES_DIRS[0], 'images', image_name)
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)

        # Add new post to the list
        new_post = {
            'id': new_id,
            'title': title,
            'content': content,
            'category': category,
            'image': image_name,
        }
        posts.append(new_post)
        return redirect('home')
    return render(request, 'blog_app/create_post.html', {
        'theme': request.COOKIES.get('theme', 'light'),
        'language': request.COOKIES.get('language', 'EN'),
    })