from movie.models import TopMovies
from typing import ContextManager
from django.shortcuts import render
from django.conf import settings

DEBUG = False


def home_screen_view(request):
    context = {}
    context['debug_mode'] = settings.DEBUG
    context['debug'] = DEBUG
    context['room_id'] = "1"
    top_10_movies = TopMovies.objects.all().order_by('-imdb_rating')[:10]
    context['top_10_movies'] = top_10_movies
    return render(request, "home/index.html", context)
