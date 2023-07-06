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
]
