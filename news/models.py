from django.db import models

class NewsFeed(models.Model): 
    headline = models.CharField(max_length=200) 
    body = models.TextField() 
    date = models.DateField()
    link = models.URLField()
    author = models.TextField()

    def __str__(self):
        return self.headline