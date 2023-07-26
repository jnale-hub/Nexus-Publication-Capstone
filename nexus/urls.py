from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("nexus_pub.urls")),
    path('games/', include("nexus_games.urls")),
    path('world_news/', include("world_news.urls")),
]