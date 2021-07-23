from django.urls import path
from .views import MovieListView, MovieUpdateView, MovieCreateView, MovieDetailView, likeit, unlikeit


app_name = 'movie'

urlpatterns = [
    path('', MovieListView.as_view(), name='home'),
    path('new', MovieCreateView.as_view(), name='create'),
    path('<int:pk>', MovieUpdateView.as_view(), name='update'),
    path('details/<int:pk>', MovieDetailView.as_view(), name='details'),
    path('like/<int:pk>', likeit, name='likeIt'),
    path('unlike/<int:pk>', unlikeit, name='UnlikeIt')
    # path("ajax/like/", likeit, name="ajax_likeIt"),
    # path("ajax/load_report/", load_report, name="ajax_load_report"),

]
