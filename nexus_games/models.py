from django.db import models
from nexus_pub.models import User

class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wordle_played = models.IntegerField(default=0)
    wordle_won = models.IntegerField(default=0)

    def __str__(self):
        return f"Game results of {self.user}"