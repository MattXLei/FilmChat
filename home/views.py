from typing import ContextManager
from django.shortcuts import render
from django.conf import settings
from movie.models import TopMovies

DEBUG = False

def home_screen_view(request):
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['room_id'] = "1"
	toptenfilms = TopMovies.objects.all().order_by("-meta_score")[:10]
	context['movies'] = toptenfilms
	return render(request, "home/index.html", context)