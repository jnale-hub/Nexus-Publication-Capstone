from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import F, Value
from django.db import models
from django.http import JsonResponse
from .models import GameResult
from nexus_pub.models import User

def games(request):
    return render(request, "games/games.html", {"games": True})

@login_required
def wordle(request):
    user = request.user

    # Try to get the user's existing GameResult or create a new one with default values
    game_result, created = GameResult.objects.get_or_create(user=user, defaults={'wordle_played': 0, 'wordle_won': 0})
    
    games_played = game_result.wordle_played
    games_won = game_result.wordle_won
    
    # Calculate percentage_wins (avoid division by zero)
    percentage_wins = (games_won * 100) / games_played if games_played > 0 else 0

    # Get the top 5 users with the highest number of games won
    top_users = GameResult.objects.order_by('-wordle_won')[:5]

    return render(request, "games/wordle.html", {
        'games_played': games_played,
        'games_won': games_won,
        'percentage_wins': percentage_wins,
        'top_users': top_users,
    })

@csrf_exempt
@login_required
def update_points(request):
    if request.method == "POST":
        user = request.user

        # Use F() expression to increment the points directly in the database
        User.objects.filter(pk=user.pk).update(points=F('points') + 1)

        # Retrieve the updated points value after the update
        updated_points = User.objects.get(pk=user.pk).points

        # Return a success response with the updated points value
        return JsonResponse({"success": True, "points": updated_points}, safe=False)

    return JsonResponse({"success": False}, safe=False)

@csrf_exempt
@login_required
def update_stats(request, isWin):

    isWin = isWin.lower() == 'true'

    if request.method == "POST":
        user = request.user

        # Get or create the GameResult object for the user
        game_result, created = GameResult.objects.get_or_create(user=user, defaults={"wordle_played": 0, "wordle_won": 0})

        # Update the statistics based on isWin using F() expressions
        if isWin:
            game_result.wordle_won = F('wordle_won') + 1
        game_result.wordle_played = F('wordle_played') + 1
        game_result.save()

        # Get the updated game statistics
        game_result = GameResult.objects.get(user=user)

        games_played = game_result.wordle_played
        games_won = game_result.wordle_won

        # Calculate the percentage_wins (avoid division by zero)
        percentage_wins = (games_won * 100) / games_played if games_played > 0 else 0

        # Return the JSON response with updated statistics
        return JsonResponse({
            "success": True,
            "games_played": games_played,
            "games_won": games_won,
            "percentage_wins": percentage_wins,
        })

    return JsonResponse({"success": False})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        article_id = request.POST.get("article_id")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if article_id:
                article_url = reverse('view_article', kwargs={'id': article_id})
                return redirect(f"{article_url}#toggle-comments")
            return redirect("games")
        else:
            messages.error(request, 'Invalid username and/or password.')
            return redirect("games")
    else:
        return redirect("games")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("games"))

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        # Ensure password matches confirmation
        if password != confirmation:
            messages.error(request, 'Passwords does not match!')

        # Attempt to create new user
        try:
            user = User.objects.create_user(name=name, username=username, email=email, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("games"))
        except IntegrityError as e:
            if 'UNIQUE constraint failed: nexus_pub_user.username' in str(e):
                messages.error(request, 'Username already taken. Please choose a different username.')
            else:
                # Handle other IntegrityError cases or unexpected errors
                print(e)
                messages.error(request, 'An error occurred. Please try again later.')

    return redirect("games")
