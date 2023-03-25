from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie
from .forms import MovieForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe

@require_safe
def index(request):
    movie = Movie.objects.all()
    context = {
        'movie' : movie
    }
    return render(request, 'movies/index.html', context)

@require_http_methods(['POST', 'GET'])
def create(request):
    movie = Movie.objects.all()
    if request.method=='POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
    context = {
        'form' : form
    }
    return render(request, 'movies/create.html', context)

@require_safe
def detail(request,pk):
    movie = get_object_or_404(Movie, pk=pk)
    context = {
        'movie' : movie
    }
    return render(request, 'movies/detail.html', context)


@require_http_methods(['POST', 'GET'])
def update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', pk = movie.pk)
    else:
        form = MovieForm(instance=movie)

    context = {
        'movie' : movie,
        'form' : form
    }
    return render(request, 'movies/update.html', context)

@require_POST
def delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.delete()
    return redirect('movies:index')
