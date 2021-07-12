from django.urls import path
from .views import MovieListView, MovieUpdateView, MovieCreateView


app_name = 'movie'

urlpatterns = [
    path('', MovieListView.as_view(), name='home'),
    path('new', MovieCreateView.as_view(), name='create'),
    path('<int:pk>', MovieUpdateView.as_view(), name='update'),

]
