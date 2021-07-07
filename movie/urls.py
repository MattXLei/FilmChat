from django.urls import path
from .views import MovieListView, MovieUpdateView, MovieDetailView


app_name = 'movie'

urlpatterns = [
    path('', MovieListView.as_view(), name='home'),
    # path('movie/<int:pk>', MovieUpdateView.as_view(), name='update'),
    path('movie/<int:pk>', MovieDetailView.as_view(), name='detail'),


]
