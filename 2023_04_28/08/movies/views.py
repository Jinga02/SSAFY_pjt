from django.shortcuts import render, get_list_or_404, get_object_or_404 
from django.views.decorators.http import require_safe
from .models import Movie
from . serializers import MovieSerializer
from django.db.models import Sum, Avg


# Create your views here.
@require_safe
def index(request):
    movie = get_list_or_404(Movie)
    # form = MovieForm()
    serializers = MovieSerializer(movie, many=True)
    context = {
        'movies' : serializers.data,
        # 'form' : form,
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializers = MovieSerializer(movie)
    context = {
        'movies' : serializers.data,
    }
    return render(request, 'movies/detail.html', context)



@require_safe
def recommended(request):
    movie = get_list_or_404(Movie)
    serializers = MovieSerializer(movie, many=True)
    total_vote_count = Movie.objects.aggregate(Sum('vote_count'))['vote_count__sum']
    average_vote_count = Movie.objects.aggregate(Avg('vote_count'))['vote_count__avg']
    avg_popularity = round(Movie.objects.aggregate(Avg('popularity'))['popularity__avg'])
    recommended_movies = []
    for movie in serializers.data:
        if movie['vote_count'] >= average_vote_count and movie['popularity'] >= avg_popularity:
            recommended_movies.append(movie)
    context = {
        'movies' : recommended_movies[:10],
        'total_vote_count': total_vote_count,
        'average_vote_count': average_vote_count,
        'avg_popularity' : avg_popularity,
    }
    return render(request, 'movies/recommended.html', context)