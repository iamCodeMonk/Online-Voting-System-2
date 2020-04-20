from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Society(models.Model):
    Name = models.CharField(max_length = 100)
    Discription = models.TextField()
    Admin = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('society-detail', kwargs={'pk':self.pk})


# Create your models here.
