from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from nexus_pub.models import User
from .models import GameResult

def games(request):
    return render(request, "games/games.html", {"games": True})

@login_required
def wordle(request):
    user = request.user
    game_results = GameResult.objects.filter(user=user)
    
    # Calculate games_played and games_won for Wordle
    games_played = sum(result.wordle_played for result in game_results)
    games_won = sum(result.wordle_won for result in game_results)
    
    # Calculate percentage_wins (avoid division by zero)
    percentage_wins = (games_won * 100) / games_played if games_played > 0 else 0

    return render(request, "games/wordle.html", {
        'games_played': games_played,
        'games_won': games_won,
        'percentage_wins': percentage_wins,
    })

@csrf_exempt
@login_required
def update_points(request):
    if request.method == "POST":
        user = request.user
        user.points += 1
        user.save()
        return JsonResponse({
            "success": True,
            "points": user.points,
        })
    return JsonResponse({"success": False})