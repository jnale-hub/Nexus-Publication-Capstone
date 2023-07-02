from django.db import models
from django.conf import settings

class User(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='user_pictures')
    points = models.IntegerField(default=0)

class Staff(models.Model):
    name = models.CharField(max_length=100)
    picture = models.URLField(default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    cover = models.URLField(default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png")
    description = models.TextField()
    email = models.EmailField()
    
    def __str__(self):
        return self.name

class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category

class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True, max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="article_category")
    author = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="article_author")
    date_published = models.DateField()
    content = models.TextField(default='')
    image = models.URLField(default=settings.DEFAULT_IMAGE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class Game(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='game_images')
