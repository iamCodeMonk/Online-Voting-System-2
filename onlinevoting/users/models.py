from django.db import models
from  django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import AbstractUser
from blog.models import Society

class Profile(models.Model):
    user =  models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Member(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    socities = models.ManyToManyField(Society)

    def __str__(self):
        return f'{self.user.username} Member'

class Elections(models.Model):
    Name = models.CharField(max_length = 100)
    Discription = models.TextField()
    society = models.ForeignKey(Society, on_delete = models.CASCADE)
    whoallvoted = models.ManyToManyField(User, related_name = 'Check_vote_once')

    def __str__(self):
        return self.Name

# Create your models here.
