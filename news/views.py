from django.shortcuts import render
from .models import NewsFeed
import pandas as pd
import requests
import json

def news(request):
    #deletes everything in model so that there are no duplicates
    NewsFeed.objects.all().delete() 

    url = "https://api.newscatcherapi.com/v2/search?q=movies&page_size=5"
    payload={}
    headers = {
    'x-api-key': 'QWHoJu9X8uUeeTUNpi_W0aGCUtE6x91dygKv3zjfuKc'
    }

    response = requests.request("GET", url, headers=headers, data=payload).json()
    articles = (response['articles']) #array of dictionaries

    df = pd.DataFrame.from_dict(articles)
    df.drop_duplicates(subset=['title'])
    df[['date', 'time']] = df['published_date'].str.split(' ', 1, expand=True)
    articles_df = df[['title', 'author', 'date', 'link', 'summary' ]]

    for index, row in articles_df.iterrows():
        NewsFeed.objects.create(
            headline=row['title'],
            body=row['summary'],
            date=row['date'],
            link=row['link'],
            author=row['author']
        )

    news = NewsFeed.objects.all()
    return render (request, 'news.html', {'news': news})
