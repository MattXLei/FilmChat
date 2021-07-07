# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ImdbMovies(models.Model):
    imdb_title_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=200, blank=True, null=True)
    # original_title = models.CharField(max_length=-1, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    date_published = models.CharField(max_length=-1, blank=True, null=True)
    genre = models.CharField(max_length=31, blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=225, blank=True, null=True)
    language = models.CharField(max_length=200, blank=True, null=True)
    # director = models.CharField(max_length=-1, blank=True, null=True)
    # writer = models.CharField(max_length=-1, blank=True, null=True)
    # production_company = models.CharField(max_length=-1, blank=True, null=True)
    # actors = models.CharField(max_length=-1, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    avg_vote = models.FloatField(blank=True, null=True)
    votes = models.IntegerField(blank=True, null=True)
    budget = models.CharField(max_length=200, blank=True, null=True)
    usa_gross_income = models.CharField(max_length=200, blank=True, null=True)
    worlwide_gross_income = models.CharField(
        max_length=200, blank=True, null=True)
    metascore = models.FloatField(blank=True, null=True)
    reviews_from_users = models.FloatField(blank=True, null=True)
    reviews_from_critics = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imdb_movies'
