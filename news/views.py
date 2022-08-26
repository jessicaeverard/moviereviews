from django.shortcuts import render
from .models import NewsFeed

def news(request):

    news = NewsFeed.objects.all().order_by('-date')

    return render (request, 'news.html', {'news': news})
