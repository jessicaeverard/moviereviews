from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
import requests
import json
import pandas as pd

def home(request):
    #deletes everything in model so that there are no duplicates
    Movie.objects.all().delete() 

    pd.options.mode.chained_assignment = None #default='warn'

    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYjlkMzBiMTAxOWIyYTRiODZkNDcwNGViZmVjNGJiMyIsInN1YiI6IjY0ZDBlODZlODUwOTBmMDEwNjkyNjExNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.LT6SXRREr4WQDgj_uIy0D5QrsqgPEIGYl9HyBkNezwY"
    }
    response = requests.get(url, headers=headers).json()
    movies = response['results']

    df = pd.DataFrame.from_dict(movies)
    df['poster_path'] = 'https://image.tmdb.org/t/p/w500' + df['poster_path'].astype(str)
    moviedf = df[['title', 'poster_path', 'overview' ]]

    for index, row in moviedf.iterrows():
        Movie.objects.create(
            title=row['title'],
            description=row['overview'],
            image_url=row['poster_path'],
    )

    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        searchmovies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        searchmovies = Movie.objects.all()
    return render(request, 'home.html',	{'searchTerm':searchTerm, 'movies': searchmovies})

def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def detail(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie = movie)
    return render(request, 'detail.html', 
                  {'movie':movie, 'reviews': reviews})

@login_required
def createreview(request, movie_id):   
    movie = get_object_or_404(Movie,pk=movie_id) 
    if request.method == 'GET':
        return render(request, 'createreview.html', 
                      {'form':ReviewForm(), 'movie': movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(request, 'createreview.html', 
              {'form':ReviewForm(),'error':'bad data passed in'})

@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', 
                      {'review': review,'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            return render(request, 'updatereview.html',
             {'review': review,'form':form,'error':'Bad data in form'})

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.movie.id)