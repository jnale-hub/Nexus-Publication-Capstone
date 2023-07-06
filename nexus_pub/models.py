from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    pass

class Staff(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(blank=True, max_length=100)
    picture = models.URLField(default=settings.DEFAULT_IMAGE)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', default=1)
    date = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    class Meta:
        ordering = ['-date']