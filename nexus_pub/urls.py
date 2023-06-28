from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    # path('article:int:id', views.view_article, name="view_atricle"),
    # path('staffs:name', views.view_staff, name="view_staff"),
]