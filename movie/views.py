from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import TopMovies


class MovieListView(ListView):
    model = TopMovies
    template_name = 'movies/home.html'
    context_object_name = 'movies'
    ordering = ['-released_year']
    paginate_by = 6


class MovieDetailView(DetailView):
    model = TopMovies
    template_name = "movies/movie_detail.html"


class MovieUpdateView(UpdateView):
    model = TopMovies
    # fields = ['title', 'content']
