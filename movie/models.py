from django.db import models
from django.urls import reverse
from django.conf import settings


def get_default_poster_image():
    return "defaultImage/clapperboard.png"


def get_poster_image_filepath(self, filename):
    return f'movie_posters/{self.pk}/{filename}'


class TopMovies(models.Model):
    poster_link = models.CharField(max_length=2000, blank=True, null=True)
    series_title = models.CharField(max_length=300, blank=True, null=True)
    released_year = models.SmallIntegerField(blank=True, null=True)
    certificate = models.CharField(max_length=25, blank=True, null=True)
    runtime = models.CharField(max_length=10, blank=True, null=True)
    genre = models.CharField(max_length=500, blank=True, null=True)
    imdb_rating = models.DecimalField(
        max_digits=600, decimal_places=1, blank=True, null=True)
    overview = models.TextField(max_length=313, blank=True, null=True)
    meta_score = models.SmallIntegerField(blank=True, null=True)
    director = models.CharField(max_length=250, blank=True, null=True)
    star1 = models.CharField(max_length=250, blank=True, null=True)
    star2 = models.CharField(max_length=250, blank=True, null=True)
    star3 = models.CharField(max_length=250, blank=True, null=True)
    star4 = models.CharField(max_length=250, blank=True, null=True)
    no_of_votes = models.IntegerField(blank=True, null=True)
    gross = models.IntegerField(blank=True, null=True)
    poster_path = models.ImageField(max_length=255, upload_to=get_poster_image_filepath,
                                    null=True, blank=True, default=get_default_poster_image)

    class Meta:
        managed = False
        db_table = 'Top_Movies'

    def get_absolute_url(self):
        return reverse('movie:update', kwargs={'pk': self.pk})


class FavoriteMovies (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(
        TopMovies, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = "favorite_movies"
        unique_together = ("user", "movie")


# class ImdbMovies(models.Model):
#     imdb_title_id = models.CharField(primary_key=True, max_length=10)
#     title = models.TextField(max_length=200, blank=True, null=True)
#     # original_title = models.CharField(max_length=-1, blank=True, null=True)
#     year = models.IntegerField(blank=True, null=True)
#     # date_published = models.CharField(max_length=-1, blank=True, null=True)
#     genre = models.TextField(max_length=31, blank=True, null=True)
#     duration = models.IntegerField(blank=True, null=True)
#     country = models.TextField(max_length=225, blank=True, null=True)
#     language = models.TextField(max_length=200, blank=True, null=True)
#     # director = models.CharField(max_length=-1, blank=True, null=True)
#     # writer = models.CharField(max_length=-1, blank=True, null=True)
#     # production_company = models.CharField(max_length=-1, blank=True, null=True)
#     # actors = models.CharField(max_length=-1, blank=True, null=True)
#     description = models.TextField(max_length=500, blank=True, null=True)
#     avg_vote = models.FloatField(blank=True, null=True)
#     votes = models.IntegerField(blank=True, null=True)
#     budget = models.CharField(max_length=200, blank=True, null=True)
#     usa_gross_income = models.CharField(max_length=200, blank=True, null=True)
#     worlwide_gross_income = models.CharField(
#         max_length=200, blank=True, null=True)
#     metascore = models.FloatField(blank=True, null=True)
#     reviews_from_users = models.FloatField(blank=True, null=True)
#     reviews_from_critics = models.FloatField(blank=True, null=True)

#     class Meta:
#         # managed = False
#         db_table = 'imdb_movies'


# class ImdbTitlePrincipals(models.Model):
#     imdb_title_id = models.CharField(max_length=10, blank=True, null=True)
#     ordering = models.IntegerField(blank=True, null=True)
#     imdb_name_id = models.CharField(max_length=10, blank=True, null=True)
#     category = models.CharField(max_length=20, blank=True, null=True)
#     job = models.CharField(max_length=130, blank=True, null=True)
#     characters = models.TextField(blank=True, null=True)

#     class Meta:
#         # managed = False
#         db_table = 'imdb_title_principals'


# class ImdbNames(models.Model):
#     imdb_name_id = models.CharField(max_length=10, blank=True, null=True)
#     name = models.TextField(max_length=100, blank=True, null=True)
#     # birth_name = models.CharField(max_length=-1, blank=True, null=True)
#     # height = models.IntegerField(blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     # birth_details = models.CharField(max_length=-1, blank=True, null=True)
#     # date_of_birth = models.CharField(max_length=-1, blank=True, null=True)
#     # place_of_birth = models.CharField(max_length=-1, blank=True, null=True)
#     # death_details = models.CharField(max_length=-1, blank=True, null=True)
#     # date_of_death = models.CharField(max_length=-1, blank=True, null=True)
#     # place_of_death = models.CharField(max_length=-1, blank=True, null=True)
#     # reason_of_death = models.CharField(max_length=-1, blank=True, null=True)
#     # spouses_string = models.CharField(max_length=-1, blank=True, null=True)
#     # spouses = models.IntegerField(blank=True, null=True)
#     # divorces = models.IntegerField(blank=True, null=True)
#     # spouses_with_children = models.IntegerField(blank=True, null=True)
#     # children = models.IntegerField(blank=True, null=True)

#     class Meta:
#         # managed = False
#         db_table = 'imdb_names'
