from django.shortcuts import get_list_or_404, get_object_or_404
from .models import Actor, Movie, Review
from .serializer import ActorSerializer, ActorDeatilSerializer, MovieSerializer, MovieDetailSerializer, ReviewSerializer, ReviewModifySerializer, ReviewDetailSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
def actors_list(request):
    actors = get_list_or_404(Actor)
    serializer = ActorSerializer(actors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def actor_detail(request, actor_pk):
    actors = get_object_or_404(Actor, pk = actor_pk)
    serializer = ActorDeatilSerializer(actors)
    return Response(serializer.data)


@api_view(['GET'])
def movie_list(request):
    movies = get_list_or_404(Movie)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def movie_detail(request, movie_pk):
    movies = get_object_or_404(Movie, pk = movie_pk)
    serializer = MovieDetailSerializer(movies)
    return Response(serializer.data)

@api_view(['GET'])
def review_list(request):
    reviews = get_list_or_404(Review)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, review_pk):
    reviews = get_object_or_404(Review ,pk = review_pk)
    if request.method == 'GET':
        serializer = ReviewDetailSerializer(reviews)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ReviewModifySerializer(reviews, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':
        delete =   f"review {review_pk} is deleted"
        context = {
            'delete' : delete
        }
        reviews.delete()
        return Response(context, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_review(request, movie_pk):
    movies = get_object_or_404(Movie, pk = movie_pk)
    serializer = ReviewModifySerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movies)
        return Response(serializer.data, status=status.HTTP_201_CREATED)