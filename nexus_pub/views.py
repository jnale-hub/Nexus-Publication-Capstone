from django.shortcuts import render, get_object_or_404
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse
import requests
from django.core.paginator import Paginator
from django.db.models import Max, Q

from .models import *


from django.db.models import OuterRef, Subquery

categories = Category.objects.all()

def index(request):
    # Get the latest article by each category
    latest_articles = Article.objects.filter(
        category=OuterRef('category')
    ).order_by('-date_published')
    
    headlines = Article.objects.filter(
        id=Subquery(latest_articles.values('id')[:1])
    )

    # Fetch articles and paginate the results
    articles = Article.objects.exclude(
        id__in=headlines.values('id')
    ).order_by("-date_published")

    # Send the article feed and headlines to the template in the context
    context = {
        "categories": categories,
        "articles": articles,
        "headlines": headlines,
    }
    return render(request, 'nexus_pub/index.html', context)


def view_article(request, id):
    articles = Article.objects.get(pk=id)

    return render(request, 'nexus_pub/article.html', {
        "article": articles,
    })

def view_category(request, category):
    # Get the category object
    category_obj = get_object_or_404(Category, category=category)

    # Get articles by category
    articles = Article.objects.filter(category=category_obj)

    # Send the article feed to the template in the context
    context = {
        "articles": articles,
        "category": category,
        "categories": categories
    }
    return render(request, 'nexus_pub/index.html', context)

def view_staff(request, name):
    staff = Staff.objects.get(name=name)
    articles = Article.objects.filter(author=staff)

    context = {
        "staff": staff,
        "articles": articles,
    }
    return render(request, 'nexus_pub/staff.html', context)

def search(request):
    query = request.GET.get('q')
    articles = Article.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(description__icontains=query) | Q(author__name__icontains=query))

    context = {
        "articles": articles,
        'search': query,
        'categories': categories,
    }

    return render(request, 'nexus_pub/index.html', context)

