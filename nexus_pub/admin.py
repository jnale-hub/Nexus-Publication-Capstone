from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Article)
admin.site.register(Staff)
admin.site.register(Category)
admin.site.register(Comment)