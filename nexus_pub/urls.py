from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('article/<int:id>', views.view_article, name="view_article"),
    path('<str:category>', views.view_category, name="view_category"),
    path('staff/<str:name>', views.view_staff, name="view_staff"),
    path('search/', views.search, name="search"),
]
