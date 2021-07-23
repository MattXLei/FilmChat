from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import TopMovies, FavoriteMovies
from .forms import MovieUpdateForm, MovieCreateForm


class MovieCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TopMovies
    form_class = MovieCreateForm
    template_name = "movie/movie_create_form.html"
    success_message = "Movie was created successfully"


class MovieListView(ListView):
    model = TopMovies
    template_name = 'movie/home.html'
    context_object_name = 'movies'
    ordering = ['-released_year']
    paginate_by = 6

    def get_queryset(self):
        q = self.request.GET.get("q")
        object_list = self.model.objects.all()
        if q:
            object_list = object_list.filter(series_title__icontains=q)
        return object_list


class MovieDetailView(DetailView):
    model = TopMovies
    template_name = "movie/movie_detail.html"


class MovieUpdateView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    model = TopMovies
    form_class = MovieUpdateForm
    template_name = "movie/movie_form.html"
    success_message = "Movie was updated successfully"


@login_required
def likeit(request, pk):
    user = request.user
    movie = get_object_or_404(TopMovies, pk=pk)
    userMovie = FavoriteMovies.objects.filter(user=request.user, movie=movie)
    count = len(FavoriteMovies.objects.filter(user=request.user))
    if userMovie:
        messages.info(
            request,  f'"{movie.series_title}" is already in your favorite list.')
    else:
        if len(FavoriteMovies.objects.filter(user=request.user)) >= 3:
            messages.info(request,  'You can only have three favorite movies.')
        else:
            FavoriteMovies(user=request.user, movie=movie).save()
            messages.success(
                request, f'You added "{movie.series_title}" in your favorite list.')

    return redirect('movie:home')


@login_required
def unlikeit(request, pk):
    FavoriteMovies.objects.get(id=pk).delete()
    return redirect('account:view', user_id=request.user.pk)
