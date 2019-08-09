import datetime
import requests
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from ybsearch.models import SearchVideo, Video
from .forms import SearchForm
import json
from django.shortcuts import redirect

# UTAPI = "AIzaSyBPBLE3yjMhaOz_LbHRA_WkDyyXx6GMX3"


def search_view(request):

        form = SearchForm(request.POST)

        if request.method == 'POST' and request.user.is_authenticated:
            videos = []
            search = form.data['search']

            payload = {'part': 'snippet',
                       'key': 'AIzaSyBPBLE3yjMhaOz_LbHRA_WkDyyXx6GMX3s',
                       'order': 'viewCount',
                       'q': search,
                       'maxResults': 50}

            existing_search = SearchVideo.objects.filter(request_string=search)

            if existing_search.exists():
                search_obj = existing_search.first()
                delta = datetime.datetime.now() - search_obj.created_at.replace(tzinfo=None)
                if delta.days > 2:
                    resp = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
                else:
                    videos = Video.objects.filter(search=search_obj)
                    return render(request, 'ybsearch/searchresult.html', context={'objects': list(videos)})
            else:
                resp = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
                search_obj = SearchVideo.objects.create(request_string=search)

            resp_dict = json.loads(resp.content)

            for item in resp_dict['items']:
                if item['id']['kind'] != 'youtube#video':
                    continue

                published_at = item['snippet']['publishedAt']
                title = item['snippet']['title']
                thumbnail = item['snippet']['thumbnails']['default']['url']

                videos.append(Video.objects.create(
                    title=title, image_url=thumbnail,
                    created_at=published_at, search=search_obj
                ))

            return render(request, 'ybsearch/searchresult.html', context={'objects': videos})

        return render(request, 'ybsearch/search-page.html', {'form': SearchForm()})


def authenticate_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'ybsearch/error.html', context={'message': 'Invalid login or password'})
        else:
            return render(request, 'ybsearch/error.html', context={'message': 'Login or password is not specified'})


def logout_view(request):
    if request.method == 'POST' and request.user.is_authenticated:
        logout(request)
        return redirect('/')
