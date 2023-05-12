from rest_framework import serializers
from .models import Movie, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only = True, many = True)
    class Meta:
        model = Movie
        fields = ('id', 'title', 'release_date', 'popularity', 'vote_count', 'vote_average', 'overview', 'poster_path', 'genres',)  