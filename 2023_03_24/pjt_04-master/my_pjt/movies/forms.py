from django import forms
from .models import Movie
import datetime


class MovieForm(forms.ModelForm):
    GENRE_CHOICES = (
        ('코미디','comedy'),
        ('공포','horror'),
        ('로맨스','romance'),
        ('스릴러','Thriller')
    )
    genre = forms.ChoiceField(choices=GENRE_CHOICES)
    score=forms.FloatField(widget=forms.NumberInput(attrs={'step':'0.5', 'min':'0', 'max':'5'}))
    release_date=forms.DateField(initial=datetime.date.today)
    class Meta:
        model = Movie
        fields = '__all__'