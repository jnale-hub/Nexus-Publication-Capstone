from django.urls import path
from . import views

urlpatterns = [
    path('', views.games, name='games'),
    path('wordle/', views.wordle, name='wordle'),
    path('update-points/', views.update_points, name='update_points'),
]
