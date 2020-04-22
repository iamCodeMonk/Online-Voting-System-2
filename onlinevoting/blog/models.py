from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Society(models.Model):
    Name = models.CharField(max_length = 100)
    Discription = models.TextField()
    Admin = models.ForeignKey(User, on_delete = models.CASCADE)
    Pending_List = models.ManyToManyField(User, related_name = 'pending_list')
    whoallvoted = models.ManyToManyField(User, related_name = 'Check_vote_once')
    
    def __str__(self):
        return self.Name


# Create your models here.
