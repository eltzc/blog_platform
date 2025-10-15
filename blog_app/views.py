from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
import json
import os
from django.conf import settings

# Sample data: blog posts
default_posts = [
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

# Data persistence helpers

def _posts_file_path():
    data_dir = settings.BASE_DIR / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir / 'posts.json'

def ensure_data_file():
    path = _posts_file_path()
    if not path.exists():
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_posts, f, ensure_ascii=False, indent=2)

def load_posts():
    ensure_data_file()
    path = _posts_file_path()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return list(default_posts)

def save_posts(posts_list):
    path = _posts_file_path()
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(posts_list, f, ensure_ascii=False, indent=2)

# Ensure data file exists at import
ensure_data_file()

def get_user_prefs(request):
    return {
        'theme': request.COOKIES.get('theme', 'light'),
        'language': request.COOKIES.get('language', 'EN'),
        'last_visited': json.loads(request.COOKIES.get('last_visited', '[]')),
        'preferred_categories': request.COOKIES.get('categories', 'tech,lifestyle,travel').split(','),
    }

def home(request):
    prefs = get_user_prefs(request)
    posts_list = load_posts()
    filtered_posts = [post for post in posts_list if post['category'] in prefs['preferred_categories']]
    visited_posts = [post for post in posts_list if post['id'] in prefs['last_visited']]
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
    posts_list = load_posts()
    post = next((p for p in posts_list if p['id'] == post_id), None)
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
        posts_list = load_posts()
        new_id = max([post['id'] for post in posts_list], default=0) + 1

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
        posts_list.append(new_post)
        save_posts(posts_list)
        return redirect('home')
    return render(request, 'blog_app/create_post.html', {
        'theme': request.COOKIES.get('theme', 'light'),
        'language': request.COOKIES.get('language', 'EN'),
    })


def delete_post(request, post_id):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    posts_list = load_posts()
    posts_list = [p for p in posts_list if p['id'] != post_id]
    save_posts(posts_list)
    return redirect('home')