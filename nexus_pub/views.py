from django.shortcuts import render
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse
import requests
from django.core.paginator import Paginator
from django.db.models import Max

from .models import *


from django.db.models import OuterRef, Subquery

def index(request):
    # Get the latest article by each category
    categories = Category.objects.all()
    latest_articles = Article.objects.filter(
        category=OuterRef('category')
    ).order_by('-date_published')
    
    headlines = Article.objects.filter(
        id=Subquery(latest_articles.values('id')[:1])
    )

    # Fetch articles and paginate the results
    all_articles = Article.objects.exclude(
        id__in=headlines.values('id')
    ).order_by("-date_published")

    paginator = Paginator(all_articles, 12)
    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    # Send the article feed and headlines to the template in the context
    context = {
        "articles": articles,
        "headlines": headlines,
    }
    return render(request, 'nexus_pub/index.html', context)



def view_article(request, id):
    articles = Article.objects.get(pk=id)

    return render(request, 'nexus_pub/article.html', {
        "article": articles,
    })