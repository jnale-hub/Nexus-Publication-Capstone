from django.urls import path
from . import views

urlpatterns = [
    path('', views.games, name='games'),
    path('logout_games/', views.logout_games, name="logout_games"),
    path('wordle/', views.wordle, name='wordle'),
    path('update-points/', views.update_points, name='update_points'),
    path('update-stats/<str:isWin>/', views.update_stats, name='update_stats'),
]