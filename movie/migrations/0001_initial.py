# Generated by Django 2.2.15 on 2021-07-22 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import movie.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TopMovies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poster_link', models.CharField(blank=True, max_length=2000, null=True)),
                ('series_title', models.CharField(blank=True, max_length=300, null=True)),
                ('released_year', models.SmallIntegerField(blank=True, null=True)),
                ('certificate', models.CharField(blank=True, max_length=25, null=True)),
                ('runtime', models.CharField(blank=True, max_length=10, null=True)),
                ('genre', models.CharField(blank=True, max_length=500, null=True)),
                ('imdb_rating', models.DecimalField(blank=True, decimal_places=1, max_digits=600, null=True)),
                ('overview', models.TextField(blank=True, max_length=313, null=True)),
                ('meta_score', models.SmallIntegerField(blank=True, null=True)),
                ('director', models.CharField(blank=True, max_length=250, null=True)),
                ('star1', models.CharField(blank=True, max_length=250, null=True)),
                ('star2', models.CharField(blank=True, max_length=250, null=True)),
                ('star3', models.CharField(blank=True, max_length=250, null=True)),
                ('star4', models.CharField(blank=True, max_length=250, null=True)),
                ('no_of_votes', models.IntegerField(blank=True, null=True)),
                ('gross', models.IntegerField(blank=True, null=True)),
                ('poster_path', models.ImageField(blank=True, default=movie.models.get_default_poster_image, max_length=255, null=True, upload_to=movie.models.get_poster_image_filepath)),
            ],
            options={
                'db_table': 'Top_Movies',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FavoriteMovies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movie.TopMovies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'favorite_movies',
                'unique_together': {('user', 'movie')},
            },
        ),
    ]
