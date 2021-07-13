from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .models import TopMovies
from .forms import MovieUpdateForm, MovieCreateForm


class MovieCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TopMovies
    form_class = MovieCreateForm
    template_name = "movies/movie_create_form.html"
    success_message = "Movie was created successfully"


class MovieListView(ListView):
    model = TopMovies
    template_name = 'movies/home.html'
    context_object_name = 'movies'
    ordering = ['-released_year']
    paginate_by = 6

    def get_queryset(self):
        q = self.request.GET.get("q")
        object_list = self.model.objects.all()
        if q:
            object_list = object_list.filter(series_title__icontains=q)
        return object_list


# class MovieDetailView(DetailView):
#     model = TopMovies
#     template_name = "movies/movie_detail.html"


class MovieUpdateView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    model = TopMovies
    form_class = MovieUpdateForm
    template_name = "movies/movie_form.html"
    success_message = "Movie was updated successfully"
