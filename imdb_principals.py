# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ImdbTitlePrincipals(models.Model):
    imdb_title = models.ForeignKey('ImdbMovies', models.DO_NOTHING, blank=True, null=True)
    ordering = models.IntegerField(blank=True, null=True)
    imdb_name = models.ForeignKey('ImdbNames', models.DO_NOTHING, blank=True, null=True)
    category = models.CharField(max_length=-1, blank=True, null=True)
    job = models.CharField(max_length=-1, blank=True, null=True)
    characters = models.CharField(max_length=-1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imdb_title_principals'
