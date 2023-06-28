from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='user_pictures')
    points = models.IntegerField(default=0)

class Staff(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='staff_pictures')
    cover = models.ImageField(upload_to='staff_covers')
    description = models.TextField()
    email = models.EmailField()

class News(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    date_published = models.DateField()

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='game_images')
