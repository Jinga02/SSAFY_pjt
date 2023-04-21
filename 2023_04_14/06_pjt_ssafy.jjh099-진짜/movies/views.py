from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Comment
from .forms import MovieForm, CommentForm
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
    # movie = Movie.objects.all()
    if request.method=='POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False) # index.html에서 유저정보가 없으면 create 표시 안되게 해서 의미는 없음.
            movie.user = request.user
            movie.save()
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
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    context = {
        'movie' : movie,
        'comment_form' : comment_form,
        'comments' : comments,
    }
    return render(request, 'movies/detail.html', context)


@require_http_methods(['POST', 'GET'])
def update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.user == movie.user:
        if request.method == "POST":
            form = MovieForm(request.POST, request.FILES, instance=movie)
            if form.is_valid():
                movie = form.save()
                return redirect('movies:detail', pk = movie.pk)
        else:
            form = MovieForm(instance=movie)
    else:
        return redirect('movies:detail', pk=movie.pk)
    context = {
        'movie' : movie,
        'form' : form
    }
    return render(request, 'movies/update.html', context)

@require_POST
def delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.user == movie.user:
        movie.delete()
        return redirect('movies:index')
    return redirect('movies:detail', movie.pk)

def community(request):
    return render(request, 'movies/community.html')

@require_POST    
def likes(request, movies_pk):
        
    movie = Movie.objects.get(pk=movies_pk)
    if movie.like_user.filter(pk=request.user.pk).exists():
        movie.like_user.remove(request.user)
        return redirect('movies:index')
    else:
        movie.like_user.add(request.user)
        return redirect('movies:index')
    
@require_POST    
def dislikes(request, movies_pk):
        
    movie = Movie.objects.get(pk=movies_pk)
    if movie.dislike_user.filter(pk=request.user.pk).exists():
        movie.dislike_user.remove(request.user)
        return redirect('movies:index')
    else:
        movie.dislike_user.add(request.user)
        return redirect('movies:index')

@require_POST
def comments_create(request, pk):
    # 아직 미사용
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie = movie
        comment.user =request.user
        comment.save()
    return redirect('movies:detail', movie.pk)

@require_POST
def comments_delete(request, pk, comment_pk):
    # 아직 미사용
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('movies:detail', pk)