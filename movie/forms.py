from django import forms
from crispy_forms.helper import FormHelper
from django.db.models import fields
from django.db.models.base import Model
from .models import TopMovies


class MovieForm(forms.ModelForm):

    genre = forms.CharField(widget=forms.TextInput(attrs={'size': '110px'}))

    overview = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 120}))

    class Meta:
        model = TopMovies
        # widgets = {'overview': forms.Textarea(attrs={'size': 120})}
        # exclude = ('poster_link', )
        fields = '__all__'

    def clean_poster_link(self):
        if self.instance:
            return self.instance.poster_link
        else:
            return self.fields['poster_link']

    def clean_series_title(self):
        if self.instance:
            return self.instance.series_title
        else:
            return self.fields['series_title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
