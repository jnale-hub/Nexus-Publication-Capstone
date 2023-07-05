from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Max, Q, OuterRef, Subquery

from .models import *

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

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        name = request.POST["name"]
        password = request.POST["password"]
        user = authenticate(request, username=name, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "nexus_pub/index.html", {
                "message": "Invalid email and/or password."
            })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "nexus_pub/index.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(name, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "nexus_pub/index.html", {
                "message": "Name already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))