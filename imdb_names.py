# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ImdbNames(models.Model):
    imdb_name_id = models.CharField(primary_key=True, max_length=-1)
    name = models.CharField(max_length=-1, blank=True, null=True)
    birth_name = models.CharField(max_length=-1, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    birth_details = models.CharField(max_length=-1, blank=True, null=True)
    date_of_birth = models.CharField(max_length=-1, blank=True, null=True)
    place_of_birth = models.CharField(max_length=-1, blank=True, null=True)
    death_details = models.CharField(max_length=-1, blank=True, null=True)
    date_of_death = models.CharField(max_length=-1, blank=True, null=True)
    place_of_death = models.CharField(max_length=-1, blank=True, null=True)
    reason_of_death = models.CharField(max_length=-1, blank=True, null=True)
    spouses_string = models.CharField(max_length=-1, blank=True, null=True)
    spouses = models.IntegerField(blank=True, null=True)
    divorces = models.IntegerField(blank=True, null=True)
    spouses_with_children = models.IntegerField(blank=True, null=True)
    children = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imdb_names'
