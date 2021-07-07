from django.contrib import admin

from movie.models import TopMovies, ImdbMovies, ImdbNames, ImdbTitlePrincipals


class ImdbMoviesAdmin(admin.ModelAdmin):
    list_filter = ['year', 'language']
    list_display = ['imdb_title_id', 'title', 'country', 'language']
    search_fields = ['imdb_title_id', 'title', 'year', ]
    readonly_fields = ['imdb_title_id', ]

    class Meta:
        model = ImdbMovies


class TopMoviesAdmin(admin.ModelAdmin):
    list_filter = ['genre']
    list_display = ['series_title', 'certificate', 'runtime', 'overview']
    search_fields = ['series_title', 'released_year', ]
    # readonly_fields = ['genre', ]

    class Meta:
        model = TopMovies


admin.site.register(ImdbMovies, ImdbMoviesAdmin)
admin.site.register(TopMovies, TopMoviesAdmin)
