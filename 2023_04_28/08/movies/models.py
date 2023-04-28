from django.db import models
from django.db.models import Sum, Avg

class Genre(models.Model):
    name = models.CharField(max_length=50)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)

    @staticmethod
    def get_average_vote_count():
        total_vote_count = Movie.objects.aggregate(models.Sum('vote_count'))['vote_count__sum']
        num_movies = Movie.objects.count()
        if total_vote_count and num_movies:
            return total_vote_count / num_movies
        else:
            return 0

    # def averag_popularity_count():
    #     avg_popularity = Movie.objects.aggregate(Avg('popularity'))['popularity__avg']