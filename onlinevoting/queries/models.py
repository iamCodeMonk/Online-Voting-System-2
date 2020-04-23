from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from blog.models import Society

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('queries-home', kwargs={'pk': self.society.pk,'Name': self.society.Name})
