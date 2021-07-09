from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import TopMovies
from .forms import MovieForm


class MovieListView(ListView):
    model = TopMovies
    template_name = 'movies/home.html'
    context_object_name = 'movies'
    ordering = ['-released_year']
    paginate_by = 6


class MovieDetailView(DetailView):
    model = TopMovies
    template_name = "movies/movie_detail.html"


class MovieUpdateView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    model = TopMovies
    form_class = MovieForm
    template_name = "movies/movie_form.html"
    success_message = "Movie was updated successfully"
