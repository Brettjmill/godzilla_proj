from django.shortcuts import render, redirect
from django.contrib import messages
from operator import itemgetter

import bcrypt

import json
import urllib.request

from .models import User, Message, Comment

# Create your views here.

def index(request):
    if 'uuid' in request.session:

        return redirect('/monster_island')

    else:

        return render(request, 'index.html')


def register(request):
    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/')

    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )

        request.session['uuid'] = new_user.id

        return redirect('/monster_island')


def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/')

    else:
        user = User.objects.get(email = request.POST['email'])
        request.session['uuid'] = user.id

        return redirect('/monster_island')


def monster_island(request):
    if 'uuid' not in request.session:

        return redirect('/')
    
    else:
        context = {
            'logged_in_user': User.objects.get(id = request.session['uuid'])
        }
        return render(request, 'monster_island.html', context)

def logout(request):
    del request.session['uuid']

    return redirect('/')


def movie_detail(request, movie_id):
    if 'uuid' not in request.session:

        return redirect('/')

    contents = urllib.request.urlopen(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=845d688f8b4a799bda05a35b3e16c248&language=en-US").read()

    results = json.loads(contents)

    film = []

    film_data = {
        'id': results['id'],
        'title': results['title'],
        'poster': results['poster_path'],
        'year': results['release_date'],
        'summary': results['overview'],
        'tagline': results['tagline']
    }
    film.append(film_data)

    context = {
        'movie': film,
        'messages': Message.objects.all(),
        'comments': Comment.objects.all()
    }

    return render(request, 'movie_detail.html', context)


def collection(request, collection_id):
    if 'uuid' not in request.session:

        return redirect('/')

    contents = urllib.request.urlopen(f"https://api.themoviedb.org/3/collection/{collection_id}?api_key=845d688f8b4a799bda05a35b3e16c248&language=en-US").read()

    results = json.loads(contents)

    coll_films = []

    for part in results['parts']:
        film_data = {
            'id': part['id'],
            'title': part['title'],
            'poster': part['poster_path'],
            'year': part['release_date']
        }
        coll_films.append(film_data)

    sorted_coll_films = sorted(coll_films, key=itemgetter('year'))

    context = {
        'collection': sorted_coll_films
    }

    return render(request, 'movie_collection.html', context)


def all_films(request):
    if 'uuid' not in request.session:

        return redirect('/')

    contents1 = urllib.request.urlopen("https://api.themoviedb.org/3/collection/374509?api_key=845d688f8b4a799bda05a35b3e16c248&language=en-US").read()
    results1 = json.loads(contents1)

    contents2 = urllib.request.urlopen("https://api.themoviedb.org/3/collection/374511?api_key=845d688f8b4a799bda05a35b3e16c248&language=en-US").read()
    results2 = json.loads(contents2)

    contents3 = urllib.request.urlopen("https://api.themoviedb.org/3/collection/374512?api_key=845d688f8b4a799bda05a35b3e16c248&language=en-US").read()
    results3 = json.loads(contents3)

    contents4 = urllib.request.urlopen("https://api.themoviedb.org/3/movie/315011?api_key=845d688f8b4a799bda05a35b3e16c248&language=en-US").read()
    results4 = json.loads(contents4)

    contents5 = urllib.request.urlopen("https://api.themoviedb.org/3/collection/535313?api_key=845d688f8b4a799bda05a35b3e16c248&language=en-US").read()
    results5 = json.loads(contents5)

    coll_films = []

    for part in results1['parts']:
        film_data = {
            'id': part['id'],
            'title': part['title'],
            'poster': part['poster_path'],
            'year': part['release_date']
        }
        coll_films.append(film_data)

    for part in results2['parts']:
        film_data = {
            'id': part['id'],
            'title': part['title'],
            'poster': part['poster_path'],
            'year': part['release_date']
        }
        coll_films.append(film_data)

    for part in results3['parts']:
        film_data = {
            'id': part['id'],
            'title': part['title'],
            'poster': part['poster_path'],
            'year': part['release_date']
        }
        coll_films.append(film_data)

    
    film_data = {
        'id': results4['id'],
        'title': results4['title'],
        'poster': results4['poster_path'],
        'year': results4['release_date']
    }
    coll_films.append(film_data)

    for part in results5['parts']:
        film_data = {
            'id': part['id'],
            'title': part['title'],
            'poster': part['poster_path'],
            'year': part['release_date']
        }
        coll_films.append(film_data)

    sorted_coll_films = sorted(coll_films, key=itemgetter('year'))

    context = {
        'collection': sorted_coll_films
    }

    return render(request, 'all_films.html', context)


def message_post(request, movie_id):
    message = Message.objects.create(
        message_content = request.POST['message_text'],
        user = User.objects.get(id = request.session['uuid']),
        movie = movie_id
    )
    message.save()

    return redirect(f'/detail/{movie_id}')


def comment_post(request, message_id, movie_id):
    comment = Comment.objects.create(
        comment_content = request.POST['comment_text'],
        user = User.objects.get(id = request.session['uuid']),
        message = Message.objects.get(id = message_id)
    )
    comment.save()

    return redirect(f'/detail/{movie_id}')


def watchlist_prep(request, film_id):

    return redirect('/watchlist')


def watchlist(request):
    if 'uuid' not in request.session:

        return redirect('/')


    return render(request, 'watchlist.html')