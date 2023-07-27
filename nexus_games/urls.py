from django.urls import path
from . import views

urlpatterns = [
    path('', views.games, name='games'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('wordle/', views.wordle, name='wordle'),
    path('update-points/', views.update_points, name='update_points'),
    path('update-stats/<str:isWin>/', views.update_stats, name='update_stats'),
]