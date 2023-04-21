from rest_framework import serializers
from .models import Actor, Movie, Review

class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title', 'overview')

class ActorNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('name',)


class MovieTitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('title',)

class ActorDeatilSerializer(serializers.ModelSerializer):
    movies = MovieTitleSerializer(many=True, read_only=True)
    class Meta:
        model = Actor
        fields = ('id', 'movies', 'name')

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('title', 'content',)
        read_only_fields = ('movie',)

class ReviewDetailSerializer(serializers.ModelSerializer):
    movie = MovieTitleSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'title', 'movie', 'content')

class ReviewModifySerializer(serializers.ModelSerializer):
    movie = MovieTitleSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'movie', 'title', 'content')
        read_only_fields = ('movie',)

class MovieDetailSerializer(serializers.ModelSerializer):
    actors = ActorNameSerializer(many=True,read_only=True)
    review_set = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ('id', 'actors', 'review_set', 'title', 'overview', 'release_date', 'poster_path')        

