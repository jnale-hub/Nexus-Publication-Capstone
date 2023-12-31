from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.conf import settings
from datetime import datetime
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Max, Q, OuterRef, Subquery
from django.contrib import messages
from django.http import JsonResponse

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

    # Fetch articles and order them by date_published
    articles = Article.objects.exclude(
        id__in=headlines.values('id')
    ).order_by("-date_published")

    # Create a Paginator object and specify the number of articles per page
    paginator = Paginator(articles, 12)  # Show 10 articles per page

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page from the Paginator object
    page_obj = paginator.get_page(page_number)

    # Send the article feed, headlines, and page_obj to the template in the context
    context = {
        "categories": categories,
        "articles": page_obj,
        "headlines": headlines,
        "page_obj": page_obj,
    }
    return render(request, 'nexus_pub/index.html', context)

def view_article(request, id):
    article = get_object_or_404(Article, pk=id)
    comments = Comment.objects.filter(article=article)

    return render(request, 'nexus_pub/article.html', {
        'article': article,
        'comments': comments,
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
    articles = Article.objects.filter(author=staff).order_by('-date_published')

    # Create a Paginator object and specify the number of articles per page
    paginator = Paginator(articles, 3)  # Show 10 articles per page

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page from the Paginator object
    page_obj = paginator.get_page(page_number)

    # Send the staff, articles, and page_obj to the template in the context
    context = {
        "staff": staff,
        "articles": page_obj,
        "page_obj": page_obj,
    }
    return render(request, 'nexus_pub/staff.html', context)

def search(request):
    query = request.GET.get('q')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    articles = Article.objects.all()
    date_range = ''
    
    if query:
        articles = articles.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(description__icontains=query) | Q(author__name__icontains=query)
        )
    
    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Check if the start date is before or equal to the end date
        if start_date <= end_date:
            articles = articles.filter(date_published__range=[start_date, end_date])
            date_range = f"from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"
        else:
            # Swap the dates if the start date is after the end date
            start_date, end_date = end_date, start_date
            articles = articles.filter(date_published__range=[start_date, end_date])
            date_range = f"from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"
    
    elif start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        articles = articles.filter(date_published__gte=start_date)
        date_range = f"from {start_date.strftime('%B %d, %Y')}"
    
    elif end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        articles = articles.filter(date_published__lte=end_date)
        date_range = f"until {end_date.strftime('%B %d, %Y')}"

    paginator = Paginator(articles, 12)  # Show 10 articles per page

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the corresponding page from the Paginator object
    page_obj = paginator.get_page(page_number)

    context = {
        "articles": page_obj,
        "date_range": date_range,
        "search": query,
        "categories": categories,
        "page_obj": page_obj
    }
    
    return render(request, 'nexus_pub/index.html', context)

@login_required
def add_comment(request, id):
    article = get_object_or_404(Article, pk=id)

    if request.method == 'POST':
        new_comment = Comment(
            user=request.user,
            article=article,
            content=request.POST['comment_content'],
            date=datetime.now()
        )
        new_comment.save()
        return redirect('view_article', id=id)

    return redirect('view_article', id=id)

@login_required
def star_article(request, id):

    article = get_object_or_404(Article, pk=id)
    user = request.user
    if request.method == "POST":
        if article in user.starred_articles.all():
            user.starred_articles.remove(article)
        else:
            user.starred_articles.add(article)

        return HttpResponseRedirect(resolve_url('view_article', id=id))

@login_required
def save_article(request, id):
    article = get_object_or_404(Article, pk=id)
    user = request.user
    if request.method == "POST":
        if article in user.saved_articles.all():
            user.saved_articles.remove(article)
        else:
            user.saved_articles.add(article)
        return HttpResponseRedirect(resolve_url('view_article', id=id))

@login_required
def starred_articles(request):
    # Get the logged-in user
    user = request.user

    # Filter the articles that the user has starred
    articles = user.starred_articles.all()

    # Send the articles to the template in the context
    context = {
        "articles": articles,
        "starred": True,
    }
    return render(request, 'nexus_pub/minimal.html', context)

@login_required
def saved_articles(request):
    # Get the logged-in user
    user = request.user

    # Filter the articles that the user has starred
    articles = user.saved_articles.all()

    # Send the articles to the template in the context
    context = {
        "articles": articles,
        "saved": True,
    }
    return render(request, 'nexus_pub/minimal.html', context)

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        # Get the form inputs from the request
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            # Update the user's data
            if name:
                user.name = name
            if username:
                user.username = username
            if email:
                user.email = email
            user.save()
            messages.success(request, 'Profile updated successfully.')

            # Redirect the user to a success page or any other desired location
            return redirect('index')

        except IntegrityError as e:
            # Handle the IntegrityError
            messages.error(request, 'An error occurred while updating the profile. Please try again.')

    return redirect('index')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        article_id = request.POST.get("article_id")
        is_games = request.POST.get("is_games")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if article_id:
                article_url = reverse('view_article', kwargs={'id': article_id})
                return redirect(f"{article_url}#toggle-comments")
            elif is_games:
                print("Is Games")
                return redirect("games")
            return redirect("index")
        else:
            messages.error(request, 'Invalid username and/or password.')
            if is_games:
                print("Is Games")
                return redirect("games")
            return redirect("index")
    else:
        if is_games:
            return redirect("games")
        return redirect("index")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        article_id = request.POST.get("article_id")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        is_games = request.POST.get("is_games")

        # Ensure password matches confirmation
        if password != confirmation:
            messages.error(request, 'Passwords does not match!')

        # Attempt to create new user
        try:
            user = User.objects.create_user(name=name, username=username, email=email, password=password)
            login(request, user)
            if article_id:
                article_url = reverse('view_article', kwargs={'id': article_id})
                return redirect(f"{article_url}#toggle-comments")
            elif is_games:
                print("Is Games")
                return redirect("games")
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError as e:
            if 'UNIQUE constraint failed: nexus_pub_user.username' in str(e):
                messages.error(request, 'Username already taken. Please choose a different username.')
            else:
                # Handle other IntegrityError cases or unexpected errors
                print(e)
                messages.error(request, 'An error occurred. Please try again later.')

    return redirect("index")
