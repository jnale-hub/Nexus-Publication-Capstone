from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('article/<int:id>/', views.view_article, name="view_article"),
    path('article/<int:id>/comment/', views.add_comment, name="add_comment"), 
    path('category/<str:category>/', views.view_category, name="view_category"),
    path('staff/<str:name>/', views.view_staff, name="view_staff"),
    path('search/', views.search, name="search"),
    path('article/star/<int:id>/', views.star_article, name='star_article'),
    path('article/save/<int:id>/', views.save_article, name='save_article'),
    path('starred_articles/', views.starred_articles, name='starred_articles'),
    path('saved_articles/', views.saved_articles, name='saved_articles'),
]
