# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TopMovies(models.Model):
    poster_link = models.CharField(max_length=2000, blank=True, null=True)
    series_title = models.CharField(max_length=300, blank=True, null=True)
    released_year = models.SmallIntegerField(blank=True, null=True)
    certificate = models.CharField(max_length=25, blank=True, null=True)
    runtime = models.CharField(max_length=-1, blank=True, null=True)
    genre = models.CharField(max_length=500, blank=True, null=True)
    imdb_rating = models.DecimalField(
        max_digits=65535, decimal_places=65535, blank=True, null=True)
    overview = models.CharField(max_length=313, blank=True, null=True)
    meta_score = models.SmallIntegerField(blank=True, null=True)
    director = models.CharField(max_length=250, blank=True, null=True)
    star1 = models.CharField(max_length=250, blank=True, null=True)
    star2 = models.CharField(max_length=250, blank=True, null=True)
    star3 = models.CharField(max_length=250, blank=True, null=True)
    star4 = models.CharField(max_length=250, blank=True, null=True)
    no_of_votes = models.IntegerField(blank=True, null=True)
    gross = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Top_Movies'
